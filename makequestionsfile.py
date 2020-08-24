"""
Backs up and restores a settings file to Dropbox.
This is an example app for API v2.
"""

import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

# Add OAuth2 access token here.
# You can generate one for yourself in the App Console.
# See <https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/>
TOKEN = 'eXYuevpTSE0AAAAAAAAAAV0CGrdMc7qkSgEDhaGoVCJ-e3pZ3lTaLvdQi4ejYmRM'

LOCALFILE = 'my-file.txt'
BACKUPPATH = '/my-file-backup.txt'

folder = '/api/questions'

if __name__ == '__main__':
    # Check for an access token
    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token. "
        "Open up backup-and-restore-example.py in a text editor and "
        "paste in your token in line 14.")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")

    with dropbox.Dropbox(TOKEN) as dbx:
        # Check that the access token is valid
        try:
            dbx.users_get_current_account()
        except AuthError:
            sys.exit("ERROR: Invalid access token; try re-generating an \n\
            access token from the app console on the web. \n\
            paste in your token in line 14.")


        if(dbx.files_get_metadata(folder).path_lower == folder):
            print("opened folder!")
            files = dbx.files_list_folder(folder).entries
            for file in files:
                print(file)
            print(len(files))
        else:
            print("couldn't open folder")
