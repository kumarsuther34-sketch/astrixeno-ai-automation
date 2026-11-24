
import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.upload"
]
print("ASTRIXENO: Starting YouTube authentication...")

flow = InstalledAppFlow.from_client_secrets_file(
    "credentials.json", SCOPES
)

credentials = flow.run_local_server(
    port=0,
    open_browser=True
)

with open("token.json", "w") as token:
    token.write(credentials.to_json())

print("SUCCESS! YouTube account connected.")
print("Token saved as token.json")
