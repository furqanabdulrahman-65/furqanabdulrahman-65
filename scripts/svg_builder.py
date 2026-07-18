from animation import build_animation

BACKGROUND="#0d1117"

CHAR_WIDTH=7
LINE_HEIGHT=13

class SVGBuilder:

    def __init__(self,rows):

        self.rows=rows

        self.width=len(rows[0])*CHAR_WIDTH+30

        self.height=len(rows)*LINE_HEIGHT+30

    def build(self):

        clips,texts,cursor=build_animation(
            self.rows,
            CHAR_WIDTH,
            LINE_HEIGHT
        )

        return f"""
<svg xmlns="http://www.w3.org/2000/svg"
width="{self.width}"
height="{self.height}"
viewBox="0 0 {self.width} {self.height}">

<rect width="100%" height="100%" fill="{BACKGROUND}"/>

<defs>

{clips}

</defs>

{texts}

{cursor}

</svg>
"""