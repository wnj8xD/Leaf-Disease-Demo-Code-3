# modules/chatbot.py

import streamlit as st
from openai import OpenAI
import os

# Load client OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Hàm gọi chatbot
def ask_bot(user_question: str, context: str = "") -> str:
    if not user_question:
        return "⚠️ Please enter a question."

    system_prompt = (
        "You are a helpful assistant that answers questions about plant diseases. "
        "Answer in simple, clear language. Keep answers concise and practical for farmers."
    )

    # Duy trì lịch sử nếu có
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Ghép nội dung trước đó
    messages = [{"role": "system", "content": system_prompt}]
    
    if context:
        messages.append({"role": "user", "content": f"Here is some context: {context}"})
    
    for msg in st.session_state["chat_history"]:
        messages.append(msg)
    
    messages.append({"role": "user", "content": user_question})

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=messages
    )

    answer = response.choices[0].message.content.strip()

    # Lưu vào session
    st.session_state["chat_history"].append({"role": "user", "content": user_question})
    st.session_state["chat_history"].append({"role": "assistant", "content": answer})

    return answer

# Hàm reset
def reset_chat():
    st.session_state["chat_history"] = []