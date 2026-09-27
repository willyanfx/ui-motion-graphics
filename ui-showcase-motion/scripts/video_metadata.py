"""Shared metadata conventions for the local video inspection helpers."""
import json
import re


def read_id_records(path):
    """Read current manifests or cumulative registries without trusting labels as filenames."""
    records = json.loads(path.read_text())
    if not isinstance(records, list):
        raise ValueError('ID manifest must be a list of video records.')
    ids, paths = set(), set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError('ID manifest must contain video record objects.')
        label, source = record.get('id'), record.get('path')
        if not isinstance(label, str) or not re.fullmatch(r'R[0-9]+', label):
            raise ValueError('Each record needs an ID such as R01.')
        if not isinstance(source, str) or not source:
            raise ValueError('Each record needs a nonempty path.')
        if label in ids or source in paths:
            raise ValueError('IDs and paths must be unique.')
        for field in ('file', 'sha256'):
            if field in record and not isinstance(record[field], str):
                raise ValueError(f'Record {field} must be a string.')
        ids.add(label)
        paths.add(source)
    return records


def display_size(video):
    """Return display dimensions after the quarter-turn metadata FFmpeg autorotates."""
    width, height = video['width'], video['height']
    rotation = 0
    for side in video.get('side_data_list', []):
        if 'rotation' in side:
            rotation = side['rotation']
    rotation = int(float(video.get('tags', {}).get('rotate', rotation) or 0)) % 360
    if rotation % 180:
        width, height = height, width
    return width, height, rotation
