
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

credentials = Credentials.from_authorized_user_file(
    "token.json", SCOPES
)

youtube = build("youtube", "v3", credentials=credentials)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "ASTRIXENO - Private Upload Test",
            "description": "Testing ASTRIXENO video automation.",
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "private"
        }
    },
    media_body=MediaFileUpload(
        "videos/astrixeno_visible_test.mp4",
        mimetype="video/mp4",
        resumable=True
    )
)

response = request.execute()

print("UPLOAD SUCCESSFUL!")
print("Video ID:", response["id"])
print("Privacy: PRIVATE")
input("Press Enter to close...")
