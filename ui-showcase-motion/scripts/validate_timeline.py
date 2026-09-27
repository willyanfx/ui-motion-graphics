#!/usr/bin/env python3
"""Check a complete motion timeline's structural contract; does not render or verify source assets."""
import argparse
import json
import math
from pathlib import Path


def validate(data):
    errors, warnings = [], []

    def problem(where, message):
        errors.append(f'{where}: {message}')

    def objects(value, where):
        if not isinstance(value, list):
            problem(where, 'must be an array')
            return []
        result = []
        for i, item in enumerate(value):
            if not isinstance(item, dict):
                problem(f'{where}[{i}]', 'must be an object')
            else:
                result.append(item)
        return result

    def integer(value):
        return type(value) is int

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def frame(value, where, low, high, exclusive=True):
        valid = integer(value) and low <= value and (value < high if exclusive else value <= high)
        if not valid:
            problem(where, f'must be an integer in [{low}, {high}{")" if exclusive else "]"}')
        return valid

    def unique(items, where):
        found = {}
        for i, item in enumerate(items):
            identity = item.get('id')
            if not text(identity):
                problem(f'{where}[{i}].id', 'must be a nonempty string')
            elif identity in found:
                problem(where, f'duplicate ID {identity}')
            else:
                found[identity] = item
        return found

    def track(items, where, start, end):
        last = start - 1
        for i, item in enumerate(objects(items, where)):
            value = item.get('frame')
            if frame(value, f'{where}[{i}].frame', start, end):
                if value <= last:
                    problem(where, 'frames must be strictly increasing; combine properties at the same frame')
                last = value
        return last

    def hold(item, where, start, end, last):
        if 'holdUntil' in item:
            value = item['holdUntil']
            if frame(value, f'{where}.holdUntil', start, end, exclusive=False) and value <= last:
                problem(where, 'holdUntil must follow the final keyframe')

    if not isinstance(data, dict):
        return ['timeline must be an object'], []
    canvas = data.get('canvas')
    if not isinstance(canvas, dict):
        return ['canvas must be an object'], []
    for field in ('width', 'height', 'durationInFrames'):
        if not integer(canvas.get(field)) or canvas[field] <= 0:
            problem(f'canvas.{field}', 'must be a positive integer')
    fps = canvas.get('fps')
    if type(fps) not in (int, float) or not math.isfinite(fps) or fps <= 0:
        problem('canvas.fps', 'must be finite and positive')
    duration = canvas.get('durationInFrames')
    if not integer(duration) or duration <= 0:
        return errors, warnings
    if data.get('timeUnit') != 'frames':
        problem('timeUnit', 'must be frames')
    if not text(data.get('renderer')):
        problem('renderer', 'must name the chosen renderer')
    if not integer(data.get('version')) or data['version'] < 1:
        problem('version', 'must be a positive integer')

    scenes = objects(data.get('scenes'), 'scenes')
    scene_ids = unique(scenes, 'scenes')
    layers = objects(data.get('layers', []), 'layers')
    layer_ids = unique(layers, 'layers')
    valid_scenes, valid_layers, actions = {}, {}, []
    cursor = 0
    for i, scene in enumerate(scenes):
        where = f'scenes[{i}]'
        start, end = scene.get('start'), scene.get('end')
        start_ok = frame(start, where + '.start', 0, duration)
        end_ok = frame(end, where + '.end', 1, duration, exclusive=False)
        if not start_ok or not end_ok:
            continue
        if start != cursor:
            problem(where, f'gap, overlap, or out-of-order scene: expected start {cursor}, got {start}')
        if end <= start:
            problem(where, 'end must follow start')
            continue
        cursor = end
        if text(scene.get('id')):
            valid_scenes[scene['id']] = (start, end)
        track(scene.get('camera', []), where + '.camera', start, end)
        elements = objects(scene.get('elements', []), where + '.elements')
        unique(elements, where + '.elements')
        for j, element in enumerate(elements):
            location = f'{where}.elements[{j}]'
            if not text(element.get('target')):
                problem(location + '.target', 'must name a target')
            last = track(element.get('keyframes', []), location + '.keyframes', start, end)
            hold(element, location, start, end, last)
        hold(scene, where, start, end, start - 1)
        for j, action in enumerate(objects(scene.get('actions', []), where + '.actions')):
            location = f'{where}.actions[{j}]'
            if frame(action.get('frame'), location + '.frame', start, end):
                actions.append(action)
                if 'completeAt' in action:
                    frame(action['completeAt'], location + '.completeAt', action['frame'], duration)
            if action.get('type') not in ('click', 'tap', 'hover', 'type', 'scroll', 'drag', 'system'):
                problem(location + '.type', 'unknown action type')
            for field in ('target', 'result'):
                if not text(action.get(field)):
                    problem(location + '.' + field, 'must be a nonempty string')
    if not scenes or cursor != duration:
        problem('scenes', f'must cover every frame from 0 through {duration - 1}')

    for i, layer in enumerate(layers):
        where = f'layers[{i}]'
        start, end = layer.get('from'), layer.get('until')
        start_ok = frame(start, where + '.from', 0, duration)
        end_ok = frame(end, where + '.until', 1, duration, exclusive=False)
        if not text(layer.get('target')):
            problem(where + '.target', 'must name a target')
        if start_ok and end_ok:
            if end <= start:
                problem(where, 'until must follow from')
                continue
            if text(layer.get('id')):
                valid_layers[layer['id']] = (start, end)
            last = track(layer.get('keyframes', []), where + '.keyframes', start, end)
            track(layer.get('camera', []), where + '.camera', start, end)
            hold(layer, where, start, end, last)

    for i, transition in enumerate(objects(data.get('transitions', []), 'transitions')):
        where = f'transitions[{i}]'
        outgoing, incoming = transition.get('from'), transition.get('to')
        if not text(outgoing) or not text(incoming) or outgoing not in scene_ids or incoming not in scene_ids:
            problem(where, 'from and to must reference existing scenes')
            continue
        if outgoing not in valid_scenes or incoming not in valid_scenes:
            continue
        start, end = valid_scenes[outgoing]
        if end != valid_scenes[incoming][0]:
            problem(where, 'transition must connect adjacent scenes')
        overlap = transition.get('overlap')
        if not isinstance(overlap, list) or len(overlap) != 2 or not all(integer(v) for v in overlap):
            problem(where + '.overlap', 'must be [start, end] in integer frames')
            continue
        if not start <= overlap[0] <= overlap[1] == end:
            problem(where + '.overlap', 'must occupy the tail of the outgoing scene; cuts use [end, end]')
        owner = transition.get('owner')
        if owner is not None:
            if not text(owner) or owner not in layer_ids:
                problem(where + '.owner', 'must reference an existing layer ID')
            elif owner in valid_layers:
                a, b = valid_layers[owner]
                if a > overlap[0] or b < overlap[1]:
                    problem(where + '.owner', 'layer must cover the complete overlap')
        elif transition.get('type') == 'shared-object':
            problem(where + '.owner', 'shared-object transitions need an owner layer')
        if not text(transition.get('handoff')):
            problem(where + '.handoff', 'must explain continuity or the deliberate cut')

    for i, cue in enumerate(objects(data.get('audio', []), 'audio')):
        where = f'audio[{i}]'
        valid_frame = frame(cue.get('frame'), where + '.frame', 0, duration)
        if 'until' in cue and valid_frame:
            frame(cue['until'], where + '.until', cue['frame'] + 1, duration, exclusive=False)
        if cue.get('role') not in ('sfx', 'music', 'vo', 'bed'):
            problem(where + '.role', 'unknown audio role')
        sync = cue.get('sync', 'loose')
        if sync not in ('press', 'arrival', 'peak', 'completeAt', 'beat', 'loose'):
            problem(where + '.sync', 'unknown sync point')
        if sync in ('press', 'completeAt'):
            field = 'frame' if sync == 'press' else 'completeAt'
            matches = [a for a in actions if (sync != 'press' or a.get('type') in ('tap', 'click'))
                       and (not cue.get('target') or a.get('target') == cue['target'])
                       and integer(a.get(field)) and a[field] == cue.get('frame')]
            if not matches:
                problem(where, f'{sync} cue does not match an action on its target/frame')
        if cue.get('status') == 'open' or not text(cue.get('file')):
            warnings.append(f'{where}: audio source is unresolved')

    def unresolved(value, where='timeline'):
        if isinstance(value, dict):
            for key, item in value.items():
                if not key.startswith('$'):
                    unresolved(item, f'{where}.{key}')
        elif isinstance(value, list):
            for i, item in enumerate(value):
                unresolved(item, f'{where}[{i}]')
        elif isinstance(value, str) and value.startswith('proposed:'):
            warnings.append(f'{where}: proposed source or target needs verification')
    unresolved(data)
    open_items = data.get('open', [])
    if not isinstance(open_items, list) or any(not text(v) for v in open_items):
        problem('open', 'must be an array of nonempty strings')
    elif open_items:
        warnings.append(f'open: {len(open_items)} unresolved decision(s)')
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('timeline', type=Path)
    parser.add_argument('--require-resolved', action='store_true', help='Also fail on declared placeholders, open decisions, or missing audio sources.')
    args = parser.parse_args()
    try:
        data = json.loads(args.timeline.read_text())
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Could not read timeline: {exc}\n')
    errors, warnings = validate(data)
    passed = not errors and not (args.require_resolved and warnings)
    print(json.dumps({'valid': passed, 'errors': errors, 'warnings': warnings,
                      'limits': 'Structural checks only. Does not verify DOM targets, assets, renderer behavior, reading holds, or visual/audio quality.'}, indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == '__main__':
    main()
