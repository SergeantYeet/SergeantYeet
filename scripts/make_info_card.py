from pathlib import Path
import os

OUTPUT = Path("info-card.svg")

USERNAME = "Sergeant"

ROWS = [
    ("Now", "B.Tech CSE (AI/ML)"),
    ("Prev", "School"),
    ("Stack", "C, Python, Git, Java"),
    ("Level", "Basics in all"),
    ("Highlights", "Gaming, coding, design"),
]

# -----------------------------
# Card configuration
# -----------------------------

WIDTH = 490
HEIGHT = 300

BG = "#0d1117"
BORDER = "#30363d"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
ACCENT = "#58a6ff"

FONT = "monospace"


# -----------------------------
# SVG
# -----------------------------

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}">

<rect
    x="1"
    y="1"
    width="{WIDTH - 2}"
    height="{HEIGHT - 2}"
    rx="10"
    fill="{BG}"
    stroke="{BORDER}"
    stroke-width="2"/>

<!-- Title -->
<text
    x="24"
    y="38"
    font-family="{FONT}"
    font-size="18"
    font-weight="bold"
    fill="{ACCENT}">
    {USERNAME}@github
</text>

<text
    x="24"
    y="60"
    font-family="{FONT}"
    font-size="12"
    fill="{MUTED}">
    ~ $ whoami
</text>

<line
    x1="24"
    y1="76"
    x2="{WIDTH - 24}"
    y2="76"
    stroke="{BORDER}"
    stroke-width="1"/>

'''

# -----------------------------
# Animated information rows
# -----------------------------

start_y = 108
row_spacing = 36

for i, (key, value) in enumerate(ROWS):

    y = start_y + i * row_spacing
    delay = 0.25 + i * 0.12

    svg += f'''
<g opacity="0">

    <animate
        attributeName="opacity"
        from="0"
        to="1"
        dur="0.35s"
        begin="{delay}s"
        fill="freeze"/>

    <text
        x="28"
        y="{y}"
        font-family="{FONT}"
        font-size="13"
        font-weight="bold"
        fill="{ACCENT}">
        {key}:
    </text>

    <text
        x="145"
        y="{y}"
        font-family="{FONT}"
        font-size="13"
        fill="{TEXT}">
        {value}
    </text>

</g>
'''

svg += '''
</svg>
'''

OUTPUT.write_text(svg, encoding="utf-8")

print(f"wrote {OUTPUT}")