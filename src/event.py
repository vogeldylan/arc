'''
    FILENAME:       event.py
    DEPENDENCIES:   datetime
    DESCRIPTION:    Implements the Event class
    AUTHORS:        Danial Hasan
    MODIFIED:       2018-1-2

    NOTE:           TODO: See todos in comments

 '''
 
from dateutil.parser import parse
 

class Event:
    '''Stores event information.'''
    
    def __init__(self, item):
         '''
         Args:
            item (:obj:'dict'): contains event information from Google Calendar API.
        '''
         
         
         self.name = item.get('summary', None)
         self.startTime = item.get('start', None)
         self.endTime = item.get('end', None)
         self.priority = item.get('priority', None)
         self.location = item.get('location', None)
         self.description = item.get('description', None)
         self.event_id = item.get('id', None)
    
    def printEvent(self):
        print("Name: ", self.name)
        print("Start: ", self.startTime)
        print("End: ", self.endTime)
        print("Priority: ", self.priority)
        print("ID: ", self.event_id)
    
    @property
    def name(self):
        '''str: name of event.'''
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
        
    @property
    def startTime(self):
        '''datetime: start time/date of event.'''
        return self._startTime
    
    @startTime.setter
    def startTime(self, value):
        self._startTime = parse(value.get('dateTime', None))
        
    @property
    def endTime(self):
        '''datetime: end time/date of event.'''
        return self._endTime
    
    @endTime.setter
    def endTime(self, value):
        self._endTime = parse(value.get('dateTime', None))
        
    @property 
    def priority(self):
        '''int: denotes priority of event.'''
        return self._priority
        
    @priority.setter
    def priority(self, value):
        self._priority = value
        
    @property
    def location(self):
        '''str, optional: location of event.'''
        return self._location
    
    @location.setter
    def location (self, value = None):
        self._location = value
        
    @property
    def description(self):
        '''str, optional: description of event.'''
        return self._description
    
    @description.setter
    def description(self, value = None):
        self._description = value
        
    @property
    def event_id(self):
        '''str: Google Calendar id of event'''
        return self._event_id
        
    @event_id.setter
    def event_id(self, value):
        self._event_id = value