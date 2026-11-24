
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

print("ASTRIXENO: Checking YouTube channel...")

credentials = Credentials.from_authorized_user_file(
    "token.json",
    ["https://www.googleapis.com/auth/youtube.readonly"]
)

youtube = build("youtube", "v3", credentials=credentials)

response = youtube.channels().list(
    part="snippet,statistics",
    mine=True
).execute()

if response.get("items"):
    channel = response["items"][0]
    print("\nSUCCESS! CHANNEL CONNECTED")
    print("Channel Name:", channel["snippet"]["title"])
    print("Channel ID:", channel["id"])
    print("Subscribers:", channel["statistics"].get("subscriberCount", "Hidden"))
else:
    print("No YouTube channel found.")

input("\nPress Enter to close...")
