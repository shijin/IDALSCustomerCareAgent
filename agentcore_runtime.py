from dotenv import load_dotenv
load_dotenv()

from bedrock_agentcore.runtime import BedrockAgentCoreApp
from agent import get_agent

app = BedrockAgentCoreApp()

@app.entrypoint
def handler(payload, context):
    """
    AgentCore runtime entrypoint.
    """

    agent = get_agent()

    # 1️⃣ Extract user message
    user_query = payload.get("prompt", "").strip()

    # 2️⃣ Extract session/user ID (used for WhatsApp)
    # AgentCore guarantees a sessionId
    user_id = context.session_id

    if not user_query:
        return {"result": "Empty input received"}

    # 3️⃣ Invoke routed agent with user_id
    result = agent(
        user_query=user_query,
        user_id=user_id
    )

    return {"result": result}

if __name__ == "__main__":
    app.run()
