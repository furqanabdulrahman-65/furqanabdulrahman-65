import requests
from bs4 import BeautifulSoup
import json


USERNAME = "furqanabdulrahman-65"


URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch():

    print("Fetching contributions...")


    response = requests.get(URL)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )


    days = []


    for cell in soup.select(
        "td.ContributionCalendar-day"
    ):

        days.append({

            "date": cell.get("data-date"),

            "level": int(
                cell.get(
                    "data-level",
                    0
                )
            )

        })


    with open(
        "../contributions.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            days,
            f,
            indent=2
        )


    print(
        f"Saved {len(days)} days"
    )


fetch()