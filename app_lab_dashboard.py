import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Chronic OPD Lab Severity",
    layout="wide"
)

# =====================================================
# PROFESSIONAL FONT (Times New Roman)
# =====================================================

st.markdown("""
<style>
html, body, [class*="css"]  {
    font-family: 'Times New Roman', serif;
}
.main-title {
    font-size: 46px;
    font-weight: bold;
}
.section-title {
    font-size: 32px;
    font-weight: bold;
    margin-top: 25px;
}
.big-text {
    font-size: 26px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    return pd.read_parquet("NB06_MULTIMODAL_SEVERITY_FUSION.parquet")

df = load_data()

# =====================================================
# HEADER
# =====================================================

st.markdown("<div class='main-title'>Chronic OPD Laboratory Severity Analysis</div>", unsafe_allow_html=True)
st.markdown("---")

# =====================================================
# SIDEBAR SELECTION
# =====================================================

selected_hadm = st.sidebar.selectbox(
    "Select Admission ID",
    df["hadm_id"].unique()
)

patient = df[df["hadm_id"] == selected_hadm].iloc[0]

# =====================================================
# TABS (NO LONG SCROLL)
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "Patient Summary",
    "Disease-Specific Severity",
    "Cohort Distribution"
])

# =====================================================
# TAB 1 – PATIENT SUMMARY
# =====================================================

with tab1:

    st.markdown("<div class='section-title'>Patient Information</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<div class='big-text'><b>Subject ID:</b> {patient['subject_id']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='big-text'><b>Admission ID:</b> {patient['hadm_id']}</div>", unsafe_allow_html=True)

        diseases = []
        if patient["has_ckd"]:
            diseases.append("Chronic Kidney Disease")
        if patient["has_diabetes"]:
            diseases.append("Diabetes Mellitus")
        if patient["has_thyroid"]:
            diseases.append("Thyroid Disorder")

        st.markdown(f"<div class='big-text'><b>Chronic Conditions:</b> {', '.join(diseases)}</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-title'>Final Lab Severity</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='big-text'><b>Severity Label:</b> {patient['final_severity_label']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='big-text'><b>Severity Score:</b> {patient['final_severity_score']}</div>", unsafe_allow_html=True)

# =====================================================
# TAB 2 – DISEASE BREAKDOWN
# =====================================================

with tab2:

    st.markdown("<div class='section-title'>Individual Disease Severity</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='big-text'><b>CKD Severity</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='big-text'>{patient.get('ckd_severity', 'Not Available')}</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='big-text'><b>Diabetes Severity</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='big-text'>{patient.get('diabetes_severity_final', 'Not Available')}</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='big-text'><b>Thyroid Severity</b></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='big-text'>{patient.get('thyroid_severity_final', 'Not Available')}</div>", unsafe_allow_html=True)

# =====================================================
# TAB 3 – COHORT DISTRIBUTION
# =====================================================

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
        "Stable": "#2E8B57",
        "Mild": "#FFD700",
        "Moderate": "#FF8C00",
        "Severe": "#B22222",
        "Unknown": "#708090"
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
        template="simple_white",
        showlegend=False,
        font=dict(size=20),
        height=550
    )

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    total = len(df)
    available = df["final_severity_label"].notna().sum()
    coverage = round((available / total) * 100, 2)

    st.markdown(f"<div class='big-text'><b>Total Chronic Admissions:</b> {total}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-text'><b>Severity Available:</b> {available}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-text'><b>Coverage:</b> {coverage}%</div>", unsafe_allow_html=True)
