import streamlit as st
import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"

FAQ_CONTEXT = """
Iron Lady offers leadership development programs for women and organizations.
Programs include:
- Individual Leadership Program
- Corporate Leadership Workshops
- Women in Leadership Transformation

Program duration: Varies by program. Typically ranges from 6 weeks to 6 months.

Program mode: Online, with some hybrid/offline options for corporate clients.

Certification: Yes, certificates are provided after successful completion.

Mentors/Coaches: Programs are led by senior industry leaders, certified leadership coaches, and experienced Iron Lady facilitators.
"""

def ask_ollama(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": f"Context: {FAQ_CONTEXT}\n\nQuestion: {prompt}\nAnswer:",
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    if response.status_code == 200:
        return response.json()["response"].strip()
    else:
        return "❌ Error: Could not get a response from Ollama."

st.title("💬 Iron Lady Leadership Chatbot")
st.write("Ask me anything about Iron Lady's leadership programs!")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    answer = ask_ollama(prompt)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
