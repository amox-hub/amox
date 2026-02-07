import streamlit as st
import google.generativeai as genai
import os

# إعداد واجهة Amox
st.set_page_config(page_title="Amox AI", page_icon="⚡")
st.title("⚡ Amox AI Chatbot")

# جلب المفتاح من الـ Secrets
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # إجبار المكتبة على استخدام الإصدار المستقر v1 بدلاً من v1beta
    os.environ["GOOGLE_API_VERSION"] = "v1" 
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("تأكد من وضع GOOGLE_API_KEY في الـ Secrets")

# استخدام الموديل بدون أي بادئات
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
        try:
            # طلب الرد
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # إذا استمر الخطأ، سنعرض رسالة واضحة
            st.error(f"خطأ في الاتصال: {e}")
