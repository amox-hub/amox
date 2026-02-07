import streamlit as st
import google.generativeai as genai

# إعداد واجهة Amox
st.set_page_config(page_title="Amox AI", page_icon="⚡")
st.title("⚡ Amox AI Chatbot")

# مفتاح الـ API الخاص بك (موجود في صورتك)
API_KEY = "AIzaSyAPQxFd26DrXkCbrNLxlUFwveJLr0tKhpQ" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("كيف يمكن لـ Amox مساعدتك؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
