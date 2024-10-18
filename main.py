from credentials import *
import datetime
import requests
from icalendar import Calendar

def fetch_ics_calendar_items(url, username, password):
    response = requests.get(url, auth=(username, password))
    response.raise_for_status()
    calendar = Calendar.from_ical(response.content)
    items = []
    for component in calendar.walk():
        if component.name == "VEVENT":
            name = component.get("SUMMARY")
            date = component.get("DTSTART").dt.strftime("%Y-%m-%d")
            location = component.get("LOCATION", "unknown")
            items.append({"name": name, "date": date, "location": location})
    return items

def parse_calendar_items(calendar_items):
    # Parse calendar items for people names
    people = {}
    for item in calendar_items:
        name = item["name"]
        date = item["date"]
        location = item["location"]
        if name not in people:
            people[name] = []
        people[name].append({"date": date, "location": location})
    return people

def determine_presence(people):
    # Determine whether people are at the office or not
    presence = {}
    for name, items in people.items():
        presence[name] = []
        for item in items:
            date = item["date"]
            location = item["location"]
            if location == "office":
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
    url = "https://nextcloud.example.com/remote.php/dav/calendars/user/calendar.ics"
    username = "your_username"
    password = "your_password"
    calendar_items = fetch_ics_calendar_items(url, username, password)
    people = parse_calendar_items(calendar_items)
    presence = determine_presence(people)
    display_presence_overview(presence)
