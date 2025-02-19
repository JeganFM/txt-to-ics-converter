# txt-to-ics-converter
A Lazy mans way of add events to Google Calendar and Apple Calendar.
# Text to ICS Converter

A Python script that converts structured and freeform text into `.ics` calendar files for Google Calendar and iCalendar.

## Features
- Supports structured event format
- Parses freeform text to extract event details
- Generates `.ics` files for easy import into calendars  


Structured Format example:
Event: Cybersecurity Conference
Date: 2025-03-10
Time: 09:00 - 17:00
Location: London Tech Hub
Description: Discuss the latest in cybersecurity trends. 

Freeform Example:
On March 15, I'll be meeting with the networking team at 2 PM to discuss the security architecture.
The discussion will take place at the downtown office.

Company annual retreat is planned for April 5th at 10 AM. Everyone should be ready!


## Installation
Clone the repository and install dependencies:

```sh
git clone https://github.com/yourusername/txt-to-ics-converter.git
cd txt-to-ics-converter
pip install -r requirements.txt
