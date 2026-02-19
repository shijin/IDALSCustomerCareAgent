import streamlit as st
from agent import get_agent


st.set_page_config(
    page_title="IDALS Customer Care Agent",
    page_icon="💃",
    layout="centered"
)

st.title("💬 IDALS Customer Care Agent")
st.caption("Ask anything about IDALS programs, certification, and learning experience.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("assistant"):
        st.spinner("⏳ Thinking...")

        # Placeholder response for now
        agent = get_agent()
        assistant_reply = agent(user_input)
        st.markdown(assistant_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

    st.rerun()
