import os
import base64
from xml.sax.saxutils import escape

# Paths
scripts_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(scripts_dir)
photo_path = os.path.join(scripts_dir, "photo.jpg")
ascii_path = os.path.join(scripts_dir, "ascii.txt")
output_path = os.path.join(root_dir, "profile-dashboard.svg")

# Encode Photo to Base64
if os.path.exists(photo_path):
    with open(photo_path, "rb") as f:
        photo_b64 = base64.b64encode(f.read()).decode("utf-8")
else:
    photo_b64 = ""

# Read ASCII text
if os.path.exists(ascii_path):
    with open(ascii_path, "r", encoding="utf-8") as f:
        ascii_lines = [line.rstrip("\n") for line in f.readlines()]
else:
    ascii_lines = ["(ASCII Portrait)"]

# Crop/scale ASCII portrait lines if needed
# We want to display about 45 lines, 80 characters wide inside the small terminal.
ascii_lines = [line[:80].ljust(80) for line in ascii_lines[:45]]

# Generate SMIL animations for ASCII rows
char_width = 3.125  # (280px terminal width - 30px padding = 250px) / 80 cols = 3.125px
line_height = 4.5    # (260px body height) / 45 lines = 4.5px
font_size = 5.2

clips = []
texts = []
cursors = []
total_rows = len(ascii_lines)
duration = 3.0 # Duration to compile the portrait
row_dur = duration / total_rows

for i, row in enumerate(ascii_lines):
    begin_time = round(i * row_dur, 4)
    y = 52 + i * line_height
    width = len(row) * char_width

    clips.append(f"""  <clipPath id="aclip{i}">
    <rect x="15" y="{y - line_height + 1.0}" width="0" height="{line_height}">
        <animate attributeName="width" from="0" to="{width}" begin="{begin_time}s" dur="{row_dur:.4f}s" fill="freeze" />
    </rect>
  </clipPath>""")

    safe_row = escape(row)
    texts.append(f"""  <text x="15" y="{y}" clip-path="url(#aclip{i})" font-family="Consolas, monospace" font-size="{font_size}" xml:space="preserve" fill="#00ffff" opacity="0.85">{safe_row}</text>""")

    cursors.append(f"""  <rect x="15" y="{y - line_height + 1.0}" width="4" height="{line_height}" fill="#00ffff" opacity="0">
    <animate attributeName="x" from="15" to="{15 + width}" begin="{begin_time}s" dur="{row_dur:.4f}s" fill="freeze" />
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.01;0.99;1" begin="{begin_time}s" dur="{row_dur:.4f}s" fill="freeze" />
  </rect>""")

# Last blinking cursor
last_y = 52 + (total_rows - 1) * line_height
last_width = len(ascii_lines[-1]) * char_width
cursors.append(f"""  <rect x="{15 + last_width}" y="{last_y - line_height + 1.0}" width="4" height="{line_height}" fill="#00ffff" opacity="0">
    <animate attributeName="opacity" values="0;1;0;1" keyTimes="0;0.5;0.51;1" begin="{duration}s" dur="0.8s" repeatCount="indefinite" />
  </rect>""")

clips_str = "\n".join(clips)
texts_str = "\n".join(texts)
cursor_str = "\n".join(cursors)

# Details info items
INFO = [
    ("User", "Mohammed Furqan Abdul Rahman"),
    ("Role", "AI Engineer"),
    ("Stack", "Python | FastAPI | RAG"),
    ("AI", "LLMs | LangGraph | Multi-Agent"),
    ("Cloud", "Docker | AWS Basics"),
    ("Projects", "Enterprise AI Platform"),
    ("Location", "India")
]

# Generate specs rows
specs_str = ""
y_spec = 70
for i, (key, value) in enumerate(INFO):
    delay = 1.0 + i * 0.15
    specs_str += f"""
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.4s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" from="0 8" to="0 0" begin="{delay}s" dur="0.4s" fill="freeze"/>
    <text x="20" y="{y_spec}" font-family="Consolas, monospace" font-size="12" font-weight="bold" fill="#00bfff">{key}:</text>
    <text x="100" y="{y_spec}" font-family="Consolas, monospace" font-size="12" fill="#c9d1d9">{value}</text>
  </g>"""
    y_spec += 25

# Nodes config for the blueprint (coordinates customized for beautiful 3D flowchart aesthetics)
NODES = [
    # (id, label, x, y, width, height, type: root, child)
    ("root", "Repositories", 440, 360, 140, 34, "root"),
    ("p1", "Projects", 330, 440, 100, 30, "child"),
    ("p2", "Breaking Dependabot", 460, 440, 160, 30, "child"),
    ("p3", "Flutanko", 650, 440, 100, 30, "child"),
    
    ("c1", "Secure Layout", 300, 520, 120, 30, "child"),
    ("c2", "Cools Repository", 450, 520, 140, 30, "child"),
    ("c3", "Project Node", 620, 520, 120, 30, "child"),
    ("c4", "Enterprise AI Platform", 770, 520, 160, 30, "child"),
    
    ("s1", "Secure IoT", 350, 600, 110, 30, "child"),
    ("s2", "Docker Integration", 530, 600, 150, 30, "child"),
    ("s3", "AI Agent System", 710, 600, 140, 30, "child"),
]

nodes_markup = ""
paths_markup = ""
pulses_markup = ""

# Draw Connections (Paths)
# Root -> level 1
paths_markup += f'<path d="M 510 394 L 510 415 L 380 415 L 380 440" fill="none" stroke="#0077ff" stroke-width="1.5" opacity="0.6"/>'
paths_markup += f'<path d="M 510 394 L 510 440" fill="none" stroke="#00ffff" stroke-width="2" opacity="0.8"/>'
paths_markup += f'<path d="M 510 394 L 510 415 L 700 415 L 700 440" fill="none" stroke="#0077ff" stroke-width="1.5" opacity="0.6"/>'

# animate points on level 1 links
pulses_markup += """
<circle r="3" fill="#ffffff">
  <animateMotion path="M 510 394 Q 510 415 380 415 L 380 440" dur="4s" repeatCount="indefinite"/>
</circle>
<circle r="3" fill="#ffffff">
  <animateMotion path="M 510 394 L 510 440" dur="3s" repeatCount="indefinite"/>
</circle>
<circle r="3" fill="#ffffff">
  <animateMotion path="M 510 394 Q 510 415 700 415 L 700 440" dur="5s" repeatCount="indefinite"/>
</circle>
"""

# Level 1 -> level 2
connections_l1_l2 = [
    # (from_x, from_y, to_x, to_y)
    (380, 470, 360, 520),
    (380, 470, 520, 520),
    (540, 470, 520, 520),
    (540, 470, 680, 520),
    (700, 470, 680, 520),
    (700, 470, 850, 520)
]
for fx, fy, tx, ty in connections_l1_l2:
    paths_markup += f'<path d="M {fx} {fy} L {fx} {fy+15} L {tx} {fy+15} L {tx} {ty}" fill="none" stroke="#0055aa" stroke-dasharray="3 3" stroke-width="1"/>'

# Level 2 -> level 3
connections_l2_l3 = [
    (360, 550, 405, 600),
    (520, 550, 405, 600),
    (520, 550, 605, 600),
    (680, 550, 605, 600),
    (680, 550, 780, 600),
    (850, 550, 780, 600)
]
for fx, fy, tx, ty in connections_l2_l3:
    paths_markup += f'<path d="M {fx} {fy} L {tx} {ty}" fill="none" stroke="#0077ff" stroke-width="1.2" opacity="0.7"/>'
    pulses_markup += f"""
<circle r="2.5" fill="#00ffff">
  <animateMotion path="M {fx} {fy} L {tx} {ty}" dur="{3.5 + (fx%3)}s" repeatCount="indefinite"/>
</circle>"""

# Render Node Boxes
for n in NODES:
    nx, ny, nw, nh, nt = n[2], n[3], n[4], n[5], n[6]
    label = n[1]
    
    stroke_col = "#00ffff" if nt == "root" else "#0077ff"
    glow_col = "drop-shadow(0px 0px 6px rgba(0,255,255,0.7))" if nt == "root" else "drop-shadow(0px 0px 4px rgba(0,119,255,0.4))"
    b_fill = "#081b33" if nt == "root" else "#071224"
    
    # Text colors
    t_col = "#ffffff" if nt == "root" else "#afd7ff"
    
    # Add a glowing micro-chassis effect
    nodes_markup += f"""
  <!-- Node: {label} -->
  <g transform="translate({nx}, {ny})">
    <rect width="{nw}" height="{nh}" rx="6" fill="{b_fill}" stroke="{stroke_col}" stroke-width="1.2" style="filter: {glow_col};" opacity="0.9"/>
    <text x="{nw//2}" y="{nh//2 + 4}" font-family="Outfit, Inter, sans-serif" font-size="10.5" font-weight="bold" fill="{t_col}" text-anchor="middle">{label}</text>
  </g>"""

# High-tech floating badges with tags on the side
badges_str = """
  <!-- Badge: RAG -->
  <g transform="translate(850, 100)">
    <rect x="0" y="0" width="70" height="24" rx="12" fill="#091d36" stroke="#00f0ff" stroke-width="1" style="filter: drop-shadow(0px 0px 4px rgba(0,240,255,0.5));"/>
    <circle cx="12" cy="12" r="4" fill="#00f0ff">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite" />
    </circle>
    <text x="42" y="16" font-family="Outfit, sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">RAG</text>
    <line x1="0" y1="12" x2="-40" y2="40" stroke="#00f0ff" stroke-width="0.8" stroke-dasharray="2 3"/>
  </g>
  
  <!-- Badge: LLMs -->
  <g transform="translate(870, 160)">
    <rect x="0" y="0" width="70" height="24" rx="12" fill="#091d36" stroke="#9d00ff" stroke-width="1" style="filter: drop-shadow(0px 0px 4px rgba(157,0,255,0.5));"/>
    <circle cx="12" cy="12" r="4" fill="#9d00ff">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="2.5s" repeatCount="indefinite" />
    </circle>
    <text x="42" y="16" font-family="Outfit, sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">LLMs</text>
    <line x1="0" y1="12" x2="-60" y2="10" stroke="#9d00ff" stroke-width="0.8" stroke-dasharray="2 3"/>
  </g>

  <!-- Badge: LangGraph -->
  <g transform="translate(860, 220)">
    <rect x="0" y="0" width="85" height="24" rx="12" fill="#091d36" stroke="#ff007f" stroke-width="1" style="filter: drop-shadow(0px 0px 4px rgba(255,0,127,0.5));"/>
    <circle cx="12" cy="12" r="4" fill="#ff007f">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="1.8s" repeatCount="indefinite" />
    </circle>
    <text x="49" y="16" font-family="Outfit, sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">LangGraph</text>
    <line x1="0" y1="12" x2="-50" y2="-10" stroke="#ff007f" stroke-width="0.8" stroke-dasharray="2 3"/>
  </g>

  <!-- Badge: AWS Basics -->
  <g transform="translate(770, 275)">
    <rect x="0" y="0" width="85" height="24" rx="12" fill="#091d36" stroke="#ffaa00" stroke-width="1" style="filter: drop-shadow(0px 0px 4px rgba(255,170,0,0.5));"/>
    <circle cx="12" cy="12" r="4" fill="#ffaa00">
      <animate attributeName="opacity" values="0.3;1;0.3" dur="2.2s" repeatCount="indefinite" />
    </circle>
    <text x="49" y="16" font-family="Outfit, sans-serif" font-size="10" font-weight="bold" fill="#ffffff" text-anchor="middle">AWS Basics</text>
  </g>
"""

# Cartridge Slot Board Grid (Pins / Cartridges)
pins_markup = """
  <!-- Motherboard cartridges design at bottom left panel -->
  <g transform="translate(25, 520)">
    <rect width="250" height="330" rx="10" fill="#060c17" stroke="#122542" stroke-width="1.5"/>
    <text x="15" y="27" font-family="Outfit, sans-serif" font-size="14" font-weight="bold" fill="#00ffff" style="filter: drop-shadow(0px 0px 3px #00ffff);">[ Motherboard Pins ]</text>
    <line x1="15" y1="36" x2="235" y2="36" stroke="#122542" stroke-width="1"/>
    
    <!-- Slots -->
    <!-- Cartridge 1 -->
    <g transform="translate(15, 50)">
      <rect width="220" height="50" rx="5" fill="#0b172a" stroke="#0077ff" stroke-width="1"/>
      <circle cx="20" cy="25" r="5" fill="#00ff00"/>
      <text x="40" y="22" font-family="Outfit, sans-serif" font-size="11" font-weight="bold" fill="#ffffff">Enterprise AI Platform</text>
      <text x="40" y="38" font-family="Consolas, monospace" font-size="9" fill="#00bfff">PORT_01 // SECURE_LINK</text>
      <!-- Glowing active pulse -->
      <line x1="210" y1="10" x2="210" y2="40" stroke="#00ff00" stroke-width="2"/>
    </g>

    <!-- Cartridge 2 -->
    <g transform="translate(15, 115)">
      <rect width="220" height="50" rx="5" fill="#0b172a" stroke="#0077ff" stroke-width="1"/>
      <circle cx="20" cy="25" r="5" fill="#00ff00"/>
      <text x="40" y="22" font-family="Outfit, sans-serif" font-size="11" font-weight="bold" fill="#ffffff">Secure IoT Platform</text>
      <text x="40" y="38" font-family="Consolas, monospace" font-size="9" fill="#00bfff">PORT_02 // AGENT_ONLINE</text>
      <line x1="210" y1="10" x2="210" y2="40" stroke="#00ff00" stroke-width="2"/>
    </g>

    <!-- Cartridge 3 -->
    <g transform="translate(15, 180)">
      <rect width="220" height="50" rx="5" fill="#0b172a" stroke="#0077ff" stroke-width="1"/>
      <circle cx="20" cy="25" r="5" fill="#ffbb00">
        <animate attributeName="opacity" values="0.4;1;0.4" dur="1.5s" repeatCount="indefinite"/>
      </circle>
      <text x="40" y="22" font-family="Outfit, sans-serif" font-size="11" font-weight="bold" fill="#ffffff">Cybersecurity Solutions</text>
      <text x="40" y="38" font-family="Consolas, monospace" font-size="9" fill="#ffbb00">PORT_03 // SCANNERS_STANDBY</text>
      <line x1="210" y1="10" x2="210" y2="40" stroke="#ffbb00" stroke-width="2"/>
    </g>

    <!-- Cartridge 4 -->
    <g transform="translate(15, 245)">
      <rect width="220" height="50" rx="5" fill="#0b172a" stroke="#0077ff" stroke-width="1"/>
      <circle cx="20" cy="25" r="5" fill="#00ff00"/>
      <text x="40" y="22" font-family="Outfit, sans-serif" font-size="11" font-weight="bold" fill="#ffffff">LangGraph Multi-Agents</text>
      <text x="40" y="38" font-family="Consolas, monospace" font-size="9" fill="#00bfff">PORT_04 // GRAPH_DEPLOYED</text>
      <line x1="210" y1="10" x2="210" y2="40" stroke="#00ff00" stroke-width="2"/>
    </g>
  </g>
"""

# Grid pattern background
grid_pattern = """
  <defs>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#0c182e" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#grid)" />
"""

# Let's compile the whole SVG template
svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="950"
     height="900"
     viewBox="0 0 950 900"
     fill="none">
  
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&amp;display=swap');
    
    .glow-card {{
      filter: drop-shadow(0px 0px 10px rgba(0, 119, 255, 0.15));
    }}
    .circle-scan {{
      transform-origin: 140px 140px;
    }}
  </style>

  <!-- Background Chassis -->
  <rect width="100%" height="100%" rx="15" fill="#030712" stroke="#122542" stroke-width="2"/>
  
  <!-- Subtle technical grid background -->
  {grid_pattern}

  <!-- ================= LEFT COLUMN ================= -->
  <g class="glow-card" transform="translate(15, 15)">
    <!-- Glass Panel Background -->
    <rect width="280" height="870" rx="16" fill="#070c17" fill-opacity="0.8" stroke="#172b4d" stroke-width="1.5"/>
    
    <!-- Holographic Scanner Target circles for Avatar -->
    <g class="circle-scan">
      <!-- Rotator 1 -->
      <circle cx="140" cy="140" r="72" fill="none" stroke="#00ffff" stroke-dasharray="12 8" stroke-width="1.5">
        <animateTransform attributeName="transform" type="rotate" from="0 140 140" to="360 140 140" dur="18s" repeatCount="indefinite"/>
      </circle>
      <!-- Rotator 2 -->
      <circle cx="140" cy="140" r="80" fill="none" stroke="#0077ff" stroke-dasharray="5 15" stroke-width="1">
        <animateTransform attributeName="transform" type="rotate" from="360 140 140" to="0 140 140" dur="24s" repeatCount="indefinite"/>
      </circle>
      <!-- Tech overlay scanner elements -->
      <circle cx="140" cy="140" r="62" fill="none" stroke="#ff007f" stroke-width="1" stroke-opacity="0.5"/>
      <!-- Crosshairs -->
      <path d="M 140 50 L 140 65 M 140 215 L 140 230 M 50 140 L 65 140 M 215 140 L 230 140" stroke="#00ffff" stroke-width="1" opacity="0.6"/>
    </g>

    <!-- Avatar Image (Profile picture of the user) -->
    <defs>
      <clipPath id="avatar-clip">
        <circle cx="140" cy="140" r="58"/>
      </clipPath>
    </defs>
    <image href="data:image/jpeg;base64,{photo_b64}" x="75" y="75" width="130" height="130" clip-path="url(#avatar-clip)" preserveAspectRatio="xMidYMid slice"/>

    <!-- User Information Info Card display -->
    <text x="140" y="255" font-family="'Outfit', sans-serif" font-weight="800" font-size="18" fill="#ffffff" text-anchor="middle">Mohammed Furqan</text>
    <text x="140" y="278" font-family="'Outfit', sans-serif" font-weight="700" font-size="17" fill="#ffffff" text-anchor="middle">Abdul Rahman Patel</text>
    <text x="140" y="302" font-family="Consolas, monospace" font-size="11.5" fill="#00e5ff" text-anchor="middle">furqanabdulrahman-65 • he/him</text>
    <line x1="30" y1="318" x2="250" y2="318" stroke="#172b4d" stroke-width="1"/>

    <!-- Bio descriptions -->
    <g transform="translate(20, 335)" font-family="'Outfit', sans-serif" font-size="11" fill="#afd7ff">
      <rect width="240" height="150" rx="8" fill="#0a1224" stroke="#122542" stroke-width="1"/>
      <text x="15" y="25" font-weight="700" fill="#00ffcc" font-size="11">PROFILE CLASSIFICATION</text>
      
      <text x="15" y="55" font-weight="750" fill="#ffffff">• PYTHON DEVELOPER</text>
      <text x="15" y="75" font-weight="750" fill="#ffffff">• AI/ML SPECIALIST</text>
      <text x="15" y="95" font-weight="750" fill="#ffffff">• SECURE INTEL SOLUTIONS</text>
      <text x="15" y="115" font-weight="750" fill="#ffffff">• IOT &amp; CYBERSECURITY</text>
      <text x="15" y="135" font-weight="750" fill="#ffffff">• OPEN SOURCE COLLABORATOR</text>
    </g>

    <!-- Pins cartridges inside Left panel -->
    {pins_markup}
  </g>

  <!-- ================= RIGHT COLUMN ================= -->
  
  <!-- Sub-column 1: Portrait Terminal (x: 310, y: 15, width: 300, height: 320) -->
  <g class="glow-card" transform="translate(310, 15)">
    <rect width="300" height="320" rx="12" fill="#070c17" fill-opacity="0.8" stroke="#172b4d" stroke-width="1.5"/>
    <!-- Terminal Title bar -->
    <g>
      <circle cx="18" cy="18" r="5" fill="#ff5f56" />
      <circle cx="33" cy="18" r="5" fill="#ffbd2e" />
      <circle cx="48" cy="18" r="5" fill="#27c93f" />
      <text x="150" y="18" font-family="Consolas, monospace" font-size="11" fill="#8b949e" text-anchor="middle" dominant-baseline="middle">furqan@portrait:~</text>
      <line x1="0" y1="36" x2="300" y2="36" stroke="#172b4d" stroke-width="1"/>
    </g>
    
    <!-- ASCII Animations defs & content -->
    <defs>
      {clips_str}
    </defs>
    {texts_str}
    {cursor_str}
  </g>

  <!-- Sub-column 2: Specs Terminal (x: 625, y: 15, width: 310, height: 320) -->
  <g class="glow-card" transform="translate(625, 15)">
    <rect width="310" height="320" rx="12" fill="#070c17" fill-opacity="0.8" stroke="#172b4d" stroke-width="1.5"/>
    <!-- Terminal Title bar -->
    <g>
      <circle cx="18" cy="18" r="5" fill="#ff5f56" />
      <circle cx="33" cy="18" r="5" fill="#ffbd2e" />
      <circle cx="48" cy="18" r="5" fill="#27c93f" />
      <text x="155" y="18" font-family="Consolas, monospace" font-size="11" fill="#8b949e" text-anchor="middle" dominant-baseline="middle">furqan@terminal:~</text>
      <line x1="0" y1="36" x2="310" y2="36" stroke="#172b4d" stroke-width="1"/>
    </g>
    
    <!-- Title brand -->
    <g transform="translate(0, 0)">
      <text x="20" y="52" font-family="Consolas, monospace" font-size="14" font-weight="bold" fill="#00ffaa">furqan@github</text>
    </g>
    <!-- Dynamic specs strings -->
    {specs_str}
    
    <!-- Terminal shell blinking prompt -->
    <g transform="translate(20, 280)">
      <text x="0" y="0" font-family="Consolas, monospace" font-size="12" fill="#8b949e">furqan@terminal:~$ </text>
      <rect x="140" y="-11" width="7" height="13" fill="#00ffaa">
        <animate attributeName="opacity" values="0;1;0;1" keyTimes="0;0.5;0.51;1" dur="0.8s" repeatCount="indefinite" />
      </rect>
    </g>
  </g>

  <!-- ================= BLUEPRINT FLOW SECTION ================= -->
  
  <!-- Graphic cyber circuit board backing representation -->
  <g transform="translate(310, 350)">
    <!-- Circuit Border Panel enclosing blueprint -->
    <rect width="625" height="535" rx="15" fill="#040914" fill-opacity="0.9" stroke="#172b4d" stroke-width="1.5"/>
    <text x="25" y="27" font-family="'Outfit', sans-serif" font-size="14" font-weight="bold" fill="#00bfff" style="filter: drop-shadow(0px 0px 3px #00bfff);">[ Holographic System Blueprint ]</text>
    <line x1="25" y1="38" x2="600" y2="38" stroke="#172b4d" stroke-width="1"/>
  </g>
  
  <!-- Diagram paths connections & node buttons logic -->
  <g>
    <!-- Glowing pulse circles & pathways -->
    {paths_markup}
    {pulses_markup}
    
    <!-- Render node blocks -->
    {nodes_markup}
    
    <!-- Floating badges tags -->
    {badges_str}
  </g>
  
</svg>
"""

# Output file
with open(output_path, "w", encoding="utf-8") as f:
    f.write(svg_content)

print(f"Holographic Profile Dashboard SVG generated successfully at {output_path}!")
