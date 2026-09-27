#!/usr/bin/env python3
"""Create a local, timestamped video inventory and contact sheets; originals are read-only."""
import argparse
import hashlib
import io
import json
import math
import re
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
    parser.add_argument('--keep-ids', type=Path, metavar='MANIFEST',
                        help='Earlier manifest.json; reuse its IDs by path, then by file hash. New files get the next free IDs.')
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
    previous = []
    if args.keep_ids:
        try:
            previous = json.loads(args.keep_ids.read_text())
        except (OSError, ValueError) as exc:
            parser.error(f'Could not read --keep-ids manifest: {exc}')
        if not isinstance(previous, list):
            parser.error('--keep-ids manifest must be a list of video records.')
        seen_ids, seen_paths = set(), set()
        for record in previous:
            if not isinstance(record, dict):
                parser.error('--keep-ids manifest must contain video record objects.')
            record_id = record.get('id')
            if not isinstance(record_id, str) or not re.fullmatch(r'R[0-9]+', record_id):
                parser.error('--keep-ids records need an ID such as R01.')
            record_path = record.get('path')
            if not isinstance(record_path, str) or not record_path:
                parser.error('--keep-ids records need a nonempty path.')
            if record_id in seen_ids or record_path in seen_paths:
                parser.error('--keep-ids records must have unique IDs and paths.')
            for field in ('file', 'sha256'):
                if field in record and not isinstance(record[field], str):
                    parser.error(f'--keep-ids record {field} must be a string.')
            seen_ids.add(record_id)
            seen_paths.add(record_path)
    args.output.mkdir(parents=True, exist_ok=True)

    def sha256(path):
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
        return digest.hexdigest()

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        hashes = list(pool.map(sha256, files))

    # Stable IDs: reuse earlier IDs by resolved path, then by file hash; number new files after the highest known ID.
    by_path = {r.get('path'): r['id'] for r in previous if r.get('id')}
    by_hash = {}
    for r in previous:
        if r.get('id') and r.get('sha256'):
            by_hash.setdefault(r['sha256'], []).append((r.get('file'), r['id']))
    used = {r['id'] for r in previous if r.get('id')}
    next_number = max([int(i[1:]) for i in used if i[1:].isdigit()] or [0]) + 1
    ids = [by_path.get(str(path)) for path in files]          # pass 1: same file, same ID
    taken = {i for i in ids if i}
    for exact_name in (True, False):                             # pass 2: moved file, same bytes (same name first)
        for n, (path, digest) in enumerate(zip(files, hashes)):
            if ids[n] is not None:
                continue
            for name, known in by_hash.get(digest, []):
                if known not in taken and (name == path.name or not exact_name):
                    ids[n] = known
                    taken.add(known)
                    break
    for n in range(len(ids)):                                    # pass 3: genuinely new files
        if ids[n] is None:
            ids[n] = f'R{next_number:02}'
            next_number += 1
    first_seen = {}                                              # canonical copy = lowest ID among identical bytes
    for path_id, digest in sorted(zip(ids, hashes), key=lambda pair: (len(pair[0]), pair[0])):
        first_seen.setdefault(digest, path_id)

    def display_size(video):
        width, height = video['width'], video['height']
        rotation = 0
        for side in video.get('side_data_list', []):
            if 'rotation' in side:
                rotation = side['rotation']
        rotation = int(float(video.get('tags', {}).get('rotate', rotation) or 0))
        if rotation % 180:
            width, height = height, width
        return width, height, rotation % 360

    def inspect(item):
        index, path = item
        digest = hashes[index]
        record = {'id': ids[index], 'file': path.name, 'path': str(path), 'sha256': digest}
        if first_seen[digest] != ids[index]:
            record['duplicate_of'] = first_seen[digest]
        try:
            meta = json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)]))
            video = next(s for s in meta['streams'] if s['codec_type'] == 'video')
            duration = float(video.get('duration') or meta['format']['duration'])
            width, height, rotation = display_size(video)
            record.update(duration=duration, width=width, height=height, rotation=rotation, fps=video.get('avg_frame_rate'), audio=any(s['codec_type'] == 'audio' for s in meta['streams']))
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
                dup = f" | duplicate of {record['duplicate_of']}" if 'duplicate_of' in record else ''
                draw.text((10, 24), f"{duration:.2f}s | {width}x{height}{dup} | requested seek times; not continuous playback", fill='#b8c6d8')
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
        records = list(pool.map(inspect, enumerate(files)))
    (args.output / 'manifest.json').write_text(json.dumps(records, indent=2) + '\n')
    failures = [r for r in records if 'error' in r]
    duplicates = {r['id']: r['duplicate_of'] for r in records if 'duplicate_of' in r}
    print(json.dumps({'videos': len(records), 'unique': len(set(hashes)), 'duplicates': duplicates, 'failed': failures, 'manifest': str((args.output / 'manifest.json').resolve())}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
