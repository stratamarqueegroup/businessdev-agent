import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
from tasks import create_task, get_tasks, complete_task

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI(title="STRATA AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "status": "online",
        "system": "STRATA AI API",
        "ai": "Gemini"
    }


@app.post("/chat")
@app.post("/api/chat")
def chat(request: ChatRequest):
    message = request.message.strip()
    lower_message = message.lower()

    # --------------------------------
    # REMINDER COMMAND
    # --------------------------------

    if lower_message.startswith("remind me to "):
        reminder_text = message[len("remind me to "):].strip()

        due_date = None
        title = reminder_text

        if " tomorrow at " in lower_message:
            marker = " tomorrow at "
            split_at = lower_message.index(marker)

            title = message[len("remind me to "):split_at].strip()
            time_part = message[split_at + len(marker):].strip()

            from datetime import datetime, timedelta

            tomorrow = datetime.now() + timedelta(days=1)
            due_date = f"{tomorrow.strftime('%Y-%m-%d')} {time_part}"

        elif " today at " in lower_message:
            marker = " today at "
            split_at = lower_message.index(marker)

            title = message[len("remind me to "):split_at].strip()
            time_part = message[split_at + len(marker):].strip()

            from datetime import datetime

            today = datetime.now()
            due_date = f"{today.strftime('%Y-%m-%d')} {time_part}"

        task = create_task(title, due_date)

        return {
            "response": f"Reminder created: {task['title']}"
            + (f" — {task['due_date']}" if task["due_date"] else "")
        }

    # --------------------------------
    # SHOW REMINDERS COMMAND
    # --------------------------------

    if lower_message in [
        "show my reminders",
        "show reminders",
        "list my reminders",
        "list reminders",
        "what are my reminders",
    ]:
        tasks = get_tasks()

        if not tasks:
            return {
                "response": "You have no reminders."
            }

        lines = ["Your reminders:"]

        for task in tasks:
            status = "completed" if task["completed"] else "pending"
            due = f" — {task['due_date']}" if task["due_date"] else ""

            lines.append(
                f"{task['id']}. {task['title']}{due} [{status}]"
            )

        return {
            "response": "\n".join(lines)
        }

    # --------------------------------
    # COMPLETE REMINDER COMMAND
    # --------------------------------

    if lower_message.startswith("complete reminder "):
        try:
            task_id = int(lower_message.replace("complete reminder ", "").strip())
        except ValueError:
            return {
                "response": "Please provide the reminder number. Example: Complete reminder 1."
            }

        task = complete_task(task_id)

        if not task:
            return {
                "response": f"Reminder {task_id} was not found."
            }

        return {
            "response": f"Reminder completed: {task['title']}"
        }

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=request.message,
            config=types.GenerateContentConfig(
                system_instruction="""
You are STRATA, the AI operating assistant for Strata Marquee Group.

Your name is STRATA. Never call yourself Sheridan or another name.

You are a professional, concise, intelligent business operations assistant.

Your job is to help operate Strata Marquee Group, including lead generation, CRM management, sales, appointment setting, follow-ups, business development, analytics, websites, marketing, and task organization.

When the user asks about the STRATA system, answer as STRATA.

When the user gives commands such as "open leads", "open crm", "open analytics", "open websites", or "open browser", understand that they are interacting with the STRATA OS interface.

Do not invent information about leads, clients, revenue, CRM records, or business activity.

If information is unavailable, say so clearly.

Be helpful, professional, and action-oriented.

Do not invent a different name for the user.
"""
            )
        )

        return {
            "response": response.text
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/tasks")
def list_tasks():
    return {"tasks": get_tasks()}


class TaskRequest(BaseModel):
    title: str
    due_date: str | None = None


@app.post("/tasks")
def add_task(request: TaskRequest):
    return create_task(request.title, request.due_date)


@app.post("/tasks/{task_id}/complete")
def finish_task(task_id: int):
    task = complete_task(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
