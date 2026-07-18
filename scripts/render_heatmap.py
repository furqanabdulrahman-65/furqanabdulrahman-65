import json


COLORS = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353"
]


CELL = 12


with open(
    "../contributions.json"
) as f:

    data = json.load(f)



svg = """
<svg xmlns="http://www.w3.org/2000/svg"
width="900"
height="170">
"""


x = 10
y = 20


for i, day in enumerate(data):

    level = day["level"]

    svg += f"""
<rect
x="{x}"
y="{y}"
width="10"
height="10"
rx="2"
fill="{COLORS[level]}"/>
"""


    x += CELL


    if (i+1)%53 == 0:

        x = 10
        y += CELL



svg += """

</svg>
"""


with open(
    "../contribution.svg",
    "w"
) as f:

    f.write(svg)



print("contribution.svg created")