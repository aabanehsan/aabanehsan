"""Generate the profile SVGs (identity banner and info card).

Run: python scripts/gen_art.py
Needs: pyfiglet (only for the wordmark grid)
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

import pyfiglet

OUT = Path(__file__).resolve().parent.parent / "assets"

BG = "#0d1117"
PANEL = "#161b22"
BORDER = "#30363d"
FG = "#c9d1d9"
DIM = "#8b949e"
GREEN = "#39d353"
SHADOW = "#1a7f37"
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def window(width: int, height: int, title: str) -> str:
    """Terminal window frame with traffic-light dots."""
    return f"""
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="{BG}" stroke="{BORDER}"/>
  <path d="M0.5 36 H{width - 0.5}" stroke="{BORDER}"/>
  <path d="M12.5 0.5 H{width - 12.5} A12 12 0 0 1 {width - 0.5} 12.5 V36 H0.5 V12.5 A12 12 0 0 1 12.5 0.5 Z" fill="{PANEL}"/>
  <circle cx="22" cy="18" r="6" fill="#ff5f57"/>
  <circle cx="42" cy="18" r="6" fill="#febc2e"/>
  <circle cx="62" cy="18" r="6" fill="#28c840"/>
  <text x="{width / 2}" y="23" text-anchor="middle" class="t dim" font-size="13">{escape(title)}</text>"""


def glyph(ch: str, x: float, y: float, w: float, h: float) -> str:
    """Draw one ANSI Shadow character as shapes so it never depends on fonts."""
    if ch == "█":
        return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w + 0.4:.1f}" height="{h + 0.4:.1f}" fill="{GREEN}"/>'
    cx, cy = x + w / 2, y + h / 2
    s = f'stroke="{SHADOW}" stroke-width="2" fill="none"'
    lines = {
        "═": f"M{x} {cy} H{x + w}",
        "║": f"M{cx} {y} V{y + h}",
        "╔": f"M{x + w} {cy} H{cx} V{y + h}",
        "╗": f"M{x} {cy} H{cx} V{y + h}",
        "╚": f"M{cx} {y} V{cy} H{x + w}",
        "╝": f"M{cx} {y} V{cy} H{x}",
    }
    d = lines.get(ch)
    return f'<path d="{d}" {s}/>' if d else ""


def identity() -> str:
    width, height = 900, 262
    cw, ch = 9.0, 14
    rows_a = pyfiglet.figlet_format("AABAN", font="ansi_shadow").rstrip("\n").split("\n")
    rows_e = pyfiglet.figlet_format("EHSAN", font="ansi_shadow").rstrip("\n").split("\n")
    rows = [a.ljust(43) + "  " + e for a, e in zip(rows_a, rows_e) if (a + e).strip()]
    cols = max(len(r) for r in rows)
    ox = (width - cols * cw) / 2
    oy = 88

    parts = []
    for i, row in enumerate(rows):
        shapes = "".join(glyph(c, ox + j * cw, oy + i * ch, cw, ch) for j, c in enumerate(row) if c != " ")
        parts.append(f'<g class="row" style="animation-delay:{1.2 + i * 0.12:.2f}s">{shapes}</g>')

    tagline = "cloud defense  //  red teaming  //  ai security"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Aaban Ehsan">
  <title>Aaban Ehsan</title>
  <style>
    .t {{ font-family: {FONT}; fill: {FG}; }}
    .dim {{ fill: {DIM}; }}
    .g {{ fill: {GREEN}; }}
    .type1 {{ clip-path: inset(0 100% 0 0); animation: type 0.9s steps(16) 0.2s forwards; }}
    .type2 {{ clip-path: inset(0 100% 0 0); animation: type 1.4s steps(38) 2.3s forwards; }}
    .row {{ opacity: 0; animation: in 0.35s ease-out forwards; }}
    .cur {{ animation: blink 1s steps(1) infinite; }}
    .scan {{ animation: scan 6s linear infinite; }}
    @keyframes type {{ to {{ clip-path: inset(0 0 0 0); }} }}
    @keyframes in {{ from {{ opacity: 0; transform: translateY(4px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @keyframes scan {{ from {{ transform: translateY(36px); }} to {{ transform: translateY({height}px); }} }}
    @media (prefers-reduced-motion: reduce) {{
      .type1, .type2, .row {{ animation: none; opacity: 1; clip-path: none; }}
      .scan, .cur {{ animation: none; }}
    }}
  </style>
  <defs>
    <linearGradient id="sl" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
      <stop offset="1" stop-color="{GREEN}" stop-opacity="0.07"/>
    </linearGradient>
    <clipPath id="body"><rect x="1" y="37" width="{width - 2}" height="{height - 38}" rx="11"/></clipPath>
  </defs>
  {window(width, height, "aaban@github: ~")}
  <text x="28" y="66" class="t type1" font-size="15"><tspan class="g">aaban@github</tspan><tspan class="dim"> ~ $ </tspan>whoami --ascii</text>
  {''.join(parts)}
  <text x="28" y="{oy + len(rows) * ch + 42}" class="t type2" font-size="15" textLength="{(len(tagline) + 2) * 9}" lengthAdjust="spacing"><tspan class="g">&gt;</tspan> {escape(tagline)}</text>
  <rect x="{28 + (len(tagline) + 2) * 9 + 4}" y="{oy + len(rows) * ch + 29}" width="9" height="17" class="g cur"/>
  <g clip-path="url(#body)"><rect class="scan" x="0" y="0" width="{width}" height="40" fill="url(#sl)"/></g>
</svg>
"""


LOGO = r"""
      .--------.
     /  .----.  \
    |  /      \  |
    |  |      |  |
  .-'--'------'--'-.
  |      .--.      |
  |     ( () )     |
  |      '||'      |
  |       ||       |
  |       ''       |
  '----------------'
""".strip("\n").split("\n")

INFO = [
    ("Role", "Cloud Defense, InfoSec @ State Farm"),
    ("Prev", "GRC, Pentest Intern @ State Farm"),
    ("School", "UT Austin, B.S. Informatics '28"),
    ("Minor", "Statistics & Data Science"),
    ("Focus", "Cloud security, red teaming, AI security"),
    ("Tools", "Burp Suite, Nmap, Nessus, Metasploit, ffuf"),
    ("Stack", "Python, Bash, Linux, Docker, SQL, R"),
    ("Blue", "Elastic SIEM, Linux hardening"),
    ("Practice", "Hack The Box weekly, red vs blue lab"),
    ("Building", "promptprobe, grc-mapper, redvblue-lab"),
    ("Web", "aabanehsan.vercel.app"),
    ("Contact", "linkedin.com/in/aaban-ehsan"),
]


def info_card() -> str:
    width = 900
    lh = 22
    top = 96
    height = top + (len(INFO) + 3) * lh + 30
    lx, rx = 34, 300

    logo = "".join(
        f'<text x="{lx}" y="{top + 34 + i * 19}" class="t g" font-size="15" xml:space="preserve">{escape(line)}</text>'
        for i, line in enumerate(LOGO)
    )

    lines = [
        f'<text x="{rx}" y="{top}" class="t" font-size="15"><tspan class="g b">aaban</tspan>@<tspan class="g b">ehsan</tspan></text>',
        f'<text x="{rx}" y="{top + lh}" class="t dim" font-size="15">{"-" * 11}</text>',
    ]
    for i, (k, v) in enumerate(INFO):
        y = top + (i + 2) * lh
        delay = 0.25 + i * 0.08
        lines.append(
            f'<text x="{rx}" y="{y}" class="t ln" font-size="15" style="animation-delay:{delay:.2f}s">'
            f'<tspan class="g b">{escape(k)}</tspan><tspan class="dim">:</tspan> '
            f'<tspan x="{rx + 92}">{escape(v)}</tspan></text>'
        )
    palette = ["#0d1117", "#ff5f57", "#28c840", "#febc2e", "#58a6ff", "#bc8cff", "#39c5cf", "#c9d1d9"]
    by = top + (len(INFO) + 2) * lh + 4
    blocks = "".join(
        f'<rect x="{rx + i * 26}" y="{by}" width="24" height="16" fill="{c}" stroke="{BORDER}"/>'
        for i, c in enumerate(palette)
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Aaban Ehsan info card">
  <title>whoami --verbose</title>
  <style>
    .t {{ font-family: {FONT}; fill: {FG}; }}
    .dim {{ fill: {DIM}; }}
    .g {{ fill: {GREEN}; }}
    .b {{ font-weight: 700; }}
    .ln {{ opacity: 0; animation: in 0.3s ease-out forwards; }}
    @keyframes in {{ from {{ opacity: 0; transform: translateX(-6px); }} to {{ opacity: 1; transform: none; }} }}
    @media (prefers-reduced-motion: reduce) {{ .ln {{ animation: none; opacity: 1; }} }}
  </style>
  {window(width, height, "aaban@github: ~ (neofetch)")}
  <text x="{lx}" y="66" class="t" font-size="15"><tspan class="g">aaban@github</tspan><tspan class="dim"> ~ $ </tspan>whoami --verbose</text>
  {logo}
  {''.join(lines)}
  {blocks}
</svg>
"""


def main() -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / "identity.svg").write_text(identity(), encoding="utf-8")
    (OUT / "info-card.svg").write_text(info_card(), encoding="utf-8")
    print("wrote", OUT / "identity.svg", OUT / "info-card.svg")


if __name__ == "__main__":
    main()
