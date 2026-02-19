from langchain_core.messages import SystemMessage, HumanMessage
from system_instructions import IDALS_SYSTEM_INSTRUCTIONS

INTENT_SYSTEM_PROMPT = """
You are an intent classifier for the IDALS Customer Care Agent.

Classify the user's question into ONE of the following intents:

1. PROGRAM_INFO
   - course structure
   - duration
   - certification
   - instructors
   - schedule

2. FEES_ENROLLMENT
   - fees
   - payment
   - enrollment
   - registration

3. LEARNING_EXPERIENCE
   - recorded or live classes
   - doubt clearing
   - feedback
   - practice
   - YouTube content

4. OUT_OF_SCOPE
   - refunds (if not mentioned)
   - guarantees
   - legal / policy questions
   - anything not clearly in FAQ

Respond with ONLY the intent name.
"""

def classify_intent(llm, user_query: str) -> str:
    response = llm.invoke([
        SystemMessage(
            content=f"{IDALS_SYSTEM_INSTRUCTIONS}\n\n{INTENT_SYSTEM_PROMPT}"
        ),
        HumanMessage(content=user_query)
    ])
    return response.content.strip()

