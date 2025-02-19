import re
from dateutil import parser
from datetime import datetime, timedelta
from ics import Calendar, Event

def parse_events(file_path):
    """Reads a text file and extracts events from structured and freeform formats."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    event_blocks = content.strip().split("\n\n")  # Separate events by blank lines
    events = []

    for block in event_blocks:
        lines = block.split("\n")
        event_details = {}

        structured = False  # Flag to check if structured format is found

        for line in lines:
            match = re.match(r'^(Event|Date|Time|Location|Description): (.+)', line)
            if match:
                key, value = match.groups()
                event_details[key] = value.strip()
                structured = True

        if structured and "Date" in event_details and "Time" in event_details:
            # Parse structured format
            start_time, end_time = event_details["Time"].split(" - ")
            start_dt = datetime.strptime(event_details["Date"] + " " + start_time, "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(event_details["Date"] + " " + end_time, "%Y-%m-%d %H:%M")

            event = Event()
            event.name = event_details.get("Event", "Unnamed Event")
            event.begin = start_dt
            event.end = end_dt
            event.location = event_details.get("Location", "")
            event.description = event_details.get("Description", "")
            events.append(event)

        else:
            # Attempt to extract event details from freeform text
            extracted_event = extract_event_from_text(block)
            if extracted_event:
                events.append(extracted_event)

    return events

def extract_event_from_text(text):
    """Extracts event details from freeform text using date parsing."""
    sentences = text.replace("\n", " ").split(". ")  # Split by period or newline

    event_name = "General Event"  # Default event name
    event_location = ""
    event_description = text

    # Extract date and time using fuzzy date parsing
    start_dt, end_dt = None, None

    for sentence in sentences:
        try:
            dt = parser.parse(sentence, fuzzy=True, ignoretz=True, default=datetime.now())
            if not start_dt:
                start_dt = dt
            else:
                end_dt = dt
                break  # Stop after finding an end time
        except ValueError:
            continue

    if not start_dt:
        return None  # Skip event if no date is found

    # Set a default duration of 1 hour if no end time is detected
    if not end_dt or end_dt.date() != start_dt.date():
        end_dt = start_dt + timedelta(hours=1)

    event = Event()
    event.name = event_name
    event.begin = start_dt
    event.end = end_dt
    event.location = event_location
    event.description = event_description

    return event

def create_ics_file(events, output_file="events.ics"):
    """Creates an ICS file from extracted events."""
    calendar = Calendar()
    
    for event in events:
        calendar.events.add(event)

    with open(output_file, "w", encoding="utf-8") as file:
        file.writelines(calendar)

    print(f"ICS file '{output_file}' created successfully with {len(events)} events!")

if __name__ == "__main__":
    txt_file = "events.txt"  # Txt file needed
    events = parse_events(txt_file)
    
    if events:
        create_ics_file(events)
    else:
        print("No valid events found.")
