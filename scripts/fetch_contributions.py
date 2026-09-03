from pathlib import Path
import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone


# ==========================================
# CONFIGURATION
# ==========================================

USERNAME = "SergeantYeet"

OUTPUT = Path("data/contributions.json")

URL = f"https://github.com/users/SergeantYeet/contributions"


# ==========================================
# FETCH GITHUB CONTRIBUTION CALENDAR
# ==========================================

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    URL,
    headers=headers,
    timeout=30
)

response.raise_for_status()

soup = BeautifulSoup(
    response.text,
    "html.parser"
)


# ==========================================
# EXTRACT CONTRIBUTION DAYS
# ==========================================

days = []

for cell in soup.select("td.ContributionCalendar-day"):

    date = cell.get("data-date")

    if not date:
        continue

    count = 0

    # GitHub's contribution cells contain
    # the contribution count in an aria-label.
    label = cell.get("aria-label", "")

    match = re.search(
        r"(\d[\d,]*) contribution",
        label
    )

    if match:
        count = int(
            match.group(1).replace(",", "")
        )

    level = cell.get(
        "data-level",
        "0"
    )

    days.append({
        "date": date,
        "count": count,
        "level": int(level)
    })


# ==========================================
# CALCULATE BASIC STATISTICS
# ==========================================

days.sort(
    key=lambda x: x["date"]
)


# Current streak
current_streak = 0

for day in reversed(days):

    if day["count"] > 0:
        current_streak += 1
    else:
        break


# Longest streak
longest_streak = 0
streak = 0

for day in days:

    if day["count"] > 0:
        streak += 1
        longest_streak = max(
            longest_streak,
            streak
        )
    else:
        streak = 0


# Best day
best_day = max(
    days,
    key=lambda x: x["count"],
    default=None
)


# Total contributions
total = sum(
    day["count"]
    for day in days
)


# ==========================================
# SAVE JSON
# ==========================================

OUTPUT.parent.mkdir(
    parents=True,
    exist_ok=True
)

data = {
    "username": USERNAME,
    "generated_at": datetime.now(
        timezone.utc
    ).isoformat(),

    "total": total,

    "current_streak": current_streak,

    "longest_streak": longest_streak,

    "best_day": best_day,

    "days": days
}


OUTPUT.write_text(
    json.dumps(
        data,
        indent=2
    ),
    encoding="utf-8"
)


print(
    f"Fetched {len(days)} contribution days"
)

print(
    f"Total contributions: {total}"
)

print(
    f"Current streak: {current_streak}"
)

print(
    f"Longest streak: {longest_streak}"
)

print(
    f"Wrote {OUTPUT}"
)