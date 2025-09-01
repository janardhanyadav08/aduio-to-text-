from datetime import timedelta

def _format_ts(seconds: float) -> str:
    if seconds is None:
        seconds = 0.0
    td = timedelta(seconds=float(seconds))
    h, remainder = divmod(td.seconds, 3600)
    m, s = divmod(remainder, 60)
    ms = int(td.microseconds / 1000)
    h += td.days * 24
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def segments_to_srt(segments):
    lines = []
    for i, seg in enumerate(segments, 1):
        start = _format_ts(seg.get('start'))
        end = _format_ts(seg.get('end'))
        text = (seg.get('text') or '').strip()
        lines.append(f"{i}\n{start} --> {end}\n{text}\n")
    return "\n".join(lines)
