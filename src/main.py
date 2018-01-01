# TODO:
#
# - Write function to integrate with Google Calendar API and collect schedule data
# - Create an intelligently formatted data structure to store scheduled events and important metadata about each. See the next point.
# - Create a datastructure which stores tags/traits/past data and tie these to the above data structure.

# DESIRED FUNCTIONALITY:
# - The software should be able to return the number of 'usable' or 'productive' hours left in a given timespan, based on past behaviour (and maybe some science)
# - The software should be able to add new events to an existing Google Calendar
# - The software should be able to categorize inputted tasks (based on increasingly few inputs) and schedule an appropriate time for it based on past data

# Includes
import httplib2
from apiclient.discovery import build
import datetime

import authentication


def setup_http():

    credentials = authentication.get_credentials()

    http = httplib2.Http()
    http = credentials.authorize(http)

    return http

class calendarInstance:
    # Create a calendar instance for a user
    def __init__(self, http):
        self.service = build('calendar', 'v3', http=http)
        self.events = []

    def requestEvents(self, calendarId='primary', maxResults=10, singleEvents=True, timeMin=None):
        self.events = []
        # Request events from the calendar instance
        # Store key event details in a list with dictionary entries
        # Should this function delete previous event lists? Probably

        if timeMin is None:
            timeMin = datetime.datetime.utcnow().isoformat() + 'Z'

        response = self.service.events().list(calendarId=calendarId, timeMin=timeMin, maxResults=maxResults, singleEvents=singleEvents, orderBy='startTime').execute()

        for event in response.get('items', []):
            self.events.append({
                    'name':         event['summary'],
                    'startTime':    event['start'].get('dateTime', None),
                    'endTime':      event['end'].get('dateTime', None),
                    # Currently just uses the default colorId's as priority.
                    'priority':     event.get('colorId', None)
                    })

if __name__ == "__main__":
    test = calendarInstance(setup_http())
    test.requestEvents()
    for item in test.events:
        print(item)
