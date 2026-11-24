
import os
import json
import urllib.request
import urllib.error

from pathlib import Path

env_file = Path(".env")

for line in env_file.read_text(encoding="utf-8").splitlines():
    if line.startswith("GEMINI_API_KEY="):
        os.environ["GEMINI_API_KEY"] = line.split("=", 1)[1].strip()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: Gemini API key missing")
    raise SystemExit

url = (
    "https://generativelanguage.googleapis.com/v1beta/models"
    f"?key={api_key}"
)

try:
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    models = [
        model["name"]
        for model in data.get("models", [])
        if "generateContent" in model.get("supportedGenerationMethods", [])
    ]

    print("GEMINI API CONNECTION SUCCESSFUL")
    print("Available text-generation models:", len(models))

    for model in models:
        print("-", model)

except urllib.error.HTTPError as error:
    print("API ERROR. HTTP status:", error.code)
except Exception:
    print("CONNECTION FAILED. Check internet or API configuration.")
