
import os
import json
import logging
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
QUEUE_FILE = os.path.join(BASE, "queue", "daily_queue.json")
LOG_FILE = os.path.join(BASE, "logs", "daily_manager.log")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def load_config():
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    temp = QUEUE_FILE + ".tmp"
    with open(temp, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
    os.replace(temp, QUEUE_FILE)

def create_daily_task():
    config = load_config()
    today = date.today().isoformat()

    for task in config["queue"]:
        if task["date"] == today:
            print("Today's task already exists.")
            return

    task = {
        "date": today,
        "topic": "5 AI Tools Changing the World in 2026",
        "status": "pending",
        "attempts": 0,
        "approval": "required",
        "video_file": None
    }

    config["queue"].append(task)
    save_config(config)

    logging.info("Daily task created: %s", today)
    print("ASTRIXENO DAILY TASK CREATED")
    print("Topic:", task["topic"])
    print("Status:", task["status"])

def show_tasks():
    config = load_config()

    print("\nASTRIXENO PRODUCTION QUEUE\n")

    if not config["queue"]:
        print("No tasks available.")
        return

    for task in config["queue"]:
        print(
            task["date"],
            "|",
            task["topic"],
            "|",
            task["status"],
            "| Attempts:",
            task["attempts"]
        )

if __name__ == "__main__":
    print("ASTRIXENO DAILY MANAGER")
    print("1. Create today's task")
    print("2. Show production queue")

    choice = input("Select 1 or 2: ").strip()

    if choice == "1":
        create_daily_task()
    elif choice == "2":
        show_tasks()
    else:
        print("Invalid selection.")
