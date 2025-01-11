import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_CLOUD_API_KEY"] = os.getenv("GOOGLE_API_KEY")  # Compatibility

genai.configure()

system_prompt = """You are a helpful AI assistant. Respond to user requests in a clear, concise, and informative manner. Provide the user with the information they need to make an informed decision."""
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_prompt)

def message_from_gemini(chat, prompt):
    try:
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error Interacting with Gemini: {e}")
        return "An error occurred while interacting with Gemini."

st.title("🤖 Gemini AI Chatbot 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "model", "parts": "Hello! How can I help you today?"}
    ]

chat = model.start_chat(
    history=st.session_state["messages"]
)

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["parts"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "parts": prompt})
    st.chat_message("user").write(prompt)
    msg = message_from_gemini(chat, prompt)
    st.session_state.messages.append({"role": "model", "parts": msg})
    st.chat_message("model").write(msg)