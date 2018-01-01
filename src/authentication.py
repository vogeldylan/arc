'''
    FILENAME:       authentication.py
    DEPENDENCIES:
    DESCRIPTION:    Handles aquiring credentials for user authentication
    AUTHORS:        Basically copied from: https://developers.google.com/google-apps/calendar/quickstart/python
    MODIFIED:       2017-12-30

    NOTE:           TODO:
                    * Implement more credential handling functions, like refresh
                    tokens and revoking permissions, as outlined here:
                    https://developers.google.com/identity/protocols/OAuth2




 '''

from oauth2client import client    # For creating flows, which get user credentials
from oauth2client import tools
from oauth2client.file import Storage
import os          # for creating system directories


SCOPE = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def get_credentials():
    home_dir = os.path.expanduser('~')     # Expands '~' for the particular OS system
    credential_dir = os.path.join(home_dir, '.arc/credentials')    # Appends our application path
    
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)          # Recursively creates required directories
    credential_path = os.path.join(credential_dir, 'arc-credentials.dat')
    
    store = Storage(credential_path)        # Load whatever is stored at the path
    credentials = Storage.get(store)
    
    if not credentials or credentials.invalid:  # If there are no credentials, create them using the client secret file
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPE)
    
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
    
    return credentials
