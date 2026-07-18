WIDTH = 500
HEIGHT = 280


INFO = [
    ("User", "Mohammed Furqan Abdul Rahman"),
    ("Role", "AI Engineer"),
    ("Stack", "Python | FastAPI | RAG"),
    ("AI", "LLMs | LangGraph | Multi-Agent"),
    ("Cloud", "Docker | AWS Basics"),
    ("Projects", "Enterprise AI Platform"),
    ("Location", "India")
]


def create_card():

    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}"
height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<rect
width="100%"
height="100%"
rx="15"
fill="#0d1117"
stroke="#30363d"/>


<text
x="25"
y="45"
font-family="monospace"
font-size="22"
fill="#58a6ff">
furqan@github
</text>


<text
x="25"
y="70"
font-family="monospace"
font-size="12"
fill="#8b949e">
------------------------------
</text>

"""

    y = 105

    for key,value in INFO:

        svg += f"""

<text
x="25"
y="{y}"
font-family="monospace"
font-size="14"
fill="#58a6ff">

{key}

</text>


<text
x="140"
y="{y}"
font-family="monospace"
font-size="14"
fill="#c9d1d9">

{value}

</text>

"""

        y += 25


    svg += """

</svg>
"""

    return svg



with open("../info-card.svg","w",encoding="utf-8") as f:

    f.write(create_card())


print("info-card.svg created")