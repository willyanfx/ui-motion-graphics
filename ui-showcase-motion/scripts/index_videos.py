#!/usr/bin/env python3
"""Create a local, timestamped video inventory and contact sheets; originals are read-only."""
import argparse
import hashlib
import io
import json
import math
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def run(args):
    return subprocess.run(args, check=True, capture_output=True).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    sampling = parser.add_mutually_exclusive_group()
    sampling.add_argument('--samples', type=int, default=12)
    sampling.add_argument('--fps', type=float, help='Requested samples per second for dense review.')
    parser.add_argument('--per-sheet', type=int, default=24)
    parser.add_argument('--start', type=float, default=0)
    parser.add_argument('--end', type=float)
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args()
    if args.samples < 2 or args.workers < 1 or args.per_sheet < 1 or not math.isfinite(args.start) or args.start < 0:
        parser.error('Use at least two overview samples, positive workers/page size, and a finite nonnegative start.')
    if args.fps is not None and (not math.isfinite(args.fps) or args.fps <= 0):
        parser.error('Sampling FPS must be finite and positive.')
    if args.end is not None and (not math.isfinite(args.end) or args.end <= args.start):
        parser.error('End must be finite and greater than start.')
    for tool in ('ffmpeg', 'ffprobe'):
        if not shutil.which(tool):
            parser.error(f'{tool} is required; install it or use another video inspection tool.')
    try:
        from PIL import Image, ImageDraw, ImageOps
    except ImportError:
        parser.error('Pillow is required by this helper.')
    source = args.source.resolve()
    if not source.exists():
        parser.error('Source does not exist.')
    files = [source] if source.is_file() else sorted(p for p in source.rglob('*') if p.suffix.lower() in {'.mp4', '.mov', '.webm', '.m4v'})
    if not files:
        parser.error('No supported videos found.')
    args.output.mkdir(parents=True, exist_ok=True)

    def inspect(item):
        index, path = item
        record = {'id': f'R{index:02}', 'file': path.name, 'path': str(path)}
        try:
            digest = hashlib.sha256()
            with path.open('rb') as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    digest.update(chunk)
            record['sha256'] = digest.hexdigest()
            meta = json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)]))
            video = next(s for s in meta['streams'] if s['codec_type'] == 'video')
            duration = float(video.get('duration') or meta['format']['duration'])
            record.update(duration=duration, width=video['width'], height=video['height'], fps=video.get('avg_frame_rate'), audio=any(s['codec_type'] == 'audio' for s in meta['streams']))
            end = min(args.end if args.end is not None else duration, duration - min(.1, duration / 2))
            if args.start >= end:
                raise ValueError('Requested sampling interval is outside the video.')
            if args.fps is not None:
                times = [args.start + n / args.fps for n in range(math.ceil((end - args.start) * args.fps))]
                times = [t for t in times if t < end]
            else:
                times = [args.start + (end - args.start) * n / (args.samples - 1) for n in range(args.samples)]
            cols, cell_w, cell_h = 4, 320, 204
            sheets = []
            for offset in range(0, len(times), args.per_sheet):
                page_times = times[offset:offset + args.per_sheet]
                page = len(sheets) + 1
                sheet = Image.new('RGB', (cols * cell_w, 42 + math.ceil(len(page_times) / cols) * cell_h), '#141820')
                draw = ImageDraw.Draw(sheet)
                draw.text((10, 8), f"{record['id']} | page {page} | {path.name[:100]}", fill='white')
                draw.text((10, 24), f"{duration:.2f}s | {video['width']}x{video['height']} | requested seek times; not continuous playback", fill='#b8c6d8')
                for n, time in enumerate(page_times):
                    raw = run(['ffmpeg', '-v', 'error', '-ss', str(time), '-i', str(path), '-frames:v', '1', '-vf', 'scale=320:180:force_original_aspect_ratio=decrease', '-f', 'image2pipe', '-vcodec', 'png', '-threads', '1', '-'])
                    frame = Image.open(io.BytesIO(raw)).convert('RGB')
                    frame = ImageOps.pad(frame, (320, 180), color='#07090d')
                    x, y = n % cols * cell_w, 42 + n // cols * cell_h
                    sheet.paste(frame, (x, y))
                    draw.text((x + 8, y + 184), f'{time:.3f}s', fill='white')
                suffix = f'-p{page:03}' if len(times) > args.per_sheet else ''
                sheet_name = f"{record['id']}-{path.stem[:60]}{suffix}.jpg"
                sheet.save(args.output / sheet_name, quality=85)
                sheets.append({'file': sheet_name, 'samples': page_times})
            record.update(samples=times, sheets=sheets, sheet=sheets[0]['file'], sampling_fps=args.fps, timestamp_basis='requested_seek', review_status='sampled_not_visually_reviewed')
        except Exception as exc:
            record.update(error=str(exc), review_status='failed')
        return record

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        records = list(pool.map(inspect, enumerate(files, 1)))
    (args.output / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')
    failures = [r for r in records if 'error' in r]
    print(json.dumps({'videos': len(records), 'failed': failures, 'manifest': str((args.output / 'manifest.json').resolve())}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
