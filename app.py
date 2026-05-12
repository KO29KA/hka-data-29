import streamlit as st
import pandas as pd
import google.generativeai as genai

# إعداد واجهة الصفحة
st.set_page_config(page_title="HKA Smart Analytics", page_icon="📊", layout="wide")

# التصميم (الأسود والذهبي)
st.markdown("""
    <style>
    .main { background-color: #000000; color: #D4AF37; }
    .stButton>button { background-color: #D4AF37; color: black; width: 100%; border-radius: 10px; }
    h1, h2, h3 { color: #D4AF37; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ HKA Smart Analytics ✨")

# ربط الذكاء الاصطناعي
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')

# منطقة الرفع
uploaded_file = st.file_uploader("📂 ارفعي ملف البيانات الخاص بكِ (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    # 1. قراءة البيانات
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        
        st.success("✅ تم استلام ملفك بنجاح!")
        
        # 2. عرض ملخص سريع للبيانات (إنفوجرافيك أولي)
        col1, col2, col3 = st.columns(3)
        col1.metric("عدد الأسطر", len(df))
        col2.metric("عدد الأعمدة", len(df.columns))
        col3.metric("القيم المفقودة", df.isnull().sum().sum())

        st.write("### 📋 معاينة البيانات:")
        st.dataframe(df.head(10)) # عرض أول 10 أسطر بشكل أنيق

        # 3. زر "اطلب من الذكاء الاصطناعي تحليل البيانات"
        st.write("---")
        user_question = st.text_input("💬 ماذا تريدين أن تعرفي عن هذه البيانات؟ (مثلاً: لخص لي أهم النتائج)")
        
        if st.button("تحليل الآن"):
            with st.spinner("HKA AI يقوم بتحليل بياناتك..."):
                # إرسال وصف البيانات للذكاء الاصطناعي
                prompt = f"لديك بيانات تحتوي على الأعمدة التالية: {list(df.columns)}. وبناءً على أول 5 أسطر: {df.head().to_string()}. {user_question}"
                response = model.generate_content(prompt)
                st.markdown("### 🤖 نتائج التحليل الذكي:")
                st.write(response.text)

    except Exception as e:
        st.error(f"حدث خطأ: {e}")

st.write("---")
st.caption("Powered by HKA Designer & AI Solutions")
