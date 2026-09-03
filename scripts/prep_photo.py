"""
Prepare a portrait photo for clean ASCII conversion.

1. Remove the background using rembg.
2. Boost local contrast using CLAHE.
3. Composite the subject onto a pure white background.

Output: source-prepped.png
"""

import os
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove


HERE = os.path.dirname(os.path.abspath(__file__))

INP = (
    sys.argv[1]
    if len(sys.argv) > 1
    else os.path.join(HERE, "..", "source-photo.jpg")
)

OUT = (
    sys.argv[2]
    if len(sys.argv) > 2
    else os.path.join(HERE, "..", "source-prepped.png")
)


# 1. Remove the background
cut = remove(Image.open(INP).convert("RGBA"))

rgb = np.array(cut.convert("RGB"))
alpha = np.array(cut.split()[-1])


# 2. Increase local contrast using CLAHE
gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

clahe = cv2.createCLAHE(
    clipLimit=2.6,
    tileGridSize=(8, 8)
)

gray = clahe.apply(gray)


# Slightly brighten the image
gray = cv2.convertScaleAbs(
    gray,
    alpha=1.05,
    beta=18
)


# 3. Put the subject onto a white background
mask = alpha.astype(np.float32) / 255.0

# Slight feathering to prevent a harsh halo
mask = cv2.GaussianBlur(
    mask,
    (0, 0),
    1.0
)

out = (
    gray.astype(np.float32) * mask
    + 255.0 * (1.0 - mask)
)

out = np.clip(
    out,
    0,
    255
).astype(np.uint8)


# Save grayscale output
Image.fromarray(
    out,
    mode="L"
).save(OUT)

print("wrote", OUT, out.shape)