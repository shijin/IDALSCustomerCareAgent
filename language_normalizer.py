def normalize_query(query: str) -> str:
    """
    Normalize Hindi / Hinglish queries into semantic English intent queries
    """
    q = query.lower()

    if any(phrase in q for phrase in [
        "kya sikh", "kya seekh", "kya milega", "kuch milega", "course mein kya"
    ]):
        return "What will I learn in this course?"

    return query
