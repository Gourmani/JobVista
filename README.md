# JobVista — Job Search Website

JobVista is a real-time developer job intelligence platform that analyzes live job market data and helps software engineers understand hiring trends, required skills, and role readiness.

It is designed as a decision-support dashboard for job seekers to align their skills with current industry demand and apply strategically.

---

## Overview

The platform fetches live job data across multiple software domains and converts it into actionable insights such as:

- Hiring demand by role and city  
- Most requested technical skills  
- Companies actively hiring  
- Resume-to-job skill alignment  
- Role-based readiness analysis  

This enables developers to understand where they stand in the market and what to improve to get hired faster.

---

## Core Features

### Live Job Market Dashboard
- Real-time job data from external APIs  
- Total open roles across domains  
- Hiring companies overview  
- Top hiring cities  
- Skill demand analytics  

### Intelligent Filtering System
- Filter jobs by role/domain  
- Filter by company  
- Filter by location  
- Filter by required skills  

### Resume Role Fit Analyzer
Allows users to:
- Upload resume (PDF)
- Select target job role
- Evaluate skill match against industry requirements
- Identify skill gaps
- Receive structured improvement suggestions

### Role-Based Hiring Readiness Score
Provides:
- Resume match percentage
- Skills detected vs missing
- Hiring readiness status
- Learning roadmap for improvement

### Direct Job Application
Users can apply directly to matching job listings through provided links.

---

## Technology Stack

### Frontend & Interface
- Streamlit (interactive dashboard UI)
- Plotly (data visualization)

### Backend & Processing
- Python
- REST API integration (Adzuna Jobs API)
- SQLite database
- Resume parsing (PDF processing)

### Engineering Practices
- Modular architecture
- Role-based skill intelligence system
- Data-driven recommendations
- Environment-based configuration
- Version control with Git

---

## System Workflow

1. User selects job domain  
2. System fetches live job data from API  
3. Job data stored in local database  
4. Skill extraction engine analyzes demand  
5. Dashboard visualizes hiring insights  
6. Resume analyzer evaluates user readiness  
7. System recommends skills and roles to target  

---

## Use Case

This project is intended for:

- Software developers preparing for job switches  
- Fresh graduates entering tech industry  
- Professionals evaluating market demand  
- Recruiters analyzing hiring trends  

---

## Project Status

Actively developed with:
- Resume intelligence system  
- Role-based job readiness scoring  
- Advanced UI improvements  
- Market-aligned skill analysis  

---

## Developer

Gourmani Choudhary  
Software Developer  

This project is built to bridge the gap between developer skills and real hiring demand in the software industry.
