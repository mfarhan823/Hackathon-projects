import streamlit as st

st.set_page_config(page_title="Mera App", page_icon="😊")

st.title("🌟 Assalamualaikum!")
st.write("Streamlit seekh raha hun - Alhamdulillah!")

# Button
if st.button("Click Karo"):
    st.balloons()
    st.success("Mubarak ho! Chal gaya!")

# Name input
name = st.text_input("Apna naam likho:")
if name:
    st.write(f"Namaste, **{name}**! 👋")

# Slider
age = st.slider("Apni umar batao", 1, 100, 18)
st.write(f"Umr: {age} saal")