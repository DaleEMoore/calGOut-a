# TODO; try the new Google calendar API v3 here.
# https://developers.google.com/google-apps/calendar/
# https://developers.google.com/google-apps/calendar/migration
# https://developers.google.com/google-apps/calendar/firstapp

__author__ = 'dalem'
"""
This might need to be used to access the new Google Calendar security.
https://console.developers.google.com/project/daleemoore/apiui/credential?clientType
Client ID for native application
"""
print("Hi world.")

import gflags
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

FLAGS = gflags.FLAGS

# Set up a Flow object to be used if we need to authenticate. This
# sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# the information it needs to authenticate. Note that it is called
# the Web Server Flow, but it can also handle the flow for native
# applications
# The client_id and client_secret can be found in Google Developers Console
# YOUR_ fields can be found at https://console.developers.google.com/project/daleemoore/apiui/credential
FLOW = OAuth2WebServerFlow(
    client_id='763456021694-pf3ue9dqld8fl1n17mevv9iofej8v2kk.apps.googleusercontent.com', #YOUR_CLIENT_ID
    client_secret='IXFBGy1dLYqWtpcSY1v0koYq', #YOUR_CLIENT_SECRET
    scope='https://www.googleapis.com/auth/calendar',
    user_agent='calGOut/0.0.1' #YOUR_APPLICATION_NAME/YOUR_APPLICATION_VERSION'
    )

# To disable the local server feature, uncomment the following line:
# FLAGS.auth_local_webserver = False

# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
storage = Storage('calendar.dat')
credentials = storage.get()
if credentials is None or credentials.invalid == True:
  credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
http = httplib2.Http()
http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google Developers Console
# to get a developerKey for your own application.
# YOUR_DEVELOPER_KEY from API keys section of https://developers.google.com/console/help/
# https://code.google.com/apis/console/?noredirect&pli=1#project:763456021694:access
# https://code.google.com/apis/console/?noredirect#project:763456021694:overview
# https://code.google.com/apis/console/?noredirect#project:763456021694:access
service = build(serviceName='calendar', version='v3', http=http,
       developerKey='YOUR_DEVELOPER_KEY') # TODO; I have no idea what my developer key is.
       #  or where to find it.

# From https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list
page_token = None
while True:
  calendar_list = service.calendarList().list(pageToken=page_token).execute()
  for calendar_list_entry in calendar_list['items']:
    print "Calendar: " + calendar_list_entry['summary']
    # TODO; get all calendars all events.
    # https://raw.githubusercontent.com/insanum/gcalcli/master/gcalcli
    """
    from gcalcli.py
    BowChickaWowWow
    AgendaQuery
    eventList = self._SearchForCalEvents(start, None, searchText)
    _IterateEvents
    _PrintEvent
    """


  page_token = calendar_list.get('nextPageToken')
  if not page_token:
    print("not page_token")
    break
  else:
    print("page_token")



print("Bye world.")
