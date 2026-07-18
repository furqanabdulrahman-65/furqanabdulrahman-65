import os
from ascii_generator import AsciiGenerator
from svg_builder import SVGBuilder

current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "source-prepped.png")

generator = AsciiGenerator(image_path)
rows = generator.generate()

builder = SVGBuilder(rows)
svg = builder.build()

output_path = os.path.join(os.path.dirname(current_dir), "avi-ascii.svg")

with open(output_path, "w", encoding="utf8") as f:
    f.write(svg)

print(f"avi-ascii.svg created at {output_path}!")