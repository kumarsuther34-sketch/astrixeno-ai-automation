import os
import json
import urllib.request
from pathlib import Path

for line in Path(".env").read_text(encoding="utf-8").splitlines():
    if line.startswith("GEMINI_API_KEY="):
        os.environ["GEMINI_API_KEY"] = line.split("=", 1)[1].strip()

key = os.getenv("GEMINI_API_KEY")

url = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.1-flash-lite:generateContent"
    f"?key={key}"
)

payload = {
    "contents": [{
        "parts": [{
            "text": (
                "You are the ASTRIXENO technology documentary writer. "
                "Write an original, engaging 45-second YouTube Shorts "
                "script about 5 AI tools changing the world. "
                "Include a powerful hook, five concise points and a "
                "strong ending. Use natural professional English."
            )
        }]
    }]
}

request = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(request, timeout=60) as response:
        result = json.loads(response.read().decode("utf-8"))

    script = result["candidates"][0]["content"]["parts"][0]["text"]

    Path("scripts").mkdir(exist_ok=True)
    Path("scripts/gemini_test_script.txt").write_text(
        script, encoding="utf-8"
    )

    print("ASTRIXENO AI SCRIPT GENERATED SUCCESSFULLY")
    print("Saved: scripts/gemini_test_script.txt")
    print("\n", script)

except urllib.error.HTTPError as error:
    print("HTTP ERROR:", error.code)
    print(error.read().decode("utf-8"))

except Exception as error:
    print("Generation failed:", str(error))