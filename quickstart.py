from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
import datetime
import os.path

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        # if creds and creds.expired and creds.refresh_token:
        #     creds.refresh(Request())
        # else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Get the most recent 10 emails with the SENT Label
    results = service.users().threads() \
                     .list(userId='me', labelIds=['INBOX']) \
                     .execute()
    thread_ids = set([
        thread.get('id', '') for thread in results.get('threads', [])
    ])
    # Check those emails against the cached list of email IDs
    if os.path.exists('sent_thread_ids.txt'):
        with open('sent_thread_ids.txt', 'r') as f:
            old_thread_ids = set([line.strip() for line in f.readlines()])
    else:
        old_thread_ids = set()

    diff = thread_ids.difference(old_thread_ids)
    print(f"Found {len(diff)} newly sent emails")
    print(''.join(["\n" + i for i in list(diff)]))
    with open('sent_thread_ids.txt', 'w') as f:
        f.writelines("\n".join(thread_ids))
    

    # If we've sent an email that's not in the cached list, dispense an m&m



    # Get all threads in the inbox
    # results = service.users().threads().list(userId='me', labelIds=['SENT']).execute()
    # threads = results.get('threads', [])
    # for i, thread in enumerate(threads):
    #     print(f"({i}) {thread.get('id')} {thread.get('snippet', '')[:40]}")
    #     msgs = service.users().threads().get(userId='me', id=thread.get('id')).execute()
    #     for msg in msgs.get('messages', []):
    #         dt = datetime.datetime.fromtimestamp(int(msg.get('internalDate'))/1000)
    #         headers = msg.get('payload', {}).get('headers', {})
    #         frm = [e for e in headers if e.get('name','') == "From"]
    #         if frm:
    #             print(f"\t{dt}, {frm[0]}")


if __name__ == '__main__':
    main()
