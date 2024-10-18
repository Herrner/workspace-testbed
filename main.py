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
            start_date = component.get("DTSTART").dt.strftime("%Y-%m-%d")
            end_date = component.get("DTEND").dt.strftime("%Y-%m-%d")
            location = component.get("LOCATION", "unknown")
            items.append(
                {
                    "name": name,
                    "start_date": start_date,
                    "end_date": end_date,
                    "location": location,
                }
            )
    return items


def read_names_from_file(file_path):
    with open(file_path, "r") as file:
        names = [line.strip() for line in file.readlines()]
    return names


def parse_calendar_items(calendar_items, names):
    # Parse calendar items for people names
    people = {}
    for name in names:
        people[name] = []

    for item in calendar_items:
        title = item["name"]
        start_date = datetime.datetime.strptime(item["start_date"], "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(item["end_date"], "%Y-%m-%d").date()
        date_range = (end_date - start_date).days
        for i in range(date_range):
            date = (start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            for name in names:
                if name in title:
                    people[name].append({"date": date})
    return people


def determine_absence(people):
    # Determine whether people are at the office or not
    absence = {}
    for name, items in people.items():
        for item in items:
            date = item["date"]
            if date not in absence:
                absence[date] = []
            absence[date].append(name)
    return absence


def display_presence_overview(absence, names):
    # Display the presence information for the next two weeks
    today = datetime.date.today()
    two_weeks_later = today + datetime.timedelta(days=14)
    print("Presence overview for the next two weeks:")
    for date in (today + datetime.timedelta(days=i) for i in range(15)):
        # exclude weekends
        if date.weekday() >= 5:
            continue
        else:
            date_str = date.strftime("%Y-%m-%d")
            print(date.strftime("%A, %d. %B %Y") + ": ", end="")
            if date_str not in absence:
                print("Alle da!")
            else:
                present_names = [
                    name for name in names if name not in absence[date_str]
                ]
                print(", ".join(present_names))


if __name__ == "__main__":
    names = read_names_from_file("credentials/names.txt")
    calendar_items = fetch_ics_calendar_items(url)
    people = parse_calendar_items(calendar_items, names)
    absence = determine_absence(people)
    display_presence_overview(absence, names)
