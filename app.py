import streamlit as st
import google.generativeai as genai

# جلب المفتاح من الـ Secrets بدلاً من كتابته يدوياً
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("يرجى إعداد المفتاح في Settings > Secrets")

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
            # إضافة معالجة للأخطاء للتأكد من الرد
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"حدث خطأ في الاتصال: {e}")
