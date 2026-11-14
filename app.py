from dotenv import load_dotenv
import os
import streamlit as st
from langchain_openai import ChatOpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        st.error("OpenRouter API Key not found!")
        st.stop()

llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)

st.title("🤖 AskBuddy - AI QnA Bot")
st.markdown("My QnA Bot with LangChain and OpenRouter!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

query = st.chat_input("Ask anything...")

if query:
    st.session_state.messages.append(
        {"role": "user", "content": query}
    )

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = llm.invoke(query)
                answer = res.content
                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as e:
                st.error(f"Error: {e}")
