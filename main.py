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
            date = component.get("DTSTART").dt.strftime("%Y-%m-%d")
            location = component.get("LOCATION", "unknown")
            items.append({"name": name, "date": date, "location": location})
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
        date = item["date"]
        if any(name.startswith(n) for n in names):
            if name not in people:
                people[name] = []
            people[name].append({"date": date})
    return people


def determine_presence(people):
    # Determine whether people are at the office or not
    presence = {}
    for name, items in people.items():
        presence[name] = []
        for item in items:
            date = item["date"]
            presence[name].append(date)
    return presence


def display_presence_overview(presence):
    # Display the presence information for the next two weeks
    today = datetime.date.today()
    two_weeks_later = today + datetime.timedelta(days=14)
    print("Presence overview for the next two weeks:")
    for name, dates in presence.items():
        print(f"{name}:")
        for date in dates:
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            if today <= date_obj <= two_weeks_later:
                print(f"  - {date}")


if __name__ == "__main__":
    names = read_names_from_file("credentials/names.txt")
    calendar_items = fetch_ics_calendar_items(url)
    people = parse_calendar_items(calendar_items, names)
    presence = determine_presence(people)
    display_presence_overview(presence)
