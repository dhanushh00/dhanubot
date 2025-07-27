import streamlit as st
import requests

# Set your Together AI API key here
API_KEY = "275e8d8522bff0cc6aeaf4ad3894964417242e63c20918a4e0370ec45ba0ad3c"

# Model from Together AI
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

# Basic App Config
st.set_page_config(
    page_title="DHANU Bot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"
)

# Title (clean, simple look)
st.markdown("## 🤖 DHANU Bot")
st.markdown("_Your intelligent assistant powered by Mistral_")

# Chat history storage
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Chat Input
user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Send to Together API
    payload = {
        "model": MODEL_NAME,
        "messages": st.session_state.chat_history,
        "max_tokens": 256,
        "temperature": 0.7,
        "top_p": 0.7,
        "stop": None
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.together.xyz/v1/chat/completions", json=payload, headers=headers)

    if response.status_code == 200:
        assistant_reply = response.json()["choices"][0]["message"]["content"]
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})

        with st.chat_message("assistant"):
            st.markdown(assistant_reply)
    else:
        st.error(f"⚠️ Error: {response.status_code} - {response.text}")

# Footer
st.divider()
st.markdown(
    "<p style='text-align: center; font-size: 0.9em;'>Developed by Dhanush | "
    "<a href='https://github.com/dhanushh00' target='_blank'>GitHub</a> | "
    "<a href='https://www.linkedin.com/in/dhanush-k-127099310/' target='_blank'>LinkedIn</a></p>",
    unsafe_allow_html=True
)
