import os
import json

# Define the colors ramp (from none to brightest green)
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "../data/contributions.json")
    output_path = os.path.join(current_dir, "../contrib-heatmap.svg")

    if not os.path.exists(json_path):
        print(f"Error: contributions data not found at {json_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    stats = data["stats"]
    days = data["days"]

    # Dimensions
    WIDTH = 860
    HEIGHT = 185

    x_offset = 87
    y_offset = 40
    cell_size = 10
    cell_gap = 3

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="{WIDTH}"
     height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}">
  <style>
    .month-text {{ font-family: Consolas, monospace; font-size: 10px; fill: #8b949e; }}
    .day-text {{ font-family: Consolas, monospace; font-size: 9px; fill: #8b949e; }}
    .stats-text {{ font-family: Consolas, monospace; font-size: 11px; fill: #c9d1d9; font-weight: bold; }}
    .legend-text {{ font-family: Consolas, monospace; font-size: 10px; fill: #8b949e; }}
  </style>

  <!-- Background card -->
  <rect width="100%" height="100%" rx="10" fill="#0d1117" stroke="#30363d" stroke-width="1.5" />

  <!-- Month labels -->
"""

    # Extract month labels
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    last_month = None
    for col in range(53):
        idx = col * 7
        if idx < len(days):
            dt = days[idx]["date"]
            m_idx = int(dt[5:7]) - 1
            m_name = months[m_idx]
            if m_name != last_month:
                x = x_offset + col * (cell_size + cell_gap)
                svg += f'  <text x="{x}" y="25" class="month-text">{m_name}</text>\n'
                last_month = m_name

    # Day labels
    day_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for label, row_idx in day_labels:
        y = y_offset + row_idx * (cell_size + cell_gap) + 8
        x = x_offset - 30
        svg += f'  <text x="{x}" y="{y}" class="day-text">{label}</text>\n'

    # Draw cells with delay-driven scale and translation animation
    for idx, day in enumerate(days):
        col = idx // 7
        row = idx % 7
        color_index = min(day["level"], len(PALETTE) - 1)
        color = PALETTE[color_index]

        x = x_offset + col * (cell_size + cell_gap)
        y = y_offset + row * (cell_size + cell_gap)

        # Diagonal delay calculation
        delay = (col + row) * 0.012

        svg += f"""  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}" opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.25s" fill="freeze" />
    <animateTransform attributeName="transform" type="translate" from="0 -4" to="0 0" begin="{delay:.3f}s" dur="0.25s" fill="freeze" />
  </rect>\n"""

    # Add spacing and footer details
    stats_y = 155
    total_cont = stats["total_contributions"]
    streak = stats["current_streak"]
    longest = stats["longest_streak"]
    stats_str = f"{total_cont:,} contributions in the last year | Current Streak: {streak} days | Longest: {longest} days"

    # Animated stats footer
    svg += f"""  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="0.8s" dur="0.4s" fill="freeze" />
    <text x="{x_offset}" y="{stats_y}" class="stats-text">{stats_str}</text>
  </g>\n"""

    # Animated legend
    legend_x = x_offset + 53 * 13 - 135
    svg += f"""  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="0.9s" dur="0.4s" fill="freeze" />
    <text x="{legend_x}" y="{stats_y}" class="legend-text">Less</text>
"""

    for i, color in enumerate(PALETTE[:5]):
        box_x = legend_x + 32 + i * 13
        box_y = stats_y - 9
        svg += f'    <rect x="{box_x}" y="{box_y}" width="10" height="10" rx="2" fill="{color}" />\n'

    svg += f"""    <text x="{legend_x + 32 + 5 * 13}" y="{stats_y}" class="legend-text">More</text>
  </g>
</svg>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)

    print(f"contrib-heatmap.svg created at {output_path}!")


if __name__ == "__main__":
    render()
