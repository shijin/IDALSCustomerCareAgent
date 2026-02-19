from analytics_store import store_event


def log_event(
    question: str,
    intent: str,
    escalation: bool,
    reason: str,
    response: str,
    language: str,
    hallucination_risk: str
):
    """
    Central analytics logger.
    This function should NEVER print.
    It should only store structured analytics data.
    """

    event = {
        "question": question,
        "intent": intent,
        "escalation": escalation,
        "reason": reason,
        "response": response,
        "language": language,
        "hallucination_risk": hallucination_risk
    }

    # 🔹 Persist event (CSV / DB / memory)
    store_event(event)
