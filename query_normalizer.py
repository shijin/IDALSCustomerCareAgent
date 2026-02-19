from langchain_aws import ChatBedrock

_llm = ChatBedrock(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="ap-south-1",
    temperature=0
)

def normalize_to_english(user_query: str) -> str:
    """
    Converts Hinglish / Hindi query into clean English
    for internal FAQ search only.
    """
    prompt = f"""
Convert the following question into clear English.
Do NOT add new meaning. Keep it factual.

Question:
{user_query}
"""
    return _llm.invoke(prompt).content.strip()
