'''
    FILENAME:       calendar_handler.py
    DEPENDENCIES:
    DESCRIPTION:    Handles interfacing with a user's calendar and events
                    Implements the calendarInstance class
    AUTHORS:        Dylan Vogel & Google Calendar API documentation
    MODIFIED:       2018-1-1

    NOTE:           TODO: See todos in comments

 '''

import httplib2
import authentication
import event as eventClass
from apiclient.discovery import build

import datetime

def setup_http():
    # Create a http instance and authorize it with the user credentials
    credentials = authentication.get_credentials()

    http = httplib2.Http()
    http = credentials.authorize(http)

    return http

class calendarInstance:
    # Create a calendar instance for a user
    def __init__(self):
        http = setup_http()
        self.service = build('calendar', 'v3', http=http)
        self.events = []
        
    def __matchID(self, ID, array):
        # Return a list of events with a matching ID using list comprehension
        return [item for item in array if item.id == ID]
    
    def __updateLocalEvents(self, event):
        # Update the local copy of self.events
        # Separate function because it's used by both requestEvents and createEvent
        
        # self.events.append({
        #                 'name':         event['summary'],
        #                 'startTime':    event['start'].get('dateTime', None),
        #                 'endTime':      event['end'].get('dateTime', None),
        #                 'priority':     event.get('colorId', None), # Currently uses the default colorId's as priority.
        #                 'id':           event['id']
        #                 })
        
        self.events.append(eventClass.Event(event))
    

    def requestEvents(self, calendarId='primary', maxResults=10, singleEvents=True, timeMin=None):
        # Request events from the user's calendar
        # Store key event details in a list with dictionary entries
        

        # Generate current time for events request
        if timeMin is None:
            timeMin = datetime.datetime.utcnow().isoformat() + 'Z'

        # Ask Google Calendar for a list of events
        response = self.service.events().list(calendarId=calendarId, timeMin=timeMin, maxResults=maxResults, singleEvents=singleEvents, orderBy='startTime').execute()


        for event in response.get('items', []):
            # Check if an event with the same ID has already been loaded
            matches = self.__matchID(event['id'], self.events)
            if len(matches) > 0:
                continue;
                # TODO: check if the remote event has been updated more recently than the local copy, and make changes if so
            else:
                self.__updateLocalEvents(event)

    def __defaultTime(self):
        # Create default start and end times for testing the createEvent function
        timeZone = 'America/Toronto'

        # Create an event that starts now and lasts for an hour
        currTime = datetime.datetime.utcnow()
        oneHour = datetime.timedelta(hours=1)

        endTime = currTime + oneHour

        # Create the start and end dicts
        start = {
            'dateTime': currTime.isoformat() + 'Z',
            'timeZone': timeZone
            }
        end = {
            'dateTime': endTime.isoformat() + 'Z',
            'timeZone': timeZone
        }

        return start, end


    def createEvent(self, summary, start={}, end={}, location=None, description=None):
        # Add an event to the user's primary calendar
        # TODO: add more data fields
        
        # Google Calendar (understandably) doesn't seem to like it when start and end times aren't specified
        # However, it doesn't seem to care about missing timeZone information

        # Event starts now and lasts one hour
        defaultStart, defaultEnd = self.__defaultTime();

        # Fill in any missing values in start and end
        start = {
            'dateTime': start.get('dateTime', defaultStart['dateTime']),
            #'timeZone': start.get('timeZone', defaultStart['timeZone'])
            }
        end = {
            'dateTime': end.get('dateTime', defaultEnd['dateTime']),
            #'timeZone': end.get('timeZone', defaultEnd['timeZone'])
            }

        event = {
            'summary': summary,
            'start': {
                    'dateTime': start['dateTime'],
                    #'timeZone': start['timeZone']
                    },
            'end': {
                    'dateTime': end['dateTime'],
                    #'timeZone': end['timeZone']
                    }
            }

        if location != None:
            event['location'] = location
        if description != None:
            event['description'] = description

        # Send Google Calendar the new event and have it return the event it creates
        # Event it returns is important for Google-generated data, like event ID tag
        event = self.service.events().insert(calendarId = 'primary', body = event).execute()
        
        # Update our local copy with this event
        self.__updateLocalEvents(event)
        
        return event
