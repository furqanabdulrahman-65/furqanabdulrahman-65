from animation import build_animation

BACKGROUND = "#0d1117"


class SVGBuilder:

    def __init__(self, rows):
        self.rows = rows
        # Fixed card size mirroring the side-by-side terminal look
        self.width = 414
        self.height = 390
        # Calibrate characters exactly to fill the terminal window body
        self.char_width = round((self.width - 30) / len(rows[0]), 4)
        self.line_height = round((self.height - 36 - 20) / len(rows), 4)

    def build(self):
        clips, texts, cursor = build_animation(
            self.rows,
            self.char_width,
            self.line_height,
            y_start=48
        )

        return f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="{self.width}"
     height="{self.height}"
     viewBox="0 0 {self.width} {self.height}">

  <rect width="100%" height="100%" rx="10" fill="{BACKGROUND}" stroke="#30363d" stroke-width="1.5"/>

  <!-- Title Bar -->
  <g>
    <!-- Mac / Unix window controls -->
    <circle cx="20" cy="18" r="5" fill="#ff5f56" />
    <circle cx="35" cy="18" r="5" fill="#ffbd2e" />
    <circle cx="50" cy="18" r="5" fill="#27c93f" />
    <text x="{self.width // 2}" y="18" font-family="Consolas, monospace" font-size="11" fill="#8b949e" text-anchor="middle" dominant-baseline="middle">furqan@portrait:~</text>
    <line x1="0" y1="34" x2="{self.width}" y2="34" stroke="#21262d" stroke-width="1" />
  </g>

  <defs>
{clips}
  </defs>

{texts}

{cursor}

</svg>
"""