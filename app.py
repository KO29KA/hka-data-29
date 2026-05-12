import streamlit as st
import pandas as pd
import google.generativeai as genai

# إعداد واجهة الصفحة بلمساتك كمصممة جرافيك
st.set_page_config(page_title="HKA Smart Analytics", page_icon="📊", layout="wide")

# تطبيق ثيم الألوان (الأسود والذهبي)
st.markdown("""
    <style>
    .main { background-color: #000000; color: #D4AF37; }
    .stButton>button { background-color: #D4AF37; color: black; border-radius: 10px; }
    h1 { color: #D4AF37; text-align: center; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_complete_html=True)

# عنوان الموقع بشعارك المفضل
st.title("✨ HKA Smart Analytics ✨")
st.write("---")

# ربط المفتاح السري الذي وضعتيه في Secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("يرجى التأكد من إعداد المفتاح السري (Secrets) بشكل صحيح.")

# منطقة رفع الملفات (Excel / CSV)
uploaded_file = st.file_uploader("📂 ارفعي ملف البيانات الخاص بكِ (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success("تم رفع الملف بنجاح!")
        st.write("### نظرة سريعة على بياناتك:", df.head())
        
        # هنا سيتم إضافة ميزات التحليل الذكي وتوليد الإنفوجرافيك لاحقاً
        st.info("الموقع الآن قيد التشغيل وجاهز للتحليل الذكي.")
        
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

st.write("---")
st.caption("Powered by HKA Designer & AI Solutions")
