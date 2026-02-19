def wants_human_help(user_query: str) -> bool:
    keywords = [
        "human",
        "talk to someone",
        "customer care",
        "support",
        "whatsapp",
        "phone",
        "call",
        "email",
        "contact"
    ]

    query_lower = user_query.lower()
    return any(keyword in query_lower for keyword in keywords)
