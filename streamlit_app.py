import streamlit as st
from openai import OpenAI
import markdown2

# -----------------------------
# Initialize OpenAI client
# -----------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# Page settings
# -----------------------------
st.set_page_config(page_title="Coding Help Chatbot", page_icon="💻")
st.title("💬 Coding Help Chatbot")
st.write("Ask me any programming question! I can explain concepts, debug code, or provide examples.")

# -----------------------------
# Sidebar settings
# -----------------------------
st.sidebar.header("Settings")
language = st.sidebar.selectbox(
    "Programming Language (optional)",
    ["Python", "JavaScript", "C++", "Java", "HTML/CSS", "Other"]
)

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# -----------------------------
# Initialize chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# User input
# -----------------------------
user_input = st.text_input("Type your question here:")

if st.button("Send") or user_input:
    if user_input:
        # Include language info in user message
        prompt = f"[Language: {language}]\n{user_input}"
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Call OpenAI API
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                temperature=0.7
            )

        bot_message = response.choices[0].message["content"]
        st.session_state.messages.append({"role": "assistant", "content": bot_message})

# -----------------------------
# Display chat history
# -----------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        md_content = markdown2.markdown(msg["content"], extras=["fenced-code-blocks"])
        st.markdown(f"**Bot:** {md_content}", unsafe_allow_html=True)
