import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Chronic OPD Lab Severity",
    layout="wide"
)

# ==========================================================
# GLOBAL FONT & STYLE (Professional Look)
# ==========================================================

st.markdown("""
<style>
body {
    font-family: 'Segoe UI', sans-serif;
}
.big-title {
    font-size: 48px;
    font-weight: 700;
}
.section-title {
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 20px;
}
.metric-large {
    font-size: 28px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_parquet("NB06_MULTIMODAL_SEVERITY_FUSION.parquet")

df = load_data()

# ==========================================================
# HEADER
# ==========================================================

st.markdown("<div class='big-title'>Chronic OPD Laboratory Severity Analysis</div>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================================
# SIDEBAR – PATIENT SELECT
# ==========================================================

selected_hadm = st.sidebar.selectbox(
    "Select Admission ID",
    df["hadm_id"].unique()
)

patient = df[df["hadm_id"] == selected_hadm].iloc[0]

# ==========================================================
# TABS (Separate Visual Sections)
# ==========================================================

tab1, tab2, tab3 = st.tabs([
    "Patient Overview",
    "Disease Breakdown",
    "Cohort Analytics"
])

# ==========================================================
# TAB 1 – PATIENT OVERVIEW
# ==========================================================

with tab1:

    st.markdown("<div class='section-title'>Patient Overview</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<div class='metric-large'>Subject ID: {patient['subject_id']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-large'>Admission ID: {patient['hadm_id']}</div>", unsafe_allow_html=True)

        diseases = []
        if patient["has_ckd"]:
            diseases.append("CKD")
        if patient["has_diabetes"]:
            diseases.append("Diabetes")
        if patient["has_thyroid"]:
            diseases.append("Thyroid")

        st.markdown(f"<div class='metric-large'>Chronic Conditions: {', '.join(diseases)}</div>", unsafe_allow_html=True)

    with col2:
        severity = patient["final_severity_label"]
        score = patient["final_severity_score"]

        st.markdown(f"""
        <div style="
            font-size:40px;
            font-weight:700;
            color:#1F2937;">
            Final Severity: {severity}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="
            font-size:28px;
            margin-top:10px;">
            Severity Score: {score}
        </div>
        """, unsafe_allow_html=True)

    # Optional Image Insert
    st.markdown("### Laboratory Module")
    st.image("https://images.unsplash.com/photo-1582719478250-c89cae4dc85b",
             use_container_width=True)

# ==========================================================
# TAB 2 – DISEASE BREAKDOWN
# ==========================================================

with tab2:

    st.markdown("<div class='section-title'>Individual Disease Severity</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### CKD")
        st.markdown(f"<div class='metric-large'>{patient.get('ckd_severity', 'N/A')}</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("### Diabetes")
        st.markdown(f"<div class='metric-large'>{patient.get('diabetes_severity_final', 'N/A')}</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("### Thyroid")
        st.markdown(f"<div class='metric-large'>{patient.get('thyroid_severity_final', 'N/A')}</div>", unsafe_allow_html=True)

# ==========================================================
# TAB 3 – COHORT ANALYTICS
# ==========================================================

with tab3:

    st.markdown("<div class='section-title'>Cohort Severity Distribution</div>", unsafe_allow_html=True)

    order = ["Stable", "Mild", "Moderate", "Severe", "Unknown"]

    distribution = (
        df["final_severity_label"]
        .value_counts()
        .reindex(order)
        .reset_index()
    )

    distribution.columns = ["Severity", "Count"]

    color_map = {
        "Stable": "#2ECC71",
        "Mild": "#F1C40F",
        "Moderate": "#E67E22",
        "Severe": "#E74C3C",
        "Unknown": "#9CA3AF"
    }

    fig = px.bar(
        distribution,
        x="Severity",
        y="Count",
        color="Severity",
        text="Count",
        color_discrete_map=color_map
    )

    fig.update_layout(
        template="plotly_white",
        showlegend=False,
        font=dict(size=18),
        height=500
    )

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    total = len(df)
    available = df["final_severity_label"].notna().sum()
    coverage = round((available / total) * 100, 2)

    colA, colB, colC = st.columns(3)

    colA.metric("Total Chronic Admissions", total)
    colB.metric("Severity Available", available)
    colC.metric("Coverage (%)", coverage)
