import sys
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
import pickle

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRETS_FILE = 'client_secret_660164281783-lhojqeemqib5e756dl5rejcd8nqfh8kg.apps.googleusercontent.com.json'
TOKEN_FILE = 'token.pickle'
PARENT_FOLDER_ID = "1bQN4CrM-6wEo9l4g5GWc6PMC11MBdvu9"

def authenticate():
    """Authenticate using OAuth 2.0."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def upload_file(file_path):
    """Uploads the given file to Google Drive."""
    if not os.path.exists(file_path):
        print(f" Error: File '{file_path}' not found.")
        sys.exit(1)

    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_name = os.path.basename(file_path)  # Get only file name
    file_metadata = {
        'name': file_name,
        'parents': [PARENT_FOLDER_ID]
    }

    media = MediaFileUpload(file_path, mimetype='application/octet-stream')  # Upload encrypted file as binary

    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()

        print(f" File uploaded successfully! File ID: {file.get('id')}")
    except Exception as e:
        print(f" Upload Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(" Error: No file path provided.")
        sys.exit(1)
    else:
        upload_file(sys.argv[1])
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Server is running!"

@app.route('/upload', methods=['POST'])
def upload():
    # your existing Google Drive upload logic here
    return "File uploaded successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
