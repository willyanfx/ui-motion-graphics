#!/usr/bin/env python3
"""Regression checks for UI Showcase Motion. All generated media stays in a temporary directory."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from validate_timeline import validate
from video_metadata import read_id_records


def run(*args, success=True):
    result = subprocess.run([str(a) for a in args], capture_output=True, text=True)
    if success and result.returncode:
        raise AssertionError(result.stderr or result.stdout)
    return result


def helper(name, *args, success=True):
    return run(sys.executable, SCRIPTS / name, *args, success=success)


class TimelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.example = json.loads((ROOT / 'assets/timeline.example.json').read_text())

    def test_complete_example_and_declared_unknowns(self):
        errors, warnings = validate(self.example)
        self.assertEqual(errors, [])
        self.assertTrue(warnings)
        result = helper('validate_timeline.py', ROOT / 'assets/timeline.example.json', '--require-resolved', success=False)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)['valid'])

    def test_minimal_resolved_contract_and_extensions(self):
        data = {'version': 2, 'renderer': 'custom', 'timeUnit': 'frames',
                'canvas': {'width': 320, 'height': 180, 'fps': 29.97, 'durationInFrames': 30},
                'scenes': [{'id': 'S1', 'start': 0, 'end': 30, 'customField': {'x': 3}}]}
        self.assertEqual(validate(data), ([], []))

    def test_structural_failures(self):
        cases = [
            ('missing scene', lambda d: d['scenes'].pop(2)),
            ('gap', lambda d: d['scenes'][1].update(start=85)),
            ('overlap', lambda d: d['scenes'][1].update(start=83)),
            ('duplicate scene', lambda d: d['scenes'][1].update(id='S1-hook')),
            ('duplicate layer', lambda d: d['layers'].append(copy.deepcopy(d['layers'][0]))),
            ('duplicate element', lambda d: d['scenes'][0]['elements'].append(copy.deepcopy(d['scenes'][0]['elements'][0]))),
            ('negative duration', lambda d: d['canvas'].update(durationInFrames=-1)),
            ('boolean fps', lambda d: d['canvas'].update(fps=True)),
            ('nonfinite fps', lambda d: d['canvas'].update(fps=float('nan'))),
            ('noninteger frame', lambda d: d['scenes'][0].update(start=0.5)),
            ('outside keyframe', lambda d: d['scenes'][0]['elements'][0]['keyframes'][-1].update(frame=84)),
            ('backward keyframe', lambda d: d['scenes'][0]['elements'][0]['keyframes'][2].update(frame=10)),
            ('duplicate keyframe', lambda d: d['scenes'][0]['elements'][0]['keyframes'][2].update(frame=15)),
            ('short hold', lambda d: d['scenes'][1]['elements'][2].update(holdUntil=150)),
            ('camera outside scene', lambda d: d['scenes'][1]['camera'][0].update(frame=83)),
            ('action outside scene', lambda d: d['scenes'][1]['actions'][0].update(frame=189)),
            ('action completion before cause', lambda d: d['scenes'][1]['actions'][0].update(completeAt=129)),
            ('action type', lambda d: d['scenes'][1]['actions'][0].update(type='teleport')),
            ('missing transition scene', lambda d: d['transitions'][0].update(to='missing')),
            ('wrong overlap', lambda d: d['transitions'][0].update(overlap=[69, 85])),
            ('missing owner', lambda d: d['transitions'][-1].update(owner='missing')),
            ('shared object without owner', lambda d: d['transitions'][-1].update(type='shared-object', owner=None)),
            ('owner starts late', lambda d: d['layers'][1].update(**{'from': 334})),
            ('audio out of bounds', lambda d: d['audio'][0].update(frame=450)),
            ('audio ends early', lambda d: d['audio'][0].update(until=129)),
            ('audio action mismatch', lambda d: d['audio'][0].update(frame=131)),
            ('audio target mismatch', lambda d: d['audio'][0].update(target='another-button')),
            ('layer keyframe outside lifetime', lambda d: d['layers'][1]['keyframes'][0].update(frame=332)),
        ]
        for label, mutate in cases:
            with self.subTest(label=label):
                data = copy.deepcopy(self.example)
                mutate(data)
                self.assertTrue(validate(data)[0])

    def test_claims_bind_figures_in_copy(self):
        def outcome(mutate):
            data = copy.deepcopy(self.example)
            mutate(data)
            return validate(data)
        benefit = lambda d: d['scenes'][4]['elements'][0]
        claim = lambda d: d['claims'][0]
        verify = lambda d: claim(d).update(status='verified', source='feed export', checked='2026-09-28')
        self.assertIn('claims[0]: claim needs a checked source', validate(self.example)[1])
        errors, warnings = outcome(verify)
        self.assertEqual(errors, [])
        self.assertFalse([w for w in warnings if 'claim' in w])
        errors, warnings = outcome(lambda d: (verify(d), benefit(d).update(target="copy:'24 new arrivals, one tap.'")))
        self.assertEqual(errors, [])
        self.assertTrue(any('literal figure' in w for w in warnings))
        vo = {'frame': 280, 'cue': 'benefit', 'role': 'vo', 'text': 'Twenty-four new, 7 days a week', 'file': 'vo.wav'}
        self.assertTrue(any('audio[2].text' in w and 'literal figure' in w
                            for w in outcome(lambda d: d['audio'].append(vo))[1]))
        for label, mutate in [
            ('unknown placeholder', lambda d: benefit(d).update(target="copy:'{claim:missing} new'")),
            ('unknown claim target', lambda d: benefit(d).update(target='claim:missing')),
            ('duplicate claim', lambda d: d['claims'].append(copy.deepcopy(claim(d)))),
            ('missing value', lambda d: claim(d).pop('value')),
            ('unknown status', lambda d: claim(d).update(status='approved')),
        ]:
            with self.subTest(label=label):
                self.assertTrue(outcome(mutate)[0])

    def test_malformed_containers_report_errors(self):
        for field, value in [('canvas', []), ('scenes', {}), ('scenes', [None]), ('layers', [None]),
                             ('transitions', [None]), ('audio', [False]), ('open', {}), ('renderer', []),
                             ('claims', {}), ('claims', [None])]:
            with self.subTest(field=field, value=value):
                data = copy.deepcopy(self.example)
                data[field] = value
                self.assertTrue(validate(data)[0])
        self.assertTrue(validate(None)[0])


@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe') and importlib.util.find_spec('PIL'),
                     'FFmpeg, FFprobe and Pillow required for media tests')
class MediaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='ui-motion-regressions-')
        cls.base = Path(cls.temp.name).resolve()
        for name, color, frequency in [('red', 'red', 440), ('blue', 'blue', 880), ('green', 'green', 660)]:
            run('ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', f'color=c={color}:s=160x90:r=30:d=1',
                '-f', 'lavfi', '-i', f'sine=frequency={frequency}:duration=1',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', cls.base / f'{name}.mp4')
        run('ffmpeg', '-v', 'error', '-display_rotation', '90', '-i', cls.base / 'red.mp4',
            '-c', 'copy', cls.base / 'rotated.mp4')
        run('ffmpeg', '-v', 'error', '-i', cls.base / 'rotated.mp4', '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p', '-an', cls.base / 'baked.mp4')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        self.work = Path(tempfile.mkdtemp(dir=self.base))

    def records(self, out):
        return json.loads((out / 'manifest.json').read_text())

    def index(self, source, out, previous=None, *extra):
        args = ['--samples', '2', *extra]
        if previous:
            args.extend(['--keep-ids', previous])
        helper('index_videos.py', source, out, *args)
        return {r['file']: r['id'] for r in self.records(out)}

    def test_audio_same_and_truncated_names_keep_distinct_sheets(self):
        source = self.work / 'source'
        for folder, stem, fixture in [('a', 'clip', 'red'), ('b', 'clip', 'blue'),
                                     ('c', 'x' * 45 + '-one', 'red'), ('d', 'x' * 45 + '-two', 'green')]:
            dest = source / folder / f'{stem}.mp4'
            dest.parent.mkdir(parents=True)
            shutil.copy2(self.base / f'{fixture}.mp4', dest)
        out = self.work / 'audio'
        helper('audio_events.py', source, out, '--top', '0')
        data = json.loads((out / 'audio.json').read_text())
        self.assertEqual(len(data), 4)
        self.assertEqual(len({r['sheet'] for r in data}), 4)
        self.assertEqual(len(list(out.glob('*.png'))), 4)
        self.assertNotEqual((out / data[0]['sheet']).read_bytes(), (out / data[1]['sheet']).read_bytes())

    def test_id_history_survives_removal_subset_and_restoration(self):
        source = self.work / 'source'
        source.mkdir()
        shutil.copy2(self.base / 'red.mp4', source / 'a.mp4')
        shutil.copy2(self.base / 'blue.mp4', source / 'b.mp4')
        self.assertEqual(self.index(source, self.work / 'one'), {'a.mp4': 'R01', 'b.mp4': 'R02'})
        (source / 'b.mp4').rename(self.work / 'absent.mp4')
        self.assertEqual(self.index(source, self.work / 'two', self.work / 'one/manifest.json'), {'a.mp4': 'R01'})
        shutil.copy2(self.base / 'green.mp4', source / 'c.mp4')
        self.assertEqual(self.index(source, self.work / 'three', self.work / 'two/manifest.json'), {'a.mp4': 'R01', 'c.mp4': 'R03'})
        self.assertEqual(self.index(source / 'c.mp4', self.work / 'subset', self.work / 'three/manifest.json'), {'c.mp4': 'R03'})
        (self.work / 'absent.mp4').rename(source / 'restored.mp4')
        (source / 'a.mp4').rename(source / 'moved.mp4')
        final = self.index(source, self.work / 'four', self.work / 'subset/id-registry.json')
        self.assertEqual(final, {'moved.mp4': 'R01', 'restored.mp4': 'R02', 'c.mp4': 'R03'})

    def test_legacy_ids_duplicates_and_audio_mapping(self):
        source = self.work / 'source'
        source.mkdir()
        shutil.copy2(self.base / 'red.mp4', source / 'a.mp4')
        shutil.copy2(self.base / 'red.mp4', source / 'b.mp4')
        legacy = self.work / 'legacy.json'
        legacy.write_text(json.dumps([{'id': 'R12', 'path': str(source / 'a.mp4')}]))
        self.assertEqual(self.index(source, self.work / 'out', legacy), {'a.mp4': 'R12', 'b.mp4': 'R13'})
        self.assertEqual(self.records(self.work / 'out')[1]['duplicate_of'], 'R12')
        helper('audio_events.py', source, self.work / 'audio', '--ids', self.work / 'out/manifest.json', '--top', '0')
        audio = json.loads((self.work / 'audio/audio.json').read_text())
        self.assertEqual([r['sheet'] for r in audio], ['R12-audio.png', 'R13-audio.png'])

    def test_rotated_display_comparison_and_identity(self):
        helper('compare_videos.py', self.base / 'red.mp4', self.base / 'rotated.mp4', self.work / 'different', '--fps', '2')
        report = json.loads((self.work / 'different/report.json').read_text())
        self.assertFalse(report['dimensions_match'])
        self.assertEqual((report['render']['width'], report['render']['height']), (90, 160))
        self.index(self.base / 'rotated.mp4', self.work / 'index')
        record = self.records(self.work / 'index')[0]
        self.assertEqual((record['width'], record['height']), (90, 160))
        helper('compare_videos.py', self.base / 'rotated.mp4', self.base / 'baked.mp4', self.work / 'same', '--fps', '2')
        report = json.loads((self.work / 'same/report.json').read_text())
        self.assertTrue(report['dimensions_match'])
        self.assertLess(report['mean_luma_difference_0_255'], 1)
        helper('compare_videos.py', self.base / 'red.mp4', self.base / 'red.mp4', self.work / 'identity', '--fps', '2')
        self.assertEqual(json.loads((self.work / 'identity/report.json').read_text())['mean_luma_difference_0_255'], 0)

    def test_invalid_ids_fail_before_writing(self):
        malformed = [{}, [None], [{'id': '../escape', 'path': '/clip'}],
                     [{'id': 'R01', 'path': '/a'}, {'id': 'R01', 'path': '/b'}],
                     [{'id': 'R01', 'path': '/a'}, {'id': 'R02', 'path': '/a'}]]
        for i, value in enumerate(malformed):
            path = self.work / f'bad-{i}.json'
            path.write_text(json.dumps(value))
            with self.subTest(case=i):
                with self.assertRaises(ValueError):
                    read_id_records(path)
                for name, flag in [('index_videos.py', '--keep-ids'), ('audio_events.py', '--ids')]:
                    out = self.work / f'{name}-{i}'
                    result = helper(name, self.base / 'red.mp4', out, flag, path, success=False)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertNotIn('Traceback', result.stderr)
                    self.assertFalse(out.exists())

    def test_existing_outputs_are_preserved(self):
        out = self.work / 'existing'
        out.mkdir()
        marker = out / 'keep.txt'
        marker.write_text('unchanged')
        for name in ('index_videos.py', 'audio_events.py', 'compare_videos.py'):
            inputs = [self.base / 'red.mp4'] * (2 if name == 'compare_videos.py' else 1)
            result = helper(name, *inputs, out, success=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(marker.read_text(), 'unchanged')
            self.assertEqual(list(out.iterdir()), [marker])


if __name__ == '__main__':
    unittest.main(verbosity=2)
