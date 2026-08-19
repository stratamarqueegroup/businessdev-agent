import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def create_task(title, due_date=None):
    tasks = load_tasks()

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "due_date": due_date,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }

    tasks.append(task)
    save_tasks(tasks)

    return task


def get_tasks():
    return load_tasks()


def complete_task(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            return task

    return None
