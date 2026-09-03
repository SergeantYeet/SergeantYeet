from pathlib import Path
import json
from datetime import date, timedelta
import html


# ==========================================
# CONFIGURATION
# ==========================================

DATA_FILE = Path("data/contributions.json")
OUTPUT_FILE = Path("contrib-heatmap.svg")

WIDTH = 860
HEIGHT = 190

CELL = 11
GAP = 3

LEFT = 30
TOP = 30

RADIUS = 2

# GitHub-style contribution colors
PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]


# ==========================================
# LOAD DATA
# ==========================================

data = json.loads(
    DATA_FILE.read_text(
        encoding="utf-8"
    )
)

days = data["days"]

day_map = {
    item["date"]: item
    for item in days
}


# ==========================================
# BUILD 53-WEEK CALENDAR
# ==========================================

today = date.today()

# Find the Sunday beginning the displayed range.
# We display 53 weeks.
start = today - timedelta(
    days=today.weekday() + 1
)

start -= timedelta(
    weeks=52
)


# ==========================================
# SVG HEADER
# ==========================================

svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<rect
width="100%"
height="100%"
rx="10"
fill="#0d1117"/>

<style>
.cell {{
    opacity: 0;
    transform-box: fill-box;
    transform-origin: center;
    animation: reveal 0.45s ease-out forwards;
}}

@keyframes reveal {{
    from {{
        opacity: 0;
        transform: translate(-5px, -5px);
    }}

    to {{
        opacity: 1;
        transform: translate(0, 0);
    }}
}}
</style>
'''


# ==========================================
# DRAW CELLS
# ==========================================

for week in range(53):

    for weekday in range(7):

        current = start + timedelta(
            weeks=week,
            days=weekday
        )

        item = day_map.get(
            current.isoformat(),
            {
                "count": 0,
                "level": 0
            }
        )

        level = int(
            item.get("level", 0)
        )

        level = max(
            0,
            min(level, len(PALETTE) - 1)
        )

        color = PALETTE[level]

        x = (
            LEFT
            + week * (CELL + GAP)
        )

        y = (
            TOP
            + weekday * (CELL + GAP)
        )

        delay = (
            week * 0.025
            + weekday * 0.015
        )

        svg += f'''
<rect
class="cell"
x="{x}"
y="{y}"
width="{CELL}"
height="{CELL}"
rx="{RADIUS}"
fill="{color}"
style="animation-delay:{delay:.3f}s"/>

<title>
{html.escape(current.isoformat())}:
{item.get("count", 0)} contributions
</title>
'''


# ==========================================
# LEGEND
# ==========================================

legend_y = 126

svg += '''
<text
x="30"
y="170"
font-family="monospace"
font-size="11"
fill="#8b949e">
Less
</text>
'''

for i, color in enumerate(PALETTE):

    x = 62 + i * 17

    svg += f'''
<rect
x="{x}"
y="160"
width="11"
height="11"
rx="2"
fill="{color}"/>
'''


svg += '''
<text
x="166"
y="170"
font-family="monospace"
font-size="11"
fill="#8b949e">
More
</text>
'''


# ==========================================
# STATS FOOTER
# ==========================================

total = data.get(
    "total",
    0
)

current_streak = data.get(
    "current_streak",
    0
)

longest_streak = data.get(
    "longest_streak",
    0
)

svg += f'''
<text
x="300"
y="170"
font-family="monospace"
font-size="11"
fill="#8b949e">
{total:,} contributions ·
streak {current_streak} ·
best {longest_streak}
</text>
'''


# ==========================================
# FINISH
# ==========================================

svg += "</svg>"

OUTPUT_FILE.write_text(
    svg,
    encoding="utf-8"
)

print(
    f"wrote {OUTPUT_FILE}"
)