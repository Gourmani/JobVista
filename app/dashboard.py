import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px
from db.database import JobDatabase
from core.skill_extractor import SkillExtractor
from core.adzuna_scraper import AdzunaScraper

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="JobVista India", page_icon="🇮🇳", layout="wide")

# HIDE DEFAULT PAGE NAV
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display:none;}
</style>
""", unsafe_allow_html=True)



# ---------------- PRO PREMIUM UI ----------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

/* ===== FULL APP BACKGROUND ===== */
.stApp {
    background: linear-gradient(120deg,#f8fafc,#eef2ff);
}

/* ===== HERO TITLE ===== */
.main-title {
    font-size: 60px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg,#2563eb,#7c3aed,#06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 10px;
    margin-bottom: 0px;
}

.subtitle {
    text-align:center;
    color:#475569;
    font-size:20px;
    margin-bottom:30px;
}

/* ===== PREMIUM METRIC CARDS ===== */
.metric-card {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(16px);
    padding: 34px;
    border-radius: 22px;
    text-align:center;
    border:1px solid rgba(255,255,255,0.5);
    box-shadow: 0 25px 60px rgba(0,0,0,0.08);
    transition:0.4s;
}

.metric-card:hover {
    transform: translateY(-10px) scale(1.03);
    box-shadow: 0 40px 80px rgba(37,99,235,0.2);
}

/* ===== JOB CARD ===== */
.job-card {
    padding:26px;
    border-radius:20px;
    background: rgba(255,255,255,0.9);
    backdrop-filter: blur(12px);
    margin-bottom:18px;
    border:1px solid #e2e8f0;
    box-shadow:0 15px 40px rgba(0,0,0,0.08);
    transition:0.4s;
}

.job-card:hover {
    transform:translateY(-7px) scale(1.01);
    box-shadow:0 30px 70px rgba(99,102,241,0.25);
    border:1px solid #6366f1;
}

/* ===== APPLY BUTTON ===== */
.job-card a {
    display:inline-block;
    margin-top:12px;
    background: linear-gradient(90deg,#4f46e5,#7c3aed);
    color:white !important;
    padding:12px 22px;
    border-radius:12px;
    text-decoration:none;
    font-weight:600;
}

.job-card a:hover {
    background: linear-gradient(90deg,#06b6d4,#4f46e5);
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#ffffff,#f1f5f9);
    border-right:1px solid #e5e7eb;
}

/* ===== BUTTONS ===== */
.stButton>button {
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    color:white;
    border-radius:12px;
    border:none;
    padding:12px 24px;
    font-weight:600;
    transition:0.3s;
}

.stButton>button:hover {
    transform:scale(1.07);
    background: linear-gradient(90deg,#06b6d4,#2563eb);
}

/* ===== FILE UPLOADER ===== */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.65);
    padding:16px;
    border-radius:16px;
    border:1px solid #e2e8f0;
}

/* ===== HEADINGS ===== */
h2, h3 {
    font-weight:700 !important;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-thumb {
  background: #c7d2fe;
  border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown("<div class='main-title'> JobVista India</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Live Indian Tech Jobs Dashboard</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)




# ---------------- SIDEBAR ----------------
st.sidebar.markdown("##  Navigatior")

page = st.sidebar.radio(
    "",
    ["🏠 Dashboard", "📄 Resume Analyzer"]
)

if page == "📄 Resume Analyzer":
    st.switch_page("pages/resume_analyzer.py")


st.sidebar.title(" Career Path")

domain_option = st.sidebar.selectbox(
    "Select Job Domain",
    [
        "Software Developer",
        "Data Science",
        "AI/ML",
        "Cloud/DevOps",
        "Frontend",
        "Backend",
        "Embedded/Automotive"
    ]
)
st.session_state["selected_domain"] = domain_option
fetch_btn = st.sidebar.button("Refresh Jobs 🔄")

if fetch_btn:
    keyword_map = {
        "Software Developer": "software developer",
        "Data Science": "data science",
        "AI/ML": "machine learning engineer",
        "Cloud/DevOps": "cloud engineer",
        "Frontend": "frontend developer",
        "Backend": "backend developer",
        "Embedded/Automotive": "embedded engineer"
    }

    keyword = keyword_map.get(domain_option, "software developer")

    with st.spinner("Fetching live jobs from Adzuna API..."):
        scraper = AdzunaScraper()
        jobs = scraper.fetch_jobs(keyword)

    if jobs:
        db = JobDatabase()
        db.clear_jobs()
        db.insert_jobs(jobs)
        st.sidebar.success(f"{len(jobs)} jobs fetched successfully!")
        st.rerun()
    else:
        st.sidebar.error("No jobs fetched")

# ---------------- LOAD DATABASE ----------------
db = JobDatabase()
rows = db.fetch_all_jobs()

if not rows:
    st.warning("⚠ No job data found. Fetch jobs from sidebar.")
    st.stop()

columns = ["id","title","company","location","description","experience","salary","source","apply_link"]
df = pd.DataFrame(rows, columns=columns)
df["location"] = df["location"].astype(str).str.split(",").str[0]

# ---------------- SKILL ANALYSIS ----------------
jobs_list = []
for _, row in df.iterrows():
    jobs_list.append(
        type("Job", (), {
            "title": row["title"],
            "company": row["company"],
            "location": row["location"],
            "description": row["description"],
            "experience": row["experience"],
            "salary": row["salary"],
            "source": row["source"]
        })
    )

skill_engine = SkillExtractor()
skill_counts = skill_engine.extract_skills_from_jobs(jobs_list)

skill_df = pd.DataFrame(skill_counts.items(), columns=["Skill","Count"])
skill_df = skill_df.sort_values(by="Count", ascending=False)

# ---------------- FILTERS ----------------
st.sidebar.title(" Filter Jobs By ")

locations = sorted(df["location"].dropna().unique().tolist())
location_filter = st.sidebar.selectbox("City", ["All"] + locations)
if location_filter != "All":
    df = df[df["location"] == location_filter]

skill_filter = st.sidebar.selectbox(
    "Skill",
    ["All"] + (skill_df["Skill"].tolist() if not skill_df.empty else [])
)
if skill_filter != "All":
    df = df[df["description"].str.lower().str.contains(skill_filter.lower(), na=False)]

company_filter = st.sidebar.selectbox(
    "Company",
    ["All"] + sorted(df["company"].dropna().unique().tolist())
)
if company_filter != "All":
    df = df[df["company"] == company_filter]





# ===================== DASHBOARD ANALYTICS =====================

st.markdown("##  Real-Time Job Market Insights")

# ---------------- METRICS (PREMIUM CARDS) ----------------
col1, col2, col3 = st.columns(3)

col1.markdown(f"""
<div style='background:white;padding:28px;border-radius:18px;
box-shadow:0 10px 25px rgba(0,0,0,0.08);text-align:center'>
<h1 style='color:#4f46e5;margin:0;font-size:40px'>{len(df)}</h1>
<p style='margin:0;color:gray;font-size:16px'>Total Live Jobs</p>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div style='background:white;padding:28px;border-radius:18px;
box-shadow:0 10px 25px rgba(0,0,0,0.08);text-align:center'>
<h1 style='color:#0ea5e9;margin:0;font-size:40px'>{df['company'].nunique()}</h1>
<p style='margin:0;color:gray;font-size:16px'>Companies Hiring</p>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div style='background:white;padding:28px;border-radius:18px;
box-shadow:0 10px 25px rgba(0,0,0,0.08);text-align:center'>
<h1 style='color:#10b981;margin:0;font-size:40px'>{df['location'].nunique()}</h1>
<p style='margin:0;color:gray;font-size:16px'>Active Cities</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- SKILL DEMAND CHART ----------------
st.markdown("###  Most In-Demand Skills in Market")

if not skill_df.empty:
    fig = px.bar(
        skill_df.head(10),
        x="Skill",
        y="Count",
        text="Count",
        color="Count",
        color_continuous_scale="blues"
    )

    fig.update_layout(
        height=420,
        template="ggplot2",
        xaxis_title="Skills",
        yaxis_title="Job Demand",
        title="Top Skills Companies Are Hiring For",
        title_x=0.3
    )

    st.plotly_chart(fig, use_container_width=True)
    st.caption("Insight: These skills are most demanded in current Indian tech job market.")

# ---------------- TOP CITIES CHART ----------------
st.markdown("### 📍 Top Hiring Cities in India")

top_locations = df["location"].value_counts().head(10)

fig_loc = px.bar(
    x=top_locations.index,
    y=top_locations.values,
    text=top_locations.values,
    color=top_locations.values,
    color_continuous_scale="teal"
)

fig_loc.update_layout(
    height=420,
    template="ggplot2",
    xaxis_title="City",
    yaxis_title="Number of Jobs",
    title="Cities With Highest Hiring",
    title_x=0.3
)

st.plotly_chart(fig_loc, use_container_width=True)
st.caption("Insight: Focus applying in these cities for higher selection probability.")



# ---------------- JOB LIST ----------------
st.subheader(" Latest Jobs")

jobs_per_page = 25
total_jobs = len(df)
total_pages = max(1, (total_jobs + jobs_per_page - 1) // jobs_per_page)

page = st.number_input("Page", min_value=1, max_value=total_pages, step=1)
start = (page - 1) * jobs_per_page
end = start + jobs_per_page
df_page = df.iloc[start:end]

st.write(f"Showing page {page} of {total_pages}")

for _, row in df_page.iterrows():
    st.markdown(f"""
    <div class='job-card'>
    <b>{row['title']}</b><br>
     {row['company']} &nbsp;&nbsp; 📍 {row['location']}<br><br>
    <a href="{row['apply_link']}" target="_blank">🚀 Apply Now</a>
    </div>
    """, unsafe_allow_html=True)

# ---------------- INSIGHT ----------------
st.subheader(" Hiring Trends & Recommendations")

if not skill_df.empty:

    top_skills = ", ".join(skill_df.head(3)["Skill"].str.upper().tolist())

    st.success(
        f" Based on live job market analysis, companies are actively hiring candidates skilled in {top_skills}. "
        "Upskilling in these areas can significantly improve interview shortlisting chances in India's tech market."
    )

# ===== RESUME AI SECTION (PRO UI) =====
st.markdown("##  Resume Skill Test")

st.markdown("""
<div style='background:linear-gradient(135deg,#4f46e5,#2563eb);
padding:28px;border-radius:18px;
box-shadow:0 20px 50px rgba(0,0,0,0.15);
color:white'>

<h3 style='margin-bottom:10px'>Check Your Resume Match Score</h3>

<p style='font-size:16px;opacity:0.95'>
Upload your resume → Get skill match score → Discover missing skills → 
Apply to best matching companies instantly.
</p>

<a href="/resume_analyzer" target="_self"
style="
display:inline-block;
margin-top:14px;
background:white;
color:#4f46e5;
padding:12px 22px;
border-radius:10px;
font-weight:600;
text-decoration:none;
">
 Analyze My Resume 🚀
</a>

</div>
""", unsafe_allow_html=True)




# ---------------- PREMIUM FOOTER ----------------
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div style="
background:linear-gradient(90deg,#0f172a,#020617);
padding:40px;
border-radius:18px;
text-align:center;
box-shadow:0 20px 60px rgba(0,0,0,0.25);
">

<h2 style="color:white;margin-bottom:6px">
 JobVista —  Dashboard  For Job Seeker
</h2>

<p style="color:#94a3b8;font-size:16px;margin-bottom:25px">
Real-time Job Intelligence • Resume Matching • Smart Job Suggestions
</p>

<div style="
height:1px;
background:linear-gradient(90deg,transparent,#334155,transparent);
margin:20px 0;">
</div>

<p style="color:#cbd5e1;font-size:15px">
Developed by <b style="color:white">Gourmani Choudhary</b>
</p>

<p style="color:#64748b;font-size:14px">
Python • Streamlit • Data Analytics • Live Job APIs
</p>

<p style="color:#475569;font-size:13px;margin-top:18px">
Built for developers to track market demand & get hired faster ⚡
</p>

</div>
""", unsafe_allow_html=True)
