import streamlit as st
from groq import Groq

#env setting 
from dotenv import load_dotenv#import library to secure ans store secret infromation
import os  #used  operating systems functions like file reading
load_dotenv()#.env file ku parhu or us mee likhi sari cheze laod kru 
client = Groq(api_key=os.getenv("GROQ_API_KEY"))  #os.getenv file se key le kr ao grok key
#grok(api_key) client ku bnao ta ky tum us ku identify kr sku

st.set_page_config(page_title="Fake News Detector", page_icon="🔍")

st.markdown("""
    <h1 style='text-align: center; color: #FF4B4B;'>🔍 Fake News Detector</h1>
    <p style='text-align: center; color: gray;'>Powered by AI — Paste any news to analyze</p>
    <hr>
""", unsafe_allow_html=True)

news = st.text_area("📰 Enter News Article or Headline:", height=200)

if st.button("🔎 Analyze Now"):
    if news:
        with st.spinner("AI is analyzing..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": f"""Analyze this news and tell me:
1. Is it REAL or FAKE or UNCERTAIN
2. Why do you think so
3. What are the red flags if any

News: {news}"""}
                ]
            )
            result = response.choices[0].message.content

            st.markdown("### 📊 Analysis Result:")
            st.info(result)
    else:
        st.warning("⚠️ Please enter some news first!")