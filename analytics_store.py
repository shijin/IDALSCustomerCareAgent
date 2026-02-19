import csv
import os
from datetime import datetime

FILE_PATH = "agent_analytics.csv"

HEADERS = [
    "timestamp",
    "question",
    "intent",
    "escalation",
    "reason",
    "language",
    "hallucination_risk",
    "response_length"
]


def store_event(event: dict):
    """
    Persist a single analytics event.
    Only writes fields defined in HEADERS.
    """

    file_exists = os.path.exists(FILE_PATH)

    cleaned_event = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": event.get("question"),
        "intent": event.get("intent"),
        "escalation": event.get("escalation"),
        "reason": event.get("reason"),
        "language": event.get("language"),
        "hallucination_risk": event.get("hallucination_risk"),
        "response_length": len(event.get("response", ""))
    }

    with open(FILE_PATH, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)

        if not file_exists:
            writer.writeheader()

        writer.writerow(cleaned_event)
