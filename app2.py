import streamlit as st
from groq import Groq

#env setting 
from dotenv import load_dotenv#import library to secure ans store secret infromation
import os  #used  operating systems functions like file reading
load_dotenv()#.env file ku parhu or us mee likhi sari cheze laod kru 
client = Groq(api_key=os.getenv("GROQ_API_KEY"))  #os.getenv file se key le kr ao grok key
#grok(api_key) client ku bnao ta ky tum us ku identify kr sku

st.title("Farhan Text Summarizer")

text = st.text_area("Enter your text here:")

if st.button("Summarize"):
    if text:
        with st.spinner("Summarizing..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": f"Summarize the text in clear bullet points, covering only the most important point, : {text}"}
                ]
            )
            summary = response.choices[0].message.content
            st.success("Summary:")
            st.write(summary)
    else:
        st.warning("Please enter some text first!")