import streamlit as st  #library
from groq import Groq   #library
#env setting 
from dotenv import load_dotenv#import library to secure ans store secret infromation
import os  #used  operating systems functions like file reading
load_dotenv()#.env file ku parhu or us mee likhi sari cheze laod kru 
client = Groq(api_key=os.getenv("GROQ_API_KEY"))  #os.getenv file se key le kr ao grok key
#grok(api_key) client ku bnao ta ky tum us ku identify kr sku



# st are functions

st.set_page_config(page_title="CGPA Calculator", page_icon="🎓")

st.markdown("""
    <h1 style='text-align: center; color: #4B9EFF;'>🎓 CGPA Calculator & AI Advisor</h1>
    <p style='text-align: center; color: gray;'>CUI Wah — Smart Academic Tool</p>
    <hr>
""", unsafe_allow_html=True)

# side bar

with st.sidebar:
    st.markdown("### 📋 Grade Scale")
    st.markdown("""
    | Marks | Grade | Points |
    |-------|-------|--------|
    | 85-100 | A  | 4.0  |
    | 80-84  | A- | 3.67 |           
    | 75-79  | B+ | 3.33 |
    | 71-74  | B  | 3.0  |
    | 68-70  | B- | 2.67 |
    | 64-67  | C+ | 2.33 |
    | 60-63  | C  | 2.0  |
    | 57-59  | C- | 1.67 |
    | 53-56  | D+ | 1.33 |
    | 50-52  | D  | 1.0  |
    | Below 50 | F | 0.0 |
    """)

# Refresh
if st.button("🔄 Refresh"):
   st.session_state["name_input"]=""
   st.session_state["roll_input"]=""
   st.session_state.clear()
   st.rerun()



#Student information
st.markdown("### 👤 Step 1: Student Information")
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Full Name", key ="name_input")
with col2:
    roll_no = st.text_input("Roll Number", key="roll_input")

if name and roll_no:
    st.success(f"Welcome, {name}!")

    st.markdown("### 🎯 Step 2: What do you want to calculate?")
    choice = st.radio("Select:", ["SGPA — Current Semester Only", "CGPA — All Semesters Combined"])

    if choice == "SGPA — Current Semester Only":
        st.markdown("### 📚 Step 3: Enter Your Subjects")
        semester = st.selectbox("Current Semester", ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"])
        num_subjects = st.number_input("How many subjects?", min_value=1, max_value=10, value=5)

  #calculation
        def marks_to_grade(marks):
            if marks >= 85: return "A", 4.0
            elif marks >= 80: return "A-", 3.67
            elif marks >= 75: return "B+", 3.33
            elif marks >= 71: return "B", 3.0
            elif marks >= 68: return "B-", 2.67
            elif marks >= 64: return "C+", 2.33
            elif marks >= 60: return "C", 2.0
            elif marks >= 57: return "C-", 1.67
            elif marks >= 53: return "D+", 1.33
            elif marks >= 50: return "D", 1.0
            else: return "F", 0.0

        subjects = []
        for i in range(int(num_subjects)):
            col1, col2, col3 = st.columns(3)
            with col1:
                subject_name = st.text_input(f"Subject {i+1}", key=f"name_{i}")
            with col2:
                marks = st.number_input(f"Marks", min_value=0, max_value=100, value=75, key=f"marks_{i}")
            with col3:
                credit_hours = st.number_input(f"Credits", min_value=1, max_value=4, value=3, key=f"credit_{i}")
            grade, points = marks_to_grade(marks)
            st.caption(f"Grade: **{grade}** | Points: **{points}**")
            subjects.append({"name": subject_name, "marks": marks, "grade": grade, "points": points, "credit_hours": credit_hours})
#calculate button and advice of Ai
        if st.button("🧮 Calculate SGPA & Get AI Advice"):
            total_points = sum(s["points"] * s["credit_hours"] for s in subjects)
            total_credits = sum(s["credit_hours"] for s in subjects)
            sgpa = total_points / total_credits if total_credits > 0 else 0
            subject_details = "\n".join([f"- {s['name']}: {s['marks']} marks, {s['grade']}" for s in subjects])

            st.markdown("---")
            st.markdown(f"### 📊 Results for {name} | {roll_no} | {semester} Semester")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🎯 SGPA", f"{sgpa:.2f} / 4.0")
            with col2:
                st.metric("📚 Total Credits", total_credits)
            with col3:
                status = "Excellent 🌟" if sgpa >= 3.5 else "Good 👍" if sgpa >= 3.0 else "Average ⚠️" if sgpa >= 2.0 else "Critical ❌"
                st.metric("Status", status)

            if sgpa >= 3.5:
                st.success("🌟 Outstanding! Dean's List level!")
            elif sgpa >= 3.0:
                st.info("👍 Good performance!")
            elif sgpa >= 2.0:
                st.warning("⚠️ Needs improvement!")
            else:
                st.error("❌ Critical — act now!")

            st.markdown("### 📈 Subject wise Result")
            for s in subjects:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"📖 {s['name']}")
                with col2:
                    st.write(f"Marks: {s['marks']} | Grade: {s['grade']}")
                with col3:
                    st.write(f"Points: {s['points']}")
#use exception if net was not connectted it perfrommcalculation but can not provide a suggestion
            try:
                with st.spinner("🤖 AI analyzing..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"""Student: {name}
Semester: {semester}
SGPA: {sgpa:.2f}
Subjects:
{subject_details}
Give:
1. Performance analysis
2. Weak subjects and tips
3. Study strategy
4. Motivation"""}]
                    )
                    advice = response.choices[0].message.content
            except:
                advice = "⚠️ No internet — AI suggestions unavailable. SGPA calculated successfully."

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🤖 AI Suggestions")
                st.info(advice)
            with col2:
                st.markdown("### 📊 Summary")
                st.success(f"""
                **Name:** {name}
                **Roll No:** {roll_no}
                **Semester:** {semester}
                **Credits:** {total_credits}
                **SGPA:** {sgpa:.2f} / 4.0
                **Status:** {status}
                """)
#for cgpa calculation
    elif choice == "CGPA — All Semesters Combined":
        st.markdown("### 📚 Step 3: Enter SGPA of Each Semester")
        completed = st.number_input("How many semesters completed?", min_value=1, max_value=8, value=2)

        sgpa_list = []
        for i in range(int(completed)):
            sgpa = st.number_input(f"Semester {i+1} SGPA", min_value=0.0, max_value=4.0, value=3.0, step=0.01, key=f"sgpa_{i}")
            sgpa_list.append(sgpa)

        if st.button("📊 Calculate CGPA & Get AI Advice"):
            cgpa = sum(sgpa_list) / len(sgpa_list)

            st.markdown("---")
            st.markdown(f"### 📊 Overall Results for {name} | {roll_no}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("🎯 Overall CGPA", f"{cgpa:.2f} / 4.0")
            with col2:
                status = "Excellent 🌟" if cgpa >= 3.5 else "Good 👍" if cgpa >= 3.0 else "Average ⚠️" if cgpa >= 2.0 else "Critical ❌"
                st.metric("Status", status)

            if cgpa >= 3.5:
                st.success("🌟 Outstanding CGPA!")
            elif cgpa >= 3.0:
                st.info("👍 Good overall performance!")
            elif cgpa >= 2.0:
                st.warning("⚠️ Needs serious improvement!")
            else:
                st.error("❌ Critical CGPA — act immediately!")

            semester_details = "\n".join([f"Semester {i+1}: {sgpa_list[i]:.2f}" for i in range(len(sgpa_list))])
# same exception
            try:
                with st.spinner("🤖 AI analyzing your overall performance..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": f"""Student: {name}
Overall CGPA: {cgpa:.2f}
Semester wise SGPA:
{semester_details}
Give:
1. Overall academic journey analysis
2. Improvement or decline trend
3. How to improve CGPA
4. Career advice based on CGPA
5. Motivation"""}]
                    )
                    advice = response.choices[0].message.content
            except:
                advice = "⚠️ No internet — AI suggestions unavailable. CGPA calculated successfully."

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🤖 AI Suggestions")
                st.info(advice)
            with col2:
                st.markdown("### 📊 Summary")   # summary at the end of student
                st.success(f"""
                **Name:** {name}
                **Roll No:** {roll_no}
                **Semesters:** {completed}
                **Overall CGPA:** {cgpa:.2f} / 4.0
                **Status:** {status}
                """)