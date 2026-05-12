import streamlit as st
import pandas as pd
import google.generativeai as genai

# إعداد واجهة الصفحة
st.set_page_config(page_title="HKA Smart Analytics", page_icon="📊", layout="wide")

# السطر التاسع المصحح (تغيير اسم الوسيط)
st.markdown("""
    <style>
    .main { background-color: #000000; color: #D4AF37; }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 10px; }
    h1 { color: #D4AF37; text-align: center; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_html=True)

# عنوان الموقع
st.title("✨ HKA Smart Analytics ✨")
st.write("---")

# ربط المفتاح السري
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
    else:
        st.warning("يرجى إضافة GOOGLE_API_KEY في إعدادات Secrets.")
except Exception as e:
    st.error(f"خطأ في إعدادات الذكاء الاصطناعي: {e}")

# منطقة رفع الملفات
uploaded_file = st.file_uploader("📂 ارفعي ملف البيانات الخاص بكِ (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    st.success("تم رفع الملف بنجاح!")
    st.info("الموقع الآن قيد التشغيل وجاهز للتحليل الذكي.")

st.write("---")
st.caption("Powered by HKA Designer & AI Solutions")
