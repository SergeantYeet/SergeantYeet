from pathlib import Path
from PIL import Image
import html
import math

# -----------------------------
# Configuration
# -----------------------------

INPUT = Path("source-prepped.png")
OUTPUT = Path("avi-ascii.svg")

COLS = 100
ROWS = 40

# Bright -> dark
RAMP = " .`:-=+*cs#%@"

TEXT_COLOR = "#b8b8b8"

FONT_SIZE = 8
CHAR_WIDTH = 4.8
LINE_HEIGHT = 8

ROW_DELAY = 0.045
ROW_DURATION = 0.55


# -----------------------------
# Load image
# -----------------------------

img = Image.open(INPUT).convert("L")

# Preserve approximate character aspect ratio.
# Terminal characters are taller than they are wide.
target_width = COLS
target_height = ROWS

img = img.resize(
    (target_width, target_height),
    Image.Resampling.LANCZOS
)


# -----------------------------
# Convert pixels → ASCII
# -----------------------------

ascii_rows = []

for y in range(target_height):
    row = []

    for x in range(target_width):
        brightness = img.getpixel((x, y))

        # Convert brightness:
        # 255 = white → first character
        # 0   = black → last character
        index = int(
            (255 - brightness)
            / 255
            * (len(RAMP) - 1)
        )

        row.append(RAMP[index])

    ascii_rows.append("".join(row))


# -----------------------------
# SVG dimensions
# -----------------------------

WIDTH = COLS * CHAR_WIDTH
HEIGHT = ROWS * LINE_HEIGHT


# -----------------------------
# Build SVG
# -----------------------------

parts = []

parts.append(
    f'''<svg xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}">
'''
)

parts.append(
    f'''
<rect width="100%" height="100%" fill="white"/>
'''
)


# -----------------------------
# Define clipping regions
# -----------------------------

parts.append("<defs>")

for y in range(ROWS):
    clip_y = y * LINE_HEIGHT

    parts.append(
        f'''
<clipPath id="row-{y}">
    <rect
        x="0"
        y="{clip_y - LINE_HEIGHT}"
        width="0"
        height="{LINE_HEIGHT * 2}"
    >
        <animate
            attributeName="width"
            from="0"
            to="{WIDTH}"
            dur="{ROW_DURATION}s"
            begin="{y * ROW_DELAY}s"
            fill="freeze"
        />
    </rect>
</clipPath>
'''
    )

parts.append("</defs>")


# -----------------------------
# Draw ASCII rows
# -----------------------------

for y, row in enumerate(ascii_rows):

    y_pos = (y + 1) * LINE_HEIGHT

    escaped = html.escape(row)

    parts.append(
        f'''
<text
    x="0"
    y="{y_pos}"
    font-family="monospace"
    font-size="{FONT_SIZE}px"
    fill="{TEXT_COLOR}"
    xml:space="preserve"
    clip-path="url(#row-{y})"
>{escaped}</text>
'''
    )


# -----------------------------
# Finish SVG
# -----------------------------

parts.append("</svg>")

OUTPUT.write_text(
    "".join(parts),
    encoding="utf-8"
)

print(f"wrote {OUTPUT}")