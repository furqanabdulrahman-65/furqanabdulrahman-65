import os
import requests
from bs4 import BeautifulSoup
import json

USERNAME = "furqanabdulrahman-65"
URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch():
    print(f"Fetching contributions for {USERNAME}...")
    response = requests.get(URL)
    
    if response.status_code != 200:
        print(f"Error fetching contributions: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Map each tooltip "for" target to the parsed count
    id_to_count = {}
    for tip in soup.find_all("tool-tip"):
        target_id = tip.get("for")
        if target_id:
            text = tip.text.strip()
            # Expecting string like "8 contributions on May 10th." or "No contributions on..."
            count = 0
            parts = text.split()
            if parts and parts[0].isdigit():
                count = int(parts[0])
            id_to_count[target_id] = count

    # Scrape all contribution cells that have a data-date
    days_list = []
    cells = soup.find_all("td", class_="ContributionCalendar-day")
    for cell in cells:
        date_str = cell.get("data-date")
        if date_str:
            level = int(cell.get("data-level", 0))
            cell_id = cell.get("id")
            count = id_to_count.get(cell_id, 0)
            
            days_list.append({
                "date": date_str,
                "level": level,
                "count": count
            })

    # Sort days chronologically
    days_list.sort(key=lambda d: d["date"])

    # Calculate stats
    total_contributions = sum(d["count"] for d in days_list)
    longest_streak = 0
    current_streak = 0
    best_day = "N/A"
    best_count = -1
    
    # Longest streak & best day
    temp_streak = 0
    for d in days_list:
        cnt = d["count"]
        dt = d["date"]
        
        if cnt > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0
            
        if cnt > best_count:
            best_count = cnt
            best_day = f"{dt} ({cnt} contributions)"

    # Current streak
    n = len(days_list)
    start_idx = -1
    if n > 0 and days_list[n-1]["count"] > 0:
        start_idx = n - 1
    elif n > 1 and days_list[n-2]["count"] > 0:
        start_idx = n - 2

    if start_idx != -1:
        for i in range(start_idx, -1, -1):
            if days_list[i]["count"] > 0:
                current_streak += 1
            else:
                break

    # Monthly totals
    monthly_totals = {}
    for d in days_list:
        ym = d["date"][:7] # YYYY-MM
        monthly_totals[ym] = monthly_totals.get(ym, 0) + d["count"]

    stats = {
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "monthly_totals": monthly_totals
    }

    # Resolve paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), "data")
    os.makedirs(data_dir, exist_ok=True)
    
    output_path = os.path.join(data_dir, "contributions.json")
    
    output_data = {
        "stats": stats,
        "days": days_list
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"Saved stats and {len(days_list)} days details to {output_path}")


if __name__ == "__main__":
    fetch()