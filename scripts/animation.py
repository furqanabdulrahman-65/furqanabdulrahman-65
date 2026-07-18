from xml.sax.saxutils import escape

TOTAL_DURATION = 4.5
CURSOR_COLOR = "#58a6ff"


def build_animation(rows, char_width, line_height):

    total_rows = len(rows)

    clip_defs = []
    animated_rows = []
    cursor = []

    for i, row in enumerate(rows):

        delay = i * (TOTAL_DURATION / total_rows)

        y = 20 + i * line_height

        width = len(row) * char_width

        clip_defs.append(f"""
<clipPath id="clip{i}">
    <rect x="15"
          y="{y-line_height+2}"
          width="{width}"
          height="{line_height}">
    </rect>
</clipPath>
""")

        safe_row = escape(row)

        animated_rows.append(f"""
<text
x="15"
y="{y}"
clip-path="url(#clip{i})"
font-family="Consolas, monospace"
font-size="11"
fill="#c9d1d9">

{safe_row}

</text>
""")

        cursor.append(f"""
<rect
x="{15+width}"
y="{y-line_height+2}"
width="2"
height="{line_height}"
fill="{CURSOR_COLOR}">

<animate
attributeName="opacity"
values="1;0;1"
dur="0.6s"
repeatCount="indefinite"/>

</rect>
""")

    return (
        "\n".join(clip_defs),
        "\n".join(animated_rows),
        "\n".join(cursor)
    )