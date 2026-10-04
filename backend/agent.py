import json
import re
from datetime import datetime

import ollama


SYSTEM_PROMPT = """
You are Unmess, a life-admin task extraction assistant.

The user's current date is 2026-10-05.

Read the user's brain dump and extract every actionable task.

Return ONLY valid JSON.

Exact format:

{
  "tasks": [
    {
      "title": "short actionable task",
      "deadline": "YYYY-MM-DD or null",
      "priority": "critical",
      "blocker": null,
      "description": "short description"
    }
  ]
}

Allowed priority values:
critical
high
normal
low

Rules:

1. Extract EVERY distinct actionable task.
2. Do not combine unrelated tasks.
3. Never invent a task.
4. Never invent a deadline.
5. If the user says "tomorrow", calculate it relative to 2026-10-05.
6. If the user says "6th October", use 2026-10-06.
7. If there is no clear deadline, use null.
8. Do not convert dates into random historical dates.
9. If one task depends on another, put the dependency in blocker.
10. Return JSON only.
11. No markdown.
12. No explanation before or after the JSON.
"""


def extract_json(text: str):
    text = text.strip()

    # Remove markdown code fences if the model added them
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            f"Gemma did not return JSON:\n{text}"
        )

    json_text = text[start:end + 1]

    return json.loads(json_text)


def normalize_task(task):
    return {
        "title": str(
            task.get("title")
            or task.get("task")
            or task.get("name")
            or "Untitled task"
        ),
        "deadline": (
            task.get("deadline")
            if task.get("deadline") not in ("", "null", None)
            else None
        ),
        "priority": str(
            task.get("priority")
            or task.get("importance")
            or "normal"
        ).lower(),
        "blocker": task.get("blocker"),
        "description": task.get("description") or "",
    }


def analyze_brain_dump(text: str):

    response = ollama.chat(
        model="gemma3:1b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": text,
            },
        ],
    )

    content = response["message"]["content"]

    print("\n===== GEMMA RAW RESPONSE =====")
    print(content)
    print("==============================\n")

    data = extract_json(content)

    raw_tasks = data.get("tasks", [])

    if not isinstance(raw_tasks, list):
        raise ValueError("Gemma returned an invalid tasks list.")

    tasks = [
        normalize_task(task)
        for task in raw_tasks
        if isinstance(task, dict)
    ]

    return {
        "tasks": tasks
    }