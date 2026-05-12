import streamlit as st
import pandas as pd
import google.generativeai as genai

# إعدادات الواجهة (هوية HKA)
st.set_page_config(page_title="HKA Smart Analytics", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #D4AF37; }
    h1, h3 { color: #D4AF37; text-align: center; }
    .stButton>button { background-color: #D4AF37; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ HKA Smart Analytics ✨")

# محاولة الاتصال بالموديل بطريقة مرنة
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # تجربة الموديل الأكثر استقراراً لهذه النسخة
    model = genai.GenerativeModel('gemini-1.0-pro') 
except Exception as e:
    st.error(f"مشكلة في التهيئة: {e}")

uploaded_file = st.file_uploader("ارفعي ملف البيانات", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl') if uploaded_file.name.endswith('xlsx') else pd.read_csv(uploaded_file)
        st.success("تم رفع البيانات!")
        st.dataframe(df.head(5))

        user_question = st.text_input("💬 اسألي الذكاء الاصطناعي عن بياناتك:")
        
        if st.button("بدء التحليل الذكي"):
            with st.spinner("جاري التحليل..."):
                # الكود هنا يرسل عينة نصية بسيطة جداً لضمان عدم حدوث خطأ 404
                prompt = f"حلل هذه البيانات باختصار: {df.columns.tolist()}. السؤال: {user_question}"
                response = model.generate_content(prompt)
                st.info(response.text)
    except Exception as e:
        st.error(f"حدث خطأ: {e}")
