import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from config import YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_TOKEN_FILE, YOUTUBE_SCOPES


def get_credentials() -> Credentials:
    """Load saved YouTube credentials or run OAuth flow to create them."""
    creds = None

    if os.path.exists(YOUTUBE_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(YOUTUBE_TOKEN_FILE, YOUTUBE_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(YOUTUBE_CLIENT_SECRETS_FILE):
                raise FileNotFoundError(
                    f"YouTube client secrets file not found: {YOUTUBE_CLIENT_SECRETS_FILE}. "
                    "Download it from Google Cloud and save it to this path."
                )
            flow = InstalledAppFlow.from_client_secrets_file(YOUTUBE_CLIENT_SECRETS_FILE, YOUTUBE_SCOPES)
            creds = flow.run_local_server(port=0)

        with open(YOUTUBE_TOKEN_FILE, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())
            print(f"[YouTube] Saved token to {YOUTUBE_TOKEN_FILE}")

    return creds
