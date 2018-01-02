# TODO:
# - Create an intelligently formatted data structure to store scheduled events and important metadata about each. See the next point.
# - Create a datastructure which stores tags/traits/past data and tie these to the above data structure.

# DESIRED FUNCTIONALITY:
# - The software should be able to return the number of 'usable' or 'productive' hours left in a given timespan, based on past behaviour (and maybe some science)
# - The software should be able to add new events to an existing Google Calendar
# - The software should be able to categorize inputted tasks (based on increasingly few inputs) and schedule an appropriate time for it based on past data

# Includes
import calendar_handler as cal
import datetime

def test_event_creation(calendar):
    # scratch work

    oneHour = datetime.timedelta(hours=1)

    start = {'dateTime': (datetime.datetime.utcnow() + oneHour).isoformat() + 'Z'}
    end = {'dateTime': (datetime.datetime.utcnow() + (2 * oneHour)).isoformat() + 'Z'}


    test.createEvent('A dinner with friends', start = start, end = end, location='Bahen Center for Information Technology')

if __name__ == "__main__":
    test = cal.calendarInstance()
    #test_event_creation(test)

    test.requestEvents()
    for item in test.events:
        print(item)