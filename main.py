from credentials import *
import datetime

def fetch_calendar_items():
    # Placeholder function to fetch items from the zfdm calendar
    # Replace with actual implementation
    return [
        {"name": "Alice", "date": "2023-04-01", "location": "office"},
        {"name": "Bob", "date": "2023-04-02", "location": "home"},
        {"name": "Charlie", "date": "2023-04-03", "location": "office"},
        {"name": "Alice", "date": "2023-04-04", "location": "home"},
        {"name": "Bob", "date": "2023-04-05", "location": "office"},
    ]

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
    calendar_items = fetch_calendar_items()
    people = parse_calendar_items(calendar_items)
    presence = determine_presence(people)
    display_presence_overview(presence)
