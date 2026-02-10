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

st.markdown(
"""
<h1 style='text-align:center;color:#0A66C2;'>🇮🇳 JobVista India</h1>
<h4 style='text-align:center;'>Live Indian Tech Job Intelligence Dashboard</h4>
<p style='text-align:center;color:gray;'>Analyze hiring trends • Track in-demand skills • Explore latest tech jobs across India</p>
<hr>
""",
unsafe_allow_html=True
)



# ---------------- SIDEBAR JOB CONTROL ----------------
st.sidebar.title("Job Filter")

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

fetch_btn = st.sidebar.button(" Refresh Jobs 🔄")

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

    scraper = AdzunaScraper()
    jobs = scraper.fetch_jobs(keyword)

    if jobs:
        db = JobDatabase()
        db.clear_jobs()
        db.insert_jobs(jobs)

        st.sidebar.success(f" {len(jobs)} jobs fetched!")
        st.rerun()
    else:
        st.sidebar.error(" No jobs fetched")

# ---------------- LOAD DATABASE ----------------
db = JobDatabase()
rows = db.fetch_all_jobs()

if not rows:
    st.warning("No job data found. Click 'Fetch Latest Jobs' from sidebar.")
    st.stop()

columns = ["id","title","company","location","description","experience","salary","source","apply_link"]
df = pd.DataFrame(rows, columns=columns)

# Clean location
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
st.sidebar.title(" Filter Jobs 🔎")

locations = sorted(df["location"].dropna().unique().tolist())

location_filter = st.sidebar.selectbox("📍 City", ["All"] + locations)
if location_filter != "All":
    df = df[df["location"] == location_filter]

skill_filter = st.sidebar.selectbox(
    " Skill",
    ["All"] + (skill_df["Skill"].tolist() if not skill_df.empty else [])
)
if skill_filter != "All":
    df = df[df["description"].str.lower().str.contains(skill_filter.lower(), na=False)]

company_filter = st.sidebar.selectbox(
    " Company",
    ["All"] + sorted(df["company"].dropna().unique().tolist())
)
if company_filter != "All":
    df = df[df["company"] == company_filter]

# ---------------- METRICS ----------------
col1, col2, col3 = st.columns(3)
col1.metric(" Total Jobs", len(df))
col2.metric(" Companies Hiring", df["company"].nunique())
col3.metric("📍 Cities", df["location"].nunique())

st.markdown("---")

# ---------------- SKILL CHART ----------------
st.subheader(" Most In-Demand Skills")

if not skill_df.empty:
    top_skills = skill_df.head(10)

    fig = px.bar(
        top_skills,
        x="Skill",
        y="Count",
        text="Count",
        color="Count",
        color_continuous_scale="tealgrn"
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ---------------- CITY CHART ----------------
st.subheader("🇮🇳 Top Hiring Cities")

top_locations = df["location"].value_counts().head(10)

fig_loc = px.bar(
    x=top_locations.index,
    y=top_locations.values,
    labels={"x": "City", "y": "Jobs"},
    color=top_locations.values,
    color_continuous_scale="blues"
)

st.plotly_chart(fig_loc, use_container_width=True)

st.markdown("---")

# ---------------- PAGINATION ----------------
st.subheader(" Latest Jobs")

jobs_per_page = 50
total_jobs = len(df)

if total_jobs == 0:
    st.warning("No jobs found for selected filters.")
    st.stop()

total_pages = max(1, (total_jobs + jobs_per_page - 1) // jobs_per_page)

page = st.number_input(" Page", min_value=1, max_value=total_pages, step=1)

start = (page - 1) * jobs_per_page
end = start + jobs_per_page
df_page = df.iloc[start:end]

st.write(f"Showing page {page} of {total_pages}")

for _, row in df_page.iterrows():
    with st.container():
        c1, c2, c3, c4 = st.columns([3,2,2,2])

        c1.write(f"**{row['title']}**")
        c2.write(row["company"])
        c3.write(row["location"])

        if row["apply_link"]:
            c4.markdown(f"[🚀 Apply Now]({row['apply_link']})")
        else:
            c4.write("No link")

        st.markdown("---")

# ---------------- CAREER INSIGHT ----------------
st.subheader(" Hiring Trends & Recommendations")

if not skill_df.empty:

    top_skills = ", ".join(skill_df.head(3)["Skill"].str.upper().tolist())

    st.success(
        f" Based on live job market analysis, companies are actively hiring candidates skilled in {top_skills}. "
        "Upskilling in these areas can significantly improve interview shortlisting chances in India's tech market."
    )


# ---------------- PROFESSIONAL FOOTER ----------------
st.markdown("---")

st.markdown(
"""
<div style='text-align:center; color:gray; font-size:14px;'>

<b>JobVista India</b> — Real-time Tech Job Intelligence Dashboard <br><br>

Developed by <b>Gourmani Choudhary</b> <br>
Built using Python • Streamlit • Data Analytics • Live Job APIs <br><br>

 For learning & career insights in Indian tech job market

</div>
""",
unsafe_allow_html=True
)
