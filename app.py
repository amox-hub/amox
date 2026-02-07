import streamlit as st
import google.generativeai as genai

# إعداد واجهة Amox
st.set_page_config(page_title="Amox AI", page_icon="⚡")
st.title("⚡ Amox AI Chatbot")

# تأكد من أن مفتاحك صحيح هنا
API_KEY = "AIzaSyAPQxFd26DrXkCbrNLxlUFwveJLr0tKhpQ" 
genai.configure(api_key=API_KEY)

# التعديل الذهبي: استخدام اسم الموديل الكامل والأحدث
model = genai.GenerativeModel('models/gemini-1.5-flash')

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
        try:
            # إضافة معالجة للأخطاء للتأكد من الرد
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ في الاتصال: {e}")
