#!/usr/bin/env python3
"""Map a video's sound to its picture: hit and swell candidates, band energy, loudness, tempo, picture-change sync, and the frame at each hit.

Candidates, not classifications: a spike in a frequency band is evidence of a sound event, not proof of what made it.
"""
import argparse
import bisect
import hashlib
import io
import json
import math
import re
import shutil
import subprocess
from array import array
from pathlib import Path

from video_metadata import read_id_records

RATE = 16000
BANDS = {  # approximate 2-pole splits; enough to tell a thump from a click, not a spectral analysis
    'low': 'lowpass=f=150',
    'mid': 'highpass=f=150,lowpass=f=4000',
    'high': 'highpass=f=4000',
}
COLORS = {'low': '#5b8def', 'mid': '#f2c14e', 'high': '#ef6f6c', 'full': '#d9dee7'}
FLOOR = -90.0


def run(args, stderr=False):
    result = subprocess.run(args, check=True, capture_output=True)
    return result.stderr.decode(errors='replace') if stderr else result.stdout


def probe(path):
    meta = json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))
    video = next((s for s in meta['streams'] if s['codec_type'] == 'video'), None)
    audio = next((s for s in meta['streams'] if s['codec_type'] == 'audio'), None)
    duration = float((video or audio or {}).get('duration') or meta['format']['duration'])
    offset = 0.0
    if video and audio:  # audio that starts after the video would shift every onset
        offset = max(0.0, float(audio.get('start_time') or 0) - float(video.get('start_time') or 0))
    return {'duration': duration, 'has_video': video is not None, 'has_audio': audio is not None, 'audio_offset': offset}


def envelope(path, start, length, chain, hop):
    raw = run(['ffmpeg', '-v', 'error', '-ss', str(start), '-t', str(length), '-i', str(path), '-vn', '-ac', '1',
               '-ar', str(RATE), '-af', chain, '-f', 's16le', '-'])
    samples = array('h')
    samples.frombytes(raw[:len(raw) - len(raw) % 2])
    step, window = int(RATE * hop), int(RATE * hop * 2)
    out = []
    for i in range(0, max(0, len(samples) - step + 1), step):
        chunk = samples[i:i + window]
        power = sum(v * v for v in chunk) / len(chunk)
        out.append(max(FLOOR, 10 * math.log10(power / 32768 ** 2)) if power else FLOOR)
    return out


def loudness(path, start, length):
    text = run(['ffmpeg', '-hide_banner', '-nostats', '-ss', str(start), '-t', str(length), '-i', str(path), '-vn',
                '-af', 'ebur128=peak=true', '-f', 'null', '-'], stderr=True)
    summary = text[text.rfind('Summary:'):]

    def grab(pattern):
        found = re.findall(pattern, summary)
        return float(found[-1]) if found else None
    return {'integrated_lufs': grab(r'I:\s+(-?[\d.]+) LUFS'), 'range_lu': grab(r'LRA:\s+(-?[\d.]+) LU'),
            'true_peak_dbfs': grab(r'Peak:\s+(-?[\d.]+) dBFS')}


def visual_changes(path, start, length, fps=30, side=(64, 36)):
    """Picture-change candidates (cuts, big moves) from low-res grayscale frame differences on a fixed fps grid."""
    raw = run(['ffmpeg', '-v', 'error', '-ss', str(start), '-t', str(length), '-i', str(path), '-an',
               '-vf', f'fps={fps},scale={side[0]}:{side[1]},format=gray', '-f', 'rawvideo', '-'])
    size = side[0] * side[1]
    frames = [raw[i:i + size] for i in range(0, len(raw) - size + 1, size)]
    diffs = [0.0] + [sum(abs(a - b) for a, b in zip(frames[i], frames[i - 1])) / size for i in range(1, len(frames))]
    events = []
    for n in range(1, len(diffs)):
        near = sorted(diffs[max(1, n - fps):n + fps + 1])
        if diffs[n] >= max(6, 3 * near[len(near) // 2]) and diffs[n] == max(diffs[max(1, n - 3):n + 4]):
            events.append({'seconds': round(start + n / fps, 3), 'change': round(diffs[n], 1)})
    return events


def tempo(novelty, hop):
    """Beat-period candidate from the autocorrelation of onset strength, searched between 60 and 180 BPM."""
    lo, hi = round(0.333 / hop), round(1.0 / hop)
    n = len(novelty)
    if n < hi * 3 or max(novelty) == 0:
        return None
    scores = {lag: sum(novelty[t] * novelty[t - lag] for t in range(lag, n)) / (n - lag) for lag in range(lo, hi + 1)}
    best = max(scores, key=scores.get)
    mean = sum(scores.values()) / len(scores)
    return {'bpm': round(60 / (best * hop), 1), 'confidence': round(scores[best] / mean, 2) if mean else 0,
            'note': 'strong if confidence >= 1.3; may be half or double the felt tempo'}


def smooth(values, radius):
    out, total, width = [], 0.0, 2 * radius + 1
    padded = [values[0]] * radius + values + [values[-1]] * radius
    for i, v in enumerate(padded):
        total += v
        if i >= width:
            total -= padded[i - width]
        if i >= width - 1:
            out.append(total / width)
    return out


def detect(bands, full, hop, min_rise, level_floor):
    n = len(full)
    # Onsets: a band jumps min_rise dB above its level 20-40 ms earlier, and it's the strongest jump within 50 ms.
    rise = [0.0] * n
    lead = [None] * n
    for name, env in bands.items():
        for t in range(4, n):
            r = env[t] - (env[t - 2] + env[t - 3] + env[t - 4]) / 3
            if env[t] > level_floor and r > rise[t]:
                rise[t], lead[t] = r, name
    reach, gap = max(1, round(0.05 / hop)), max(1, round(0.08 / hop))
    onsets, last = [], -gap
    for t in range(n):
        if rise[t] < min_rise or rise[t] < max(rise[max(0, t - reach):t + reach + 1]):
            continue
        if t - last < gap:
            if onsets and rise[t] > onsets[-1]['rise_db']:
                onsets.pop()
            else:
                continue
        peak = max(full[t:t + max(1, round(0.1 / hop))])
        tail = next((k for k in range(t, min(n, t + round(2 / hop))) if full[k] < peak - 12), min(n, t + round(2 / hop)))
        tail_ms = round((tail - t) * hop * 1000)
        band = lead[t]
        hint = ('tick/click' if band == 'high' and tail_ms < 150 else
                'thump/impact' if band == 'low' else
                'hit with tail' if tail_ms >= 300 else 'short hit')
        onsets.append({'index': t, 'rise_db': round(rise[t], 1), 'band': band, 'peak_dbfs': round(peak, 1),
                       'tail_ms': tail_ms, 'hint': hint})
        last = t
    # Swells: smoothed level climbs >= 9 dB over 0.25-2.5 s into a local peak (whoosh when short, riser when long).
    level = smooth(full, max(1, round(0.05 / hop)))
    swells, peak_reach = [], max(1, round(0.15 / hop))
    for t in range(n):
        if level[t] < max(level[max(0, t - peak_reach):t + peak_reach + 1]) or level[t] < level_floor:
            continue
        back = level[max(0, t - round(2.5 / hop)):t + 1]
        low_at = max(0, t - round(2.5 / hop)) + back.index(min(back))
        span = (t - low_at) * hop
        if level[t] - level[low_at] >= 9 and span >= 0.25:
            if swells and low_at <= swells[-1]['peak_index']:
                if level[t] - level[low_at] <= swells[-1]['rise_db']:
                    continue
                swells.pop()
            swells.append({'start_index': low_at, 'peak_index': t, 'rise_db': round(level[t] - level[low_at], 1),
                           'hint': 'whoosh' if span < 0.7 else 'riser'})
    silences, run_start = [], None
    for t, v in enumerate(full + [0.0]):
        if v < -50 and run_start is None:
            run_start = t
        elif v >= -50 and run_start is not None:
            if (t - run_start) * hop >= 0.25:
                silences.append((run_start, t))
            run_start = None
    return onsets, swells, silences, rise


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('source', type=Path, help='A video file or a folder of videos.')
    parser.add_argument('output', type=Path, help='New or empty folder for audio.json and the sheets.')
    parser.add_argument('--start', type=float, default=0)
    parser.add_argument('--end', type=float)
    parser.add_argument('--top', type=int, default=12, help='Strongest hits shown as frames (default 12).')
    parser.add_argument('--min-rise', type=float, default=6, help='dB jump that counts as a hit (default 6).')
    parser.add_argument('--hop-ms', type=float, default=10, help='Analysis step in ms (default 10).')
    parser.add_argument('--ids', type=Path, metavar='MANIFEST', help='index_videos.py manifest.json, to label clips by ID.')
    args = parser.parse_args()
    if not all(math.isfinite(v) for v in (args.start, args.min_rise, args.hop_ms)) or args.start < 0:
        parser.error('Start, min-rise, and hop must be finite; start must be nonnegative.')
    if args.end is not None and (not math.isfinite(args.end) or args.end <= args.start):
        parser.error('End must be finite and greater than start.')
    if args.top < 0 or args.min_rise <= 0 or not 2 <= args.hop_ms <= 50:
        parser.error('Use --top >= 0, a positive --min-rise, and --hop-ms between 2 and 50.')
    for tool in ('ffmpeg', 'ffprobe'):
        if not shutil.which(tool):
            parser.error(f'{tool} is required.')
    try:
        from PIL import Image, ImageDraw, ImageOps
    except ImportError:
        parser.error('Pillow is required.')
    source = args.source.resolve()
    if not source.exists():
        parser.error('Source does not exist.')
    files = [source] if source.is_file() else sorted(p for p in source.rglob('*') if p.suffix.lower() in {'.mp4', '.mov', '.webm', '.m4v'})
    if not files:
        parser.error('No supported videos found.')
    if args.output.exists() and (not args.output.is_dir() or any(args.output.iterdir())):
        parser.error('Choose a new or empty output directory; earlier results will not be mixed or overwritten.')
    ids = {}
    if args.ids:
        try:
            ids = {r['path']: r['id'] for r in read_id_records(args.ids)}
        except (OSError, ValueError, TypeError) as exc:
            parser.error(f'Could not read --ids manifest: {exc}')
    args.output.mkdir(parents=True, exist_ok=True)
    hop = args.hop_ms / 1000
    records = []

    for path in files:
        # Include the resolved path in fallback IDs: equal stems (including truncated
        # long names) must never share a sheet. Manifest IDs are validated above.
        stem = re.sub(r'[^A-Za-z0-9_-]+', '-', path.stem)[:40].strip('-') or 'clip'
        digest = hashlib.sha256(str(path).encode()).hexdigest()
        label = ids.get(str(path), f'{stem}-{digest}')
        record = {'id': label, 'file': path.name, 'path': str(path)}
        try:
            info = probe(path)
            record.update(duration=info['duration'], audio=info['has_audio'])
            if not info['has_audio']:
                record['note'] = 'no audio stream'
                records.append(record)
                continue
            end = min(args.end if args.end is not None else info['duration'], info['duration'])
            if args.start >= end:
                raise ValueError('Requested window is outside the video.')
            length = end - args.start
            lead_in = max(0.0, info['audio_offset'] - args.start)  # silence before the first audio sample
            bands = {name: envelope(path, args.start, length, chain, hop) for name, chain in BANDS.items()}
            full = envelope(path, args.start, length, 'anull', hop)
            n = min(len(full), *(len(b) for b in bands.values()))
            full, bands = full[:n], {k: v[:n] for k, v in bands.items()}
            if n < 10:
                raise ValueError('Too little audio in the window to analyze.')
            onsets, swells, silences, novelty = detect(bands, full, hop, args.min_rise, -55)

            def at(index):
                return round(args.start + lead_in + index * hop, 3)
            for o in onsets:
                o['seconds'] = at(o.pop('index'))
            for s in swells:
                s['start_seconds'], s['peak_seconds'] = at(s.pop('start_index')), at(s.pop('peak_index'))
            record.update(
                window=[args.start, end], hop_ms=args.hop_ms, audio_offset_s=info['audio_offset'],
                loudness=loudness(path, args.start, length),
                silent=all(v < -60 for v in full),
                band_mean_dbfs={k: round(sum(v) / n, 1) for k, v in bands.items()},
                onsets=onsets, swells=swells,
                silences=[[at(a), at(b)] for a, b in silences],
                tempo=tempo([min(r, 30) for r in novelty], hop),
                timestamp_basis='audio analysis step; frames are requested seeks, so pair them within about one video frame',
                review_status='candidates_not_auditioned')

            if info['has_video']:
                changes = visual_changes(path, args.start, length)
                window_s = 0.067  # two frames at 30 fps
                pairs = []
                for c in changes:
                    near = min(onsets, key=lambda o: abs(o['seconds'] - c['seconds']), default=None)
                    if near and abs(near['seconds'] - c['seconds']) <= window_s:
                        pairs.append(round((near['seconds'] - c['seconds']) * 1000))
                        c['nearest_hit_offset_ms'] = pairs[-1]
                pairs.sort()
                hits = sorted(o['seconds'] for o in onsets)

                def near_hit(t):
                    i = bisect.bisect_left(hits, t - window_s)
                    return i < len(hits) and hits[i] <= t + window_s
                grid = [args.start + k * 0.01 for k in range(int(length / 0.01))]
                chance = sum(1 for t in grid if near_hit(t)) / len(grid) if grid and hits else 0
                k, m = len(pairs), len(changes)
                # Probability of at least k of m changes landing near a hit if changes ignored the sound.
                p_value = sum(math.comb(m, i) * chance ** i * (1 - chance) ** (m - i) for i in range(k, m + 1)) if m else None
                record.update(picture_changes=changes, sync={
                    'changes': len(changes), 'with_hit_within_2_frames': len(pairs),
                    'share': round(len(pairs) / len(changes), 2) if changes else None,
                    'chance_share': round(chance, 2),
                    'p_by_chance': round(p_value, 3) if p_value is not None else None,
                    'median_offset_ms': pairs[len(pairs) // 2] if pairs else None,
                    'note': 'Treat as sync evidence only when p_by_chance is small (<= 0.05); dense music makes chance_share high. '
                            'offset > 0: sound after the picture change; the 30 fps video grid is +-33 ms.'})

            # Sheet: frames at the strongest hits over a band-energy timeline, numbered so each frame finds its tick.
            width, plot_h, cell_w, cell_h, cols = 1600, 300, 200, 200, 8
            shown = sorted(sorted(onsets, key=lambda o: o['rise_db'], reverse=True)[:args.top] if info['has_video'] else [],
                           key=lambda o: o['seconds'])
            rows = math.ceil(len(shown) / cols)
            sheet = Image.new('RGB', (width, 48 + rows * (cell_h + 22) + plot_h + 56), '#141820')
            draw = ImageDraw.Draw(sheet)
            loud = record['loudness']
            draw.text((10, 8), f"{label} | {path.name[:110]}", fill='white')
            draw.text((10, 26), f"{args.start:.2f}-{end:.2f}s | {loud['integrated_lufs']} LUFS | true peak {loud['true_peak_dbfs']} dBFS | "
                                f"{len(onsets)} hits, {len(swells)} swells | tempo {(record['tempo'] or {}).get('bpm', '-')} BPM "
                                f"(conf {(record['tempo'] or {}).get('confidence', '-')}) | picture changes with a hit "
                                f"{record.get('sync', {}).get('with_hit_within_2_frames', '-')}/{record.get('sync', {}).get('changes', '-')} "
                                f"(chance {record.get('sync', {}).get('chance_share', '-')}, p {record.get('sync', {}).get('p_by_chance', '-')}) | "
                                f"candidates, not auditioned", fill='#b8c6d8')
            for k, o in enumerate(shown):
                raw = run(['ffmpeg', '-v', 'error', '-ss', str(o['seconds']), '-i', str(path), '-frames:v', '1',
                           '-vf', f'scale={cell_w}:{cell_h - 20}:force_original_aspect_ratio=decrease',
                           '-f', 'image2pipe', '-vcodec', 'png', '-'])
                x, y = k % cols * cell_w, 48 + k // cols * (cell_h + 22)
                if raw:
                    frame = ImageOps.pad(Image.open(io.BytesIO(raw)).convert('RGB'), (cell_w - 4, cell_h - 20), color='#07090d')
                    sheet.paste(frame, (x + 2, y))
                draw.text((x + 6, y + cell_h - 16), f"{k + 1}  {o['seconds']:.2f}s {o['band']} +{o['rise_db']:.0f}dB", fill=COLORS[o['band']])
            top = 48 + rows * (cell_h + 22) + 10
            left, right = 40, width - 10

            def px(seconds):
                return left + (seconds - args.start) / length * (right - left)

            def py(db):
                return top + (min(0, max(-60, db)) / -60) * plot_h
            for a, b in record['silences']:
                draw.rectangle([px(a), top, px(b), top + plot_h], fill='#20252f')
            for s in swells:
                draw.rectangle([px(s['start_seconds']), top, px(s['peak_seconds']), top + plot_h], fill='#2a2f24')
            for db in (0, -20, -40, -60):
                draw.line([left, py(db), right, py(db)], fill='#2c3340')
                draw.text((4, py(db) - 6), f'{db}', fill='#7d8796')
            step = max(1, round(length / 16))
            for s in range(math.ceil(args.start), math.floor(end) + 1, step):
                draw.line([px(s), top + plot_h, px(s), top + plot_h + 6], fill='#7d8796')
                draw.text((px(s) - 8, top + plot_h + 10), f'{s}s', fill='#7d8796')
            for name, env in list(bands.items()) + [('full', full)]:
                points = [(px(args.start + lead_in + i * hop), py(v)) for i, v in enumerate(env)]
                stride = max(1, len(points) // (right - left))
                draw.line(points[::stride], fill=COLORS[name], width=1)
            for o in onsets:
                draw.line([px(o['seconds']), top, px(o['seconds']), top + 10], fill=COLORS[o['band']], width=2)
            for k, o in enumerate(shown):
                draw.text((px(o['seconds']) - 3, top + 12), str(k + 1), fill='white')
            for c in record.get('picture_changes', []):
                x = px(c['seconds'])
                draw.polygon([(x - 4, top + plot_h), (x + 4, top + plot_h), (x, top + plot_h - 8)], fill='#7fe0d0')
            lx, ly = right - 520, top + plot_h + 24
            for name, label_text in (('low', 'low <150 Hz'), ('mid', 'mid 150 Hz-4 kHz'), ('high', 'high >4 kHz'), ('full', 'full band')):
                draw.line([lx, ly + 6, lx + 16, ly + 6], fill=COLORS[name], width=2)
                draw.text((lx + 20, ly), label_text, fill='#b8c6d8')
                lx += 110
            draw.polygon([(lx, ly + 10), (lx + 8, ly + 10), (lx + 4, ly + 2)], fill='#7fe0d0')
            draw.text((lx + 12, ly), 'picture change', fill='#b8c6d8')
            name = f"{label}-audio.png"
            # Exclusive creation also catches a collision instead of losing evidence.
            with (args.output / name).open('xb') as output:
                sheet.save(output, format='PNG')
            record['sheet'] = name
        except (subprocess.CalledProcessError, ValueError, KeyError, OSError) as exc:
            record.update(error=str(exc), review_status='failed')
        records.append(record)

    (args.output / 'audio.json').write_text(json.dumps(records, indent=2) + '\n')
    failures = [r['file'] for r in records if 'error' in r]
    print(json.dumps({'clips': len(records), 'with_audio': sum(1 for r in records if r.get('audio')),
                      'failed': failures, 'report': str((args.output / 'audio.json').resolve())}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
