import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

st.set_page_config(
    page_title="AI Content Repurposer",
    page_icon="🚀",
    layout="wide",
)

# Custom CSS for gorgeous UI
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 AI Content Repurposer (أداة تحويل المحتوى الذكية)")
st.markdown("حول أي مقال أو رابط إلى **تغريدات Twitter**، **منشورات LinkedIn**، و**نشرات إخبارية** بضغطة زر واحدة!")

# Sidebar for API Key & Settings
with st.sidebar:
    st.header("⚙️ الإعدادات")
    api_key = st.text_input("OpenAI API Key", type="password")
    model_choice = st.selectbox("الموديل", ["gpt-4o-mini", "gpt-4o"])
    
    st.divider()
    st.markdown("### 📈 خطة التسويق والإطلاق السريع")
    st.markdown("""
    1. **Product Hunt Launch:** انشر الأداة اليوم على Product Hunt.
    2. **Twitter/X Build in Public:** انشر لقطات شاشة لنتائج الأداة مع هاشتاغ #BuildInPublic.
    3. **Reddit & Facebook:** انشر في مجتمعات صناع المحتوى والمسوقين.
    4. **Pricing:** $15/شهر أو باقة 50 مقال مجاناً ثم $9.
    """)

# Main Tabs
tab1, tab2 = st.tabs(["✨ مولد المحتوى", "📋 دليل التسويق والنشر"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📥 إدخال المحتوى")
        input_type = st.radio("اختر طريقة الإدخال:", ["رابط مقال (URL)", "نص مباشر"])
        
        content_input = ""
        if input_type == "رابط مقال (URL)":
            url = st.text_input("أدخل رابط المقال هنا:")
            if url and st.button("جلب المحتوى"):
                try:
                    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    paragraphs = soup.find_all('p')
                    content_input = "\n".join([p.get_text() for p in paragraphs])
                    st.success("تم جلب المقال بنجاح!")
                except Exception as e:
                    st.error(f"خطأ في جلب الرابط: {e}")
        else:
            content_input = st.text_area("ألصق المقال أو النص هنا:", height=200)
            
        tone = st.selectbox("نبرة الصوت:", ["احترافية", "حماسية", "تعليمية", "تحفيزية"])
        generate_btn = st.button("🚀 توليد المحتوى الآن")

    with col2:
        st.subheader("📤 النتائج المولدة")
        
        if generate_btn:
            if not api_key:
                st.error("الرجاء إدخال مفتاح OpenAI API في الشريط الجانبي.")
            elif not content_input.strip():
                st.error("الرجاء إدخال محتوى أو رابط صالح.")
            else:
                client = openai.OpenAI(api_key=api_key)
                
                with st.spinner("جاري صياغة المحتوى بالذكاء الاصطناعي..."):
                    prompt = f"""
                    قم بتحويل النص التالي إلى 3 أشكال محتوى بنبرة ({tone}):
                    1. Twitter Thread (سلسلة من 5 تغريدات مقسمة بـ ---).
                    2. LinkedIn Post (منشور احترافي وجذاب مع إيموجي وهاشتاغات).
                    3. Newsletter Summary (ملخص قصير ومفيد لنشرة إخبارية).
                    
                    النص:
                    {content_input[:4000]}
                    """
                    
                    try:
                        response = client.chat.completions.create(
                            model=model_choice,
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.7
                        )
                        result = response.choices[0].message.content
                        
                        st.markdown(result)
                        st.download_button("تحميل النتائج كملف Text", result, file_name="repurposed_content.txt")
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء الاتصال بـ OpenAI: {e}")

with tab2:
    st.subheader("📢 دليل التسويق والنشر السريع (خلال 24 ساعة)")
    st.markdown("""
    ### 1. إطلاق Product Hunt:
    - جهز صور الشعار ولقطات الشاشة للأداة.
    - اكتب وصفاً قصيراً: *"Turn any article into viral tweets and LinkedIn posts in 1 click using AI."*
    - اطلب من أصدقائك ومجتمعاتك دعم الإطلاق في أول ساعتين.

    ### 2. التسويق على تويتر (X) و LinkedIn:
    - انشر فيديو مدته 30 ثانية يظهر كيف حولت مقالاً طويلاً إلى تغريدات خلال 5 ثوانٍ.
    - استخدم هاشتاغات: `#AI #ContentCreator #BuildInPublic #IndieHacker`.

    ### 3. مجموعات Reddit & Facebook:
    - انشر في مجتمعات مثل `r/SaaS`, `r/Entrepreneur`, `r/ContentMarketing`.
    - لا تقم بالترويج المباشر بفظاظة، بل قل: *"بنيت هذه الأداة خلال أيام لحل مشكلتي في نشر المقالات، جربوها وأخبروني برأيكم (توجد باقة مجانية)."*
    """)
