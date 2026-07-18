from rembg import remove
from PIL import Image
import cv2
import numpy as np

INPUT_IMAGE = "photo.jpg"
OUTPUT_IMAGE = "source-prepped.png"

# ----------------------------
# Remove Background
# ----------------------------
print("Removing background...")

with open(INPUT_IMAGE, "rb") as i:
    input_data = i.read()

output_data = remove(input_data)

with open("temp.png", "wb") as o:
    o.write(output_data)

# ----------------------------
# Open RGBA Image
# ----------------------------
img = Image.open("temp.png").convert("RGBA")

# White background
background = Image.new("RGBA", img.size, (255, 255, 255, 255))
background.paste(img, mask=img)

rgb = np.array(background.convert("RGB"))

# ----------------------------
# Convert to grayscale
# ----------------------------
gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

# ----------------------------
# CLAHE (Adaptive Contrast)
# ----------------------------
clahe = cv2.createCLAHE(
    clipLimit=2.5,
    tileGridSize=(8, 8)
)

gray = clahe.apply(gray)

# ----------------------------
# Light smoothing
# ----------------------------
gray = cv2.GaussianBlur(gray, (3, 3), 0)

# ----------------------------
# Save
# ----------------------------
cv2.imwrite(OUTPUT_IMAGE, gray)

print(f"Saved: {OUTPUT_IMAGE}")