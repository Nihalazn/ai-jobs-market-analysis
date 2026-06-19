import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="AI Jobs Salary Predictor",
    page_icon="💼",
    layout="wide"
)

# ── Load data and model ───────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv('data/processed/cleaned_jobs.csv')

@st.cache_resource
def load_model():
    return joblib.load('models/xgboost_salary_predictor.pkl')

df = load_data()
model = load_model()

# ── Manual encoding maps ──────────────────────────────────
emp_map = {'PT': 3, 'CT': 0, 'FL': 1, 'FT': 2}
size_map = {'M': 1, 'L': 0, 'S': 2}
edu_map = {'Associate': 0, 'Bachelor': 1, 'PhD': 3, 'Master': 2}
currency_map = {'USD': 7, 'JPY': 5, 'EUR': 3, 'SGD': 6,
                'CAD': 1, 'AUD': 0, 'GBP': 4, 'CHF': 2}
exp_map = {'EN - Entry': 0, 'MI - Mid': 2,
           'SE - Senior': 3, 'EX - Executive': 1}

job_map = {
    'Data Scientist': 10, 'Head of AI': 12, 'Data Engineer': 9,
    'Computer Vision Engineer': 7, 'Robotics Engineer': 19,
    'AI Consultant': 1, 'Machine Learning Engineer': 14,
    'Deep Learning Engineer': 11, 'Principal Data Scientist': 17,
    'AI Product Manager': 2, 'Machine Learning Researcher': 15,
    'AI Software Engineer': 4, 'ML Ops Engineer': 13,
    'AI Architect': 0, 'AI Specialist': 5, 'Data Analyst': 8,
    'Research Scientist': 18, 'Autonomous Systems Engineer': 6,
    'NLP Engineer': 16, 'AI Research Scientist': 3
}

location_map = {
    'Sweden': 16, 'Japan': 11, 'Germany': 7, 'Finland': 5,
    'France': 6, 'Singapore': 14, 'Canada': 2, 'Australia': 0,
    'United Kingdom': 18, 'Denmark': 4, 'United States': 19,
    'Norway': 13, 'India': 8, 'Switzerland': 17,
    'Netherlands': 12, 'Ireland': 9, 'Austria': 1,
    'China': 3, 'Israel': 10, 'South Korea': 15
}

skills_map = {
    'Python': 2, 'SQL': 3, 'TensorFlow': 5, 'Tableau': 9,
    'R': 1, 'PyTorch': 7, 'AWS': 0, 'Docker': 4,
    'Spark': 11, 'Scala': 12, 'Kubernetes': 10,
    'GCP': 6, 'Hadoop': 8
}

industry_map = {
    'Transportation': 14, 'Automotive': 0, 'Finance': 4,
    'Technology': 12, 'Gaming': 5, 'Consulting': 1,
    'Government': 6, 'Telecommunications': 13, 'Healthcare': 7,
    'Education': 2, 'Energy': 3, 'Real Estate': 10,
    'Media': 9, 'Retail': 11, 'Manufacturing': 8
}

# ── Sidebar navigation ────────────────────────────────────
page = st.sidebar.selectbox("Navigate",
    ["Market Overview", "Salary Predictor"])

# ══════════════════════════════════════════════════════════
# PAGE 1 — Market Overview
# ══════════════════════════════════════════════════════════
if page == "Market Overview":
    st.header("📊 Market Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Jobs", f"{len(df):,}")
    col2.metric("Avg Salary", f"${df['salary_usd'].mean():,.0f}")
    col3.metric("Countries", df['company_location'].nunique())
    col4.metric("Job Titles", df['job_title'].nunique())

    st.divider()

    st.subheader("Average Salary by Experience Level")
    exp_salary = (df.groupby('experience_level')['salary_usd']
                    .mean().reset_index()
                    .sort_values('salary_usd', ascending=False))
    st.bar_chart(exp_salary.set_index('experience_level'))

    st.subheader("Top 10 Highest Paying Job Titles")
    top_jobs = (df.groupby('job_title')['salary_usd']
                  .mean().sort_values(ascending=False)
                  .head(10).reset_index())
    st.bar_chart(top_jobs.set_index('job_title'))

    st.subheader("Remote vs Hybrid vs On-site")
    remote_counts = df['remote_ratio'].value_counts().reset_index()
    remote_counts.columns = ['remote_ratio', 'count']
    st.bar_chart(remote_counts.set_index('remote_ratio'))

    st.subheader("Average Salary by Industry")
    industry_salary = (df.groupby('industry')['salary_usd']
                         .mean().sort_values(ascending=False)
                         .reset_index())
    st.bar_chart(industry_salary.set_index('industry'))

# ══════════════════════════════════════════════════════════
# PAGE 2 — Salary Predictor
# ══════════════════════════════════════════════════════════
elif page == "Salary Predictor":
    st.header("🔮 Predict Your Salary")
    st.markdown("Fill in your details to get a salary estimate.")

    col1, col2 = st.columns(2)

    with col1:
        experience_level = st.selectbox("Experience Level",
            ["EN - Entry", "MI - Mid",
             "SE - Senior", "EX - Executive"])
        employment_type = st.selectbox("Employment Type",
            ['FT', 'PT', 'CT', 'FL'])
        company_size = st.selectbox("Company Size",
            ['S', 'M', 'L'])
        remote_ratio = st.selectbox("Work Setting",
            [0, 50, 100],
            format_func=lambda x:
                "On-site" if x == 0
                else "Hybrid" if x == 50
                else "Remote")
        salary_currency = st.selectbox("Salary Currency",
            ['USD', 'EUR', 'GBP', 'JPY',
             'SGD', 'CAD', 'AUD', 'CHF'])

    with col2:
        years_experience = st.slider(
            "Years of Experience", 0, 20, 3)
        benefits_score = st.slider(
            "Benefits Score", 0.0, 10.0, 5.0)
        education = st.selectbox("Education Level",
            ['Associate', 'Bachelor', 'Master', 'PhD'])
        job_title = st.selectbox("Job Title",
            sorted(job_map.keys()))
        location = st.selectbox("Company Location",
            sorted(location_map.keys()))
        residence = st.selectbox("Employee Residence",
            sorted(location_map.keys()))
        skills = st.selectbox("Primary Skill",
            sorted(skills_map.keys()))
        industry = st.selectbox("Industry",
            sorted(industry_map.keys()))

    if st.button("Predict Salary", type="primary"):

        input_data = np.array([[
            currency_map[salary_currency],
            exp_map[experience_level],
            emp_map[employment_type],
            size_map[company_size],
            remote_ratio,
            edu_map[education],
            years_experience,
            benefits_score,
            job_map[job_title],
            location_map[location],
            location_map.get(residence, 0),
            skills_map[skills],
            industry_map[industry]
        ]])

        prediction = model.predict(input_data)[0]

        st.success(f"### Estimated Salary: ${prediction:,.0f} USD")
        st.caption(
            "Based on XGBoost model trained on 15,000 AI job listings")