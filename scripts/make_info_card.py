import os

STATIC = os.environ.get("STATIC") == "1"

WIDTH = 446
HEIGHT = 390

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
    # Helper to wrap elements in animation if not static
    def anim(delay):
        if STATIC:
            return ""
        return f"""
        <animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.4s" fill="freeze" />
        <animateTransform attributeName="transform" type="translate" from="0 8" to="0 0" begin="{delay}s" dur="0.4s" fill="freeze" />
        """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="{WIDTH}"
     height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}">
  <style>
    .key {{ font-weight: bold; fill: #58a6ff; }}
    .val {{ fill: #c9d1d9; }}
    .title {{ font-weight: bold; fill: #58a6ff; }}
  </style>

  <rect width="100%" height="100%" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.5" />

  <!-- Terminal Window Title Bar -->
  <g opacity="{1 if STATIC else 0}" transform="translate(0, 0)">
    {anim(0.05)}
    <!-- Mac / Unix window controls -->
    <circle cx="20" cy="18" r="5" fill="#ff5f56" />
    <circle cx="35" cy="18" r="5" fill="#ffbd2e" />
    <circle cx="50" cy="18" r="5" fill="#27c93f" />
    <text x="{WIDTH // 2}" y="18" font-family="Consolas, monospace" font-size="11" fill="#8b949e" text-anchor="middle" dominant-baseline="middle">furqan@terminal:~</text>
    <line x1="0" y1="34" x2="{WIDTH}" y2="34" stroke="#21262d" stroke-width="1" />
  </g>

  <!-- Title / Logo details -->
  <g opacity="{1 if STATIC else 0}" transform="translate(0, 0)">
    {anim(0.15)}
    <text x="25" y="62" font-family="Consolas, monospace" font-size="16" class="title">furqan@github</text>
    <text x="25" y="80" font-family="Consolas, monospace" font-size="12" fill="#8b949e">------------------------------</text>
  </g>
"""

    y = 110
    for i, (key, value) in enumerate(INFO):
        delay = 0.25 + i * 0.08
        svg += f"""
  <g opacity="{1 if STATIC else 0}" transform="translate(0, 0)">
    {anim(delay)}
    <text x="25" y="{y}" font-family="Consolas, monospace" font-size="13" class="key">{key}:</text>
    <text x="120" y="{y}" font-family="Consolas, monospace" font-size="13" class="val">{value}</text>
  </g>
"""
        y += 30

    # Animated blinking bottom prompt
    prompt_delay = 0.25 + len(INFO) * 0.08
    svg += f"""
  <g opacity="{1 if STATIC else 0}">
    {anim(prompt_delay)}
    <text x="25" y="340" font-family="Consolas, monospace" font-size="13" fill="#8b949e">furqan@terminal:~$ </text>
    <rect x="170" y="327" width="8" height="15" fill="#58a6ff" opacity="0">
      <animate attributeName="opacity" values="0;1;0;1" keyTimes="0;0.5;0.51;1" begin="{prompt_delay + 0.4}s" dur="0.8s" repeatCount="indefinite" />
    </rect>
  </g>
"""

    svg += """
</svg>
"""
    return svg


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(os.path.dirname(current_dir), "info-card.svg")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(create_card())
    print(f"info-card.svg created at {output_path}!")

