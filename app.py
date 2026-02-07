
import streamlit as st
import google.generativeai as genai
import os

# --- 1. إعدادات الهوية والواجهة ---
st.set_page_config(
    page_title="Amox AI Chatbot",
    page_icon="⚡",
    layout="centered"
)

# تحسين مظهر النصوص والرسائل
st.markdown("""
    <style>
    .stChatMessage { border-radius: 10px; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. إعداد الاتصال (توافقية النسخة 0.7.0) ---
# إجبار النظام على استخدام v1 لتجنب خطأ 404 الشهير في v1beta
os.environ["GOOGLE_API_VERSION"] = "v1"

def setup_model():
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("🔑 خطأ: لم يتم العثور على المفتاح في إعدادات Secrets.")
        st.stop()
    
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # في النسخة 0.7.0، هذا هو الموديل الأكثر استقراراً
    return genai.GenerativeModel('gemini-1.5-flash')

model = setup_model()

# --- 3. إدارة الذاكرة (Chat History) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. معالجة الإدخال والرد الذكي ---
st.title("⚡ Amox AI")
st.caption("النسخة الاحترافية المستقرة")

if prompt := st.chat_input("كيف يمكن لـ Amox مساعدتك؟"):
    # إضافة رسالة المستخدم للذاكرة والعرض
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الرد من الذكاء الاصطناعي
    with st.chat_message("assistant"):
        try:
            with st.spinner("جاري التفكير..."):
                # في نسخة 0.7.0 نستخدم generate_content مباشرة
                response = model.generate_content(prompt)
                full_response = response.text
                st.markdown(full_response)
                
                # إضافة رد الموديل للذاكرة
                st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"⚠️ عذراً، حدث خطأ تقني: {str(e)}")
