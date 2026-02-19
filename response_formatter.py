def format_idals_response(raw_answer: str, user_query: str, intent: str) -> str:
    """
    Converts raw FAQ content into a clean, conversational answer.
    """

    if not raw_answer or raw_answer.strip() == "":
        return "This information is not specified in the IDALS program details."

    # Split into bullet-style facts
    lines = [
        line.strip("• ").strip()
        for line in raw_answer.split("\n")
        if line.strip()
    ]

    # Keep only the most relevant points (max 3)
    relevant_points = []
    for line in lines:
        if "Q:" in line or "A:" in line:
            continue
        relevant_points.append(line)
        if len(relevant_points) == 3:
            break

    if not relevant_points:
        return "This information is not specified in the IDALS program details."

    # Conversational framing based on intent
    if intent == "LEARNING_EXPERIENCE":
        intro = "Here’s what you’ll learn in the IDALS program:"
    elif intent == "PROGRAM_INFO":
        intro = "Here’s how the IDALS program works:"
    elif intent == "FEES_ENROLLMENT":
        intro = "Here are the enrollment and fee details:"
    else:
        intro = "Here’s what we found in the IDALS program details:"

    bullets = "\n".join([f"• {point}" for point in relevant_points])

    return f"{intro}\n\n{bullets}"
