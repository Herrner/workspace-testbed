from credentials.calendars import url
import datetime
import requests
from icalendar import Calendar


def fetch_ics_calendar_items(url):
    response = requests.get(url)
    print(f"Fetching URL: {url}")
    print(f"Status Code: {response.status_code}")
    response.raise_for_status()
    calendar = Calendar.from_ical(response.content)
    items = []
    for component in calendar.walk():
        if component.name == "VEVENT":
            name = component.get("SUMMARY")
            print(name)
            start_date = component.get("DTSTART").dt.strftime("%Y-%m-%d")
            end_date = component.get("DTEND").dt.strftime("%Y-%m-%d")
            location = component.get("LOCATION", "unknown")
            items.append({"name": name, "start_date": start_date, "end_date": end_date, "location": location})
    return items


def read_names_from_file(file_path):
    with open(file_path, "r") as file:
        names = [line.strip() for line in file.readlines()]
    return names


def parse_calendar_items(calendar_items, names):
    # Parse calendar items for people names
    people = {}
    for item in calendar_items:
        name = item["name"]
        start_date = datetime.datetime.strptime(item["start_date"], "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(item["end_date"], "%Y-%m-%d").date()
        date_range = (end_date - start_date).days
        for i in range(date_range):
            date = (start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            if any(name.startswith(n) for n in names):
                if name not in people:
                    people[name] = []
                people[name].append({"date": date})
    return people


def determine_presence(people):
    # Determine whether people are at the office or not
    presence = {}
    for name, items in people.items():
        for item in items:
            date = item["date"]
            if date not in presence:
                presence[date] = []
            presence[date].append(name)
    return presence


def display_presence_overview(presence):
    # Display the presence information for the next two weeks
    today = datetime.date.today()
    two_weeks_later = today + datetime.timedelta(days=14)
    print("Presence overview for the next two weeks:")
    for date in (today + datetime.timedelta(days=i) for i in range(15)):
        date_str = date.strftime("%Y-%m-%d")
        if date_str in presence:
            print(f"{date_str}:")
            for name in presence[date_str]:
                print(f"  - {name}")
        else:
            print(f"{date_str}: (nobody)")


if __name__ == "__main__":
    names = read_names_from_file("credentials/names.txt")
    calendar_items = fetch_ics_calendar_items(url)
    people = parse_calendar_items(calendar_items, names)
    presence = determine_presence(people)
    display_presence_overview(presence)
