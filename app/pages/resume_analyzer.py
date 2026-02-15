import streamlit as st
import pdfplumber

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Resume Analyzer", page_icon="🚀", layout="wide")

# ---------------- PREMIUM UI STYLE ----------------
st.markdown("""
<style>
.stApp{
    background: linear-gradient(120deg,#f8fafc,#eef2ff);
}
</style>
""", unsafe_allow_html=True)

# ================= HERO HEADER =================
st.markdown("""
<div style='
background:linear-gradient(135deg,#4f46e5,#06b6d4);
padding:38px;
border-radius:18px;
color:white;
text-align:center;
box-shadow:0 20px 50px rgba(0,0,0,0.15);
'>

<h1 style='margin-bottom:8px'>🚀 Resume Role Fit Analyzer</h1>

<p style='font-size:18px;opacity:0.95'>
Upload your resume • Choose target role • 
See how job-ready you are in today's tech market
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ================= ROLE SKILLS =================
ROLE_SKILLS = {

"Software Developer": [
"python","java","c++","javascript",
"sql","mysql","postgresql",
"git","github","api","rest api",
"data structures","algorithms","oop",
"linux","docker"
],

"Python Developer": [
"python","django","flask","fastapi",
"sql","postgresql","mysql",
"rest api","json","pandas",
"git","docker"
],

"Backend Developer": [
"java","spring","springboot",
"node","express",
"django","flask",
"sql","mongodb",
"api","microservices","docker"
],

"Frontend Developer": [
"html","css","javascript",
"react","angular","vue",
"typescript","bootstrap","tailwind",
"api","responsive"
],

"AI/ML Engineer": [
"python","machine learning","deep learning",
"pandas","numpy","scikit","tensorflow","pytorch",
"nlp","data science"
],

"Data Analyst": [
"sql","excel","power bi","tableau",
"python","pandas","numpy",
"data visualization","statistics"
],

"QA/Test Engineer": [
"testing","selenium","pytest",
"automation","manual testing",
"api testing","postman","jira"
],

"Embedded/Automotive": [
"c","c++","embedded","rtos",
"can","autosar","matlab","simulink",
"microcontroller","iot"
]

}

# ================= UPLOAD BOX =================

st.markdown("""
<style>

/* Upload box full styling */
[data-testid="stFileUploader"] {
    background: white;
    padding: 30px;
    border-radius: 18px;
    border: 2px dashed #c7d2fe;
    box-shadow: 0 10px 35px rgba(0,0,0,0.08);
}

/* Remove default ugly border */
[data-testid="stFileUploader"] section {
    border: none;
}

/* Center everything */
[data-testid="stFileUploader"] div {
    text-align:center;
}

/* Browse button styling */
[data-testid="stFileUploader"] button {
    background: linear-gradient(90deg,#4f46e5,#7c3aed);
    color: white;
    border-radius: 10px;
    padding: 10px 22px;
    border: none;
    font-weight: 600;
    margin-top: 10px;
}

[data-testid="stFileUploader"] button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg,#06b6d4,#4f46e5);
}

</style>
""", unsafe_allow_html=True)

st.markdown("### 📄 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Drag & Drop your resume here or click Browse",
    type=["pdf"],
    label_visibility="collapsed"
)

# ---------- PDF TEXT EXTRACT FUNCTION ----------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content.lower() + " "
    return text



# ================= MAIN =================
if uploaded_file:

    resume_text = extract_text_from_pdf(uploaded_file)

    if resume_text.strip() == "":
        st.error("Unable to read resume text")
        st.stop()

    st.success("Resume uploaded & analyzed successfully")

    # ================= ROLE SELECT =================
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style='
    background:white;
    padding:22px;
    border-radius:16px;
    box-shadow:0 10px 30px rgba(0,0,0,0.08);
    '>
    <h3>🎯 Choose Your Target Role</h3>
    <p style='color:gray'>Select role you want to apply for</p>
    </div>
    """, unsafe_allow_html=True)

    target_role = st.selectbox("", list(ROLE_SKILLS.keys()))
    required_skills = ROLE_SKILLS[target_role]

    # ================= MATCHING =================
    matched = []
    missing = []

    for skill in required_skills:
        if skill.lower() in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)

    match_percent = int((len(matched)/len(required_skills))*100)

    # ================= SCORE CARD =================
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='
    background:linear-gradient(135deg,#111827,#1f2937);
    padding:28px;
    border-radius:18px;
    color:white;
    box-shadow:0 25px 60px rgba(0,0,0,0.25);
    '>

    <h2>📊 Resume Match Score</h2>
    <h1 style='font-size:60px;margin:10px 0'>{match_percent}%</h1>

    <p style='font-size:18px'>
    {"🔥 Excellent — Job Ready" if match_percent>=80 else 
     "⚡ Good — Improve few skills" if match_percent>=60 else 
     "🛠 Upskill needed"}
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.progress(match_percent/100)
    st.markdown("---")

    # ================= SKILLS FOUND =================
    st.markdown("## ✅ Skills Detected In Your Resume")

    if matched:
        for s in matched:
            st.write("✔", s)
    else:
        st.warning("No major required skills detected")

    # ================= SKILL BOOST =================
    st.markdown("## 🚀 Skills That Can Increase Your Hiring Chances")

    if missing:
        st.info(f"Learning these skills will boost your hiring chances for **{target_role}**")

        for s in missing[:10]:
            st.write("⭐", s)
    else:
        st.success("Your profile matches most in-demand skills 🔥")

    # ================= CAREER GUIDANCE =================
    st.markdown("## 🧭 Career Guidance")

    if match_percent >= 80:
        st.success("You are ready. Start applying aggressively on LinkedIn & Naukri.")

    elif match_percent >= 60:
        st.info(f"Focus on {', '.join(missing[:3])} to become strong candidate in 2-4 weeks.")

    else:
        st.warning("Focus on core skills + projects first. Then start applying.")

    # ================= ROADMAP =================
    st.markdown("## 📚 Suggested Learning Roadmap")

    if missing:
        for skill in missing[:6]:
            st.markdown(f"""
            <div style='background:white;padding:14px;border-radius:12px;
            margin-bottom:10px;border-left:5px solid #4f46e5;
            box-shadow:0 5px 15px rgba(0,0,0,0.06)'>
            📌 Learn <b>{skill.upper()}</b> → High impact skill for {target_role}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.success("💡 Tip: Update resume after learning new skills and recheck score.")
