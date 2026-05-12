import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="HKA Smart Analytics",
    page_icon="📊",
    layout="wide"
)

# 2. تصميم الواجهة (هوية HKA بالأسود والذهبي)
st.markdown("""
    <style>
    /* الخلفية والنصوص العامة */
    .main { background-color: #000000; color: #D4AF37; }
    /* تنسيق العناوين */
    h1, h2, h3 { color: #D4AF37 !important; text-align: center; font-family: 'Arial'; }
    /* تنسيق الأزرار */
    .stButton>button { 
        background-color: #D4AF37; 
        color: black; 
        font-weight: bold; 
        border-radius: 10px; 
        width: 100%;
        border: none;
    }
    .stButton>button:hover { background-color: #B8860B; color: white; }
    /* تنسيق خانة رفع الملفات */
    .stFileUploader { color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

# 3. عنوان المنصة
st.title("✨ HKA Smart Analytics ✨")
st.markdown("<p style='text-align: center; color: #D4AF37;'>منصتك الذكية لتحليل البيانات وتوليد الرؤى</p>", unsafe_allow_html=True)
st.write("---")

# 4. إعداد مفتاح Google AI (Gemini)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    else:
        st.warning("⚠️ يرجى إضافة GOOGLE_API_KEY في إعدادات Secrets لتفعيل التحليل الذكي.")
except Exception as e:
    st.error(f"خطأ في إعدادات الذكاء الاصطناعي: {e}")

# 5. منطقة رفع الملفات
uploaded_file = st.file_uploader("📂 ارفعي ملف البيانات (CSV أو Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # قراءة الملف حسب نوعه مع معالجة ملفات الإكسل
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            # استخدام engine='openpyxl' لضمان قراءة ملفات الإكسل الحديثة
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        st.success("✅ تم رفع الملف وقراءته بنجاح!")

        # 6. عرض ملخص رقمي (Dashboard مصغر)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("عدد الصفوف", df.shape[0])
        with col2:
            st.metric("عدد الأعمدة", df.shape[1])
        with col3:
            st.metric("الخلايا الفارغة", df.isnull().sum().sum())

        st.write("### 📋 معاينة البيانات")
        st.dataframe(df.head(10)) # عرض أول 10 أسطر

        st.write("---")

        # 7. قسم التحليل الذكي باستخدام Gemini
        st.subheader("🤖 اسألي HKA AI عن بياناتك")
        user_question = st.text_input("مثال: لخص لي أهم الاستنتاجات، أو ما هو أكثر عمود يحتوي على بيانات؟")

        if st.button("بدء التحليل الذكي"):
            if user_question:
                with st.spinner("انتظري قليلاً.. HKA AI يحلل بياناتك الآن..."):
                    try:
                        # تجهيز سياق البيانات للذكاء الاصطناعي (أعمدة + عينة صغيرة)
                        data_context = f"الأعمدة: {list(df.columns)}. عينة بيانات: {df.head(3).to_string()}"
                        prompt = f"أنت خبير تحليل بيانات. إليك ملخص لبياناتي: {data_context}. السؤال هو: {user_question}"
                        
                        response = model.generate_content(prompt)
                        st.markdown("#### 💡 نتيجة التحليل:")
                        st.info(response.text)
                    except Exception as e:
                        st.error(f"عذراً، حدث خطأ أثناء التحليل: {e}")
            else:
                st.warning("يرجى كتابة سؤال أولاً.")

    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء معالجة الملف: {e}")

# 8. التذييل (Footer)
st.write("---")
st.markdown("<p style='text-align: center; font-size: 0.8em;'>Powered by HKA Designer & AI Solutions | 2026</p>", unsafe_allow_html=True)
