from ascii_generator import AsciiGenerator
from svg_builder import SVGBuilder

generator = AsciiGenerator("source-prepped.png")

rows = generator.generate()

builder = SVGBuilder(rows)

svg = builder.build()

with open("ascii.svg", "w", encoding="utf8") as f:
    f.write(svg)

print("ascii.svg created!")