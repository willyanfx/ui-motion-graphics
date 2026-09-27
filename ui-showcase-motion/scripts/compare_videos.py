#!/usr/bin/env python3
"""Make sampled reference/render pairs and diagnostic differences; never a quality gate."""
import argparse
import io
import json
import math
import shutil
import subprocess
from pathlib import Path

from video_metadata import display_size


def run(command):
    return subprocess.run(command, capture_output=True, check=True).stdout


def probe(path):
    data = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))
    video = next(s for s in data['streams'] if s['codec_type'] == 'video')
    width, height, rotation = display_size(video)
    return {'path': str(path.resolve()), 'duration': float(video.get('duration') or data['format']['duration']),
            'width': width, 'height': height, 'rotation': rotation, 'fps': video.get('avg_frame_rate')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reference', type=Path)
    parser.add_argument('render', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--fps', type=float, default=8, help='Requested samples/second, not output video FPS.')
    parser.add_argument('--reference-start', type=float, default=0)
    parser.add_argument('--render-start', type=float, default=0)
    parser.add_argument('--duration', type=float, help='Seconds to compare; defaults to common remaining duration.')
    args = parser.parse_args()
    for value in (args.fps, args.reference_start, args.render_start):
        if not math.isfinite(value):
            parser.error('FPS and start times must be finite.')
    if args.fps <= 0 or min(args.reference_start, args.render_start) < 0:
        parser.error('Use positive FPS and nonnegative start times.')
    if args.duration is not None and (not math.isfinite(args.duration) or args.duration <= 0):
        parser.error('Duration must be finite and positive.')
    if not args.reference.is_file() or not args.render.is_file():
        parser.error('Both input videos must exist.')
    if args.output.exists() and (not args.output.is_dir() or any(args.output.iterdir())):
        parser.error('Choose a new or empty output directory; existing review files will not be overwritten.')
    for tool in ('ffmpeg', 'ffprobe'):
        if not shutil.which(tool):
            parser.error(f'{tool} is required.')
    try:
        from PIL import Image, ImageChops, ImageDraw, ImageOps, ImageStat
    except ImportError:
        parser.error('Pillow is required.')

    def sample(path, time):
        raw = run(['ffmpeg', '-v', 'error', '-ss', str(time), '-i', str(path), '-frames:v', '1',
                   '-vf', 'scale=320:180:force_original_aspect_ratio=decrease', '-f', 'image2pipe',
                   '-vcodec', 'png', '-threads', '1', '-'])
        if not raw:
            raise ValueError(f'No video frame available at {time:.6f}s in {path.name}')
        return ImageOps.pad(Image.open(io.BytesIO(raw)).convert('RGB'), (320, 180), color='black')

    def difference(a, b):
        return ImageStat.Stat(ImageChops.difference(a.convert('L'), b.convert('L'))).mean[0]

    try:
        reference, render = probe(args.reference), probe(args.render)
        available_ref = reference['duration'] - args.reference_start
        available_render = render['duration'] - args.render_start
        common = min(available_ref, available_render)
        if common <= 0:
            raise ValueError('A start time is outside its video.')
        span = min(common, args.duration) if args.duration is not None else common
        # Keep requested samples safely before the end; report this guard rather than claiming full frame coverage.
        guard = min(.1, span / 2)
        times = [n / args.fps for n in range(math.ceil((span - guard) * args.fps))]
        times = [t for t in times if t < span - guard] or [0.0]
        args.output.mkdir(parents=True, exist_ok=True)
        rows, pages, changes = [], [], []
        previous = None
        sheet = None
        for i, time in enumerate(times):
            a = sample(args.reference, args.reference_start + time)
            b = sample(args.render, args.render_start + time)
            score = difference(a, b)
            row = {'relative_seconds': time, 'reference_seconds': args.reference_start + time,
                   'render_seconds': args.render_start + time, 'mean_luma_difference_0_255': score}
            rows.append(row)
            if previous is not None:
                changes.append({'from_seconds': args.render_start + times[i - 1],
                                'to_seconds': args.render_start + time,
                                'mean_luma_change_0_255': difference(previous, b)})
            previous = b
            if i % 6 == 0:
                count = min(6, len(times) - i)
                sheet = Image.new('RGB', (640, 40 + count * 208), '#131820')
                draw = ImageDraw.Draw(sheet)
                draw.text((10, 10), 'REFERENCE', fill='#a8dcff')
                draw.text((330, 10), 'RENDER / requested seek times', fill='#ffc0a8')
            y = 40 + (i % 6) * 208
            sheet.paste(a, (0, y))
            sheet.paste(b, (320, y))
            draw.text((8, y + 184), f"{row['reference_seconds']:.3f}s", fill='white')
            draw.text((328, y + 184), f"{row['render_seconds']:.3f}s | luma diff {score:.2f}", fill='white')
            if i % 6 == 5 or i == len(times) - 1:
                name = f'pairs-{len(pages) + 1:03}.jpg'
                sheet.save(args.output / name, quality=90)
                pages.append(name)
        report = {
            'status': 'diagnostics_only_not_visually_reviewed',
            'reference': reference, 'render': render,
            'reference_start': args.reference_start, 'render_start': args.render_start,
            'sampling_fps': args.fps, 'timestamp_basis': 'requested_seek',
            'requested_duration': args.duration, 'common_available_seconds': common,
            'compared_window_seconds': span, 'end_guard_seconds': guard,
            'requested_window_truncated': args.duration is not None and args.duration > common,
            'render_minus_reference_duration_seconds': render['duration'] - reference['duration'],
            'uncompared_reference_tail_seconds': max(0, available_ref - span),
            'uncompared_render_tail_seconds': max(0, available_render - span),
            'dimensions_match': (reference['width'], reference['height']) == (render['width'], render['height']),
            'sample_count': len(rows), 'pairs': pages,
            'mean_luma_difference_0_255': sum(r['mean_luma_difference_0_255'] for r in rows) / len(rows),
            'largest_differences': sorted(rows, key=lambda r: r['mean_luma_difference_0_255'], reverse=True)[:12],
            'largest_render_changes': sorted(changes, key=lambda r: r['mean_luma_change_0_255'], reverse=True)[:12],
            'samples': rows,
            'limits': 'Sampled grayscale/padded comparison. Cuts and fast moves can create large changes. No audio, continuous-playback, or full-resolution mechanics review.'
        }
        (args.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps({'report': str((args.output / 'report.json').resolve()), 'samples': len(rows),
                          'mean_luma_difference': report['mean_luma_difference_0_255'],
                          'duration_difference_seconds': report['render_minus_reference_duration_seconds'],
                          'status': report['status']}, indent=2))
    except (subprocess.CalledProcessError, ValueError, KeyError, StopIteration, OSError) as exc:
        parser.exit(1, f'Inspection failed: {exc}\n')


if __name__ == '__main__':
    main()
