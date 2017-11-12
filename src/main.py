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
import sys

from apiclient.discovery import build
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow

import datetime

#client_id = 
#client_secret = 
#
#scope = 'https://www.googleapis.com/auth/calendar'
#
#flow = OAuth2WebServerFlow(client_id, client_secret, scope)

def setup():
    storage = Storage('credentials.dat')
    
    credentials = storage.get()
    
    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage, tools.argparser.parse_args())
        
    http = httplib2.Http()
    http = credentials.authorize(http)
    
    return http

class Events:
    # Shoud store a list of events. Currently, this is just a single event.
    
    def __init__(self, http):
        self.service = build('calendar', 'v3', http=http)
        self.events = []
                 
    def requestEvents(self, calendarId='primary', maxResults=100, singleEvents=True, timeMin=None):
        if timeMin is None:
            timeMin = datetime.datetime.utcnow().isoformat() + 'Z'
        
        self.response = self.service.events().list(calendarId='primary', timeMin=timeMin, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        
        for event in self.response.get('items', []):
            self.events.append({
                    'name':         event['summary'],
                    'startTime':    event['start'].get('dateTime', None),
                    'endTime':      event['end'].get('dateTime', None),
                    # Currently just uses the defaul colorId's as priority.
                    'priority':     event.get('colorId', None)
                    })

if __name__ == "__main__":
    http = setup()
    test = Events(http)
    test.requestEvents()
    print(test.events)