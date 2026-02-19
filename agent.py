from langchain_aws import ChatBedrock
from tools import search_faq
from router import classify_intent
from escalation_detector import wants_human_help
from sensitive_detector import is_sensitive_query
from escalation import (
    HUMAN_REQUEST_ESCALATION,
    OUT_OF_SCOPE_ESCALATION,
    SENSITIVE_QUERY_ESCALATION
)
from analytics import log_event

_agent = None


def detect_language(text: str) -> str:
    """
    Lightweight language detection for analytics only.
    """
    return "hinglish" if not text.isascii() else "english"


def get_agent():
    global _agent
    if _agent:
        return _agent

    llm = ChatBedrock(
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        region_name="ap-south-1",
        temperature=0
    )

    def routed_agent(user_query: str) -> str:
        """
        Production-grade agent:
        - FAQ is used only as grounding
        - LLM produces final clean answer
        """

        language = detect_language(user_query)

        # 1️⃣ Human escalation
        if wants_human_help(user_query):
            response = HUMAN_REQUEST_ESCALATION

            log_event(
                question=user_query,
                intent="HUMAN_REQUEST",
                escalation=True,
                reason="explicit_user_request",
                response=response,
                language=language,
                hallucination_risk="none"
            )

            return response

        # 2️⃣ Sensitive queries
        if is_sensitive_query(user_query):
            response = SENSITIVE_QUERY_ESCALATION

            log_event(
                question=user_query,
                intent="SENSITIVE_QUERY",
                escalation=True,
                reason="policy_or_promise_related",
                response=response,
                language=language,
                hallucination_risk="none"
            )

            return response

        # 3️⃣ Intent classification
        intent = classify_intent(llm, user_query)

        if intent in ["PROGRAM_INFO", "FEES_ENROLLMENT", "LEARNING_EXPERIENCE"]:
            # 🔹 Retrieve grounding facts (NOT final answer)
            faq_context = search_faq.invoke(user_query)

            if not faq_context or faq_context.strip() == "":
                response = "This information is not specified in the IDALS program details."

                log_event(
                    question=user_query,
                    intent=intent,
                    escalation=False,
                    reason="no_faq_match",
                    response=response,
                    language=language,
                    hallucination_risk="low"
                )

                return response

            # 🔹 Final synthesis prompt (UNCHANGED)
            synthesis_prompt = f"""
You are an IDALS customer support agent for an Indian based dance education platform.

Important Context:
- All fees mentioned are in Indian Rupees (INR / ₹)
- Do NOT convert fees to dollars
- Always mention ₹ when talking about price or fees

CRITICAL RULES (NON-NEGOTIABLE):
- Answer ONLY using the provided IDALS information
- Do NOT invent offers, discounts, promotions, or guarantees
- If discounts are not explicitly mentioned, clearly say:
  "IDALS does not offer any discounts on the current fee structure."
- NEVER speculate or suggest future offers
- NEVER add examples that are not in the source
- There are no installment options for fees payment
- For any new batch related questions, the user should be directed to our calling number or email
- All course details needs to be shared when asked on course or program details
- While responding about certification, please mention about registered company and ISO certified company as well

Answer the user's question clearly and conversationally,
using ONLY the information provided below.

Rules:
- Do NOT mention FAQ, sources, or internal notes
- Do NOT repeat the question
- Do NOT include Q/A formatting
- Give a direct, friendly answer
- Use simple bullet points if helpful (max 4)

User question:
{user_query}

IDALS program information:
{faq_context}
"""

            response = llm.invoke(synthesis_prompt).content.strip()

            log_event(
                question=user_query,
                intent=intent,
                escalation=False,
                reason=None,
                response=response,
                language=language,
                hallucination_risk="low"
            )

            return response

        # 4️⃣ Out of scope
        response = OUT_OF_SCOPE_ESCALATION

        log_event(
            question=user_query,
            intent="OUT_OF_SCOPE",
            escalation=True,
            reason="not_in_faq",
            response=response,
            language=language,
            hallucination_risk="low"
        )

        return response

    _agent = routed_agent
    return _agent
