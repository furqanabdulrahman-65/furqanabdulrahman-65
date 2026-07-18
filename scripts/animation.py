from xml.sax.saxutils import escape

TOTAL_DURATION = 4.0
CURSOR_COLOR = "#58a6ff"


def build_animation(rows, char_width, line_height):
    total_rows = len(rows)
    row_dur = TOTAL_DURATION / total_rows

    clip_defs = []
    animated_rows = []
    cursor = []

    for i, row in enumerate(rows):
        begin_time = round(i * row_dur, 4)
        y = 20 + i * line_height
        width = len(row) * char_width

        clip_defs.append(f"""
<clipPath id="clip{i}">
    <rect x="15" y="{y - line_height + 2}" width="0" height="{line_height}">
        <animate attributeName="width" from="0" to="{width}" begin="{begin_time}s" dur="{row_dur:.4f}s" fill="freeze" />
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
xml:space="preserve"
fill="#c9d1d9">
{safe_row}
</text>
""")

        cursor.append(f"""
<rect
x="15"
y="{y - line_height + 2}"
width="6"
height="{line_height}"
fill="{CURSOR_COLOR}"
opacity="0">
    <animate attributeName="x" from="15" to="{15 + width}" begin="{begin_time}s" dur="{row_dur:.4f}s" fill="freeze" />
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.99;1" begin="{begin_time}s" dur="{row_dur:.4f}s" fill="freeze" />
</rect>
""")

    if total_rows > 0:
        last_y = 20 + (total_rows - 1) * line_height
        last_width = len(rows[-1]) * char_width
        cursor.append(f"""
<rect
x="{15 + last_width}"
y="{last_y - line_height + 2}"
width="6"
height="{line_height}"
fill="{CURSOR_COLOR}"
opacity="0">
    <animate attributeName="opacity" values="0;1;0;1" keyTimes="0;0.5;0.51;1" begin="{TOTAL_DURATION}s" dur="0.8s" repeatCount="indefinite" />
</rect>
""")

    return (
        "\n".join(clip_defs),
        "\n".join(animated_rows),
        "\n".join(cursor)
    )