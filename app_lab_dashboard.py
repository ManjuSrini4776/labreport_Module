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
# GLOBAL PROFESSIONAL STYLE (Times New Roman)
# =====================================================

st.markdown("""
<style>
html, body, [class*="css"]  {
    font-family: 'Times New Roman', serif;
}

.main-title {
    font-size: 48px;
    font-weight: bold;
    text-align: center;
}

.section-title {
    font-size: 32px;
    font-weight: bold;
    margin-top: 40px;
    margin-bottom: 15px;
}

.large-text {
    font-size: 26px;
}

.severity-box {
    padding: 40px;
    border-radius: 8px;
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    color: white;
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

st.markdown("<div class='main-title'>Chronic OPD Laboratory Severity Dashboard</div>", unsafe_allow_html=True)
st.markdown("---")

# =====================================================
# SIDEBAR PATIENT SELECTION
# =====================================================

selected_hadm = st.sidebar.selectbox(
    "Select Admission ID",
    df["hadm_id"].unique()
)

patient = df[df["hadm_id"] == selected_hadm].iloc[0]

# =====================================================
# SECTION 1 – PATIENT INFO + FINAL SEVERITY
# =====================================================

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='section-title'>Patient Information</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='large-text'><b>Subject ID:</b> {patient['subject_id']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='large-text'><b>Admission ID:</b> {patient['hadm_id']}</div>", unsafe_allow_html=True)

    diseases = []
    if patient["has_ckd"]:
        diseases.append("Chronic Kidney Disease")
    if patient["has_diabetes"]:
        diseases.append("Diabetes Mellitus")
    if patient["has_thyroid"]:
        diseases.append("Thyroid Disorder")

    st.markdown(f"<div class='large-text'><b>Chronic Conditions:</b> {', '.join(diseases)}</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='section-title'>Final Lab Severity</div>", unsafe_allow_html=True)

    severity = patient["final_severity_label"]
    score = patient["final_severity_score"]

    color_map = {
        "Stable": "#2E8B57",
        "Mild": "#FFD700",
        "Moderate": "#FF8C00",
        "Severe": "#B22222",
        "Unknown": "#708090"
    }

    box_color = color_map.get(severity, "#708090")

    st.markdown(
        f"""
        <div class='severity-box' style='background-color:{box_color};'>
            {severity} <br>
            Severity Score: {score}
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# SECTION 2 – INDIVIDUAL DISEASE SEVERITY
# =====================================================

st.markdown("<div class='section-title'>Individual Disease Severity</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("<div class='large-text'><b>CKD Severity</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='large-text'>{patient.get('ckd_severity', 'Not Available')}</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='large-text'><b>Diabetes Severity</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='large-text'>{patient.get('diabetes_severity_final', 'Not Available')}</div>", unsafe_allow_html=True)

with c3:
    st.markdown("<div class='large-text'><b>Thyroid Severity</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='large-text'>{patient.get('thyroid_severity_final', 'Not Available')}</div>", unsafe_allow_html=True)

# =====================================================
# SECTION 3 – COHORT DISTRIBUTION (MULTICOLOR)
# =====================================================

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

# =====================================================
# SECTION 4 – DATA SUMMARY
# =====================================================

st.markdown("<div class='section-title'>Data Summary</div>", unsafe_allow_html=True)

total = len(df)
available = df["final_severity_label"].notna().sum()
coverage = round((available / total) * 100, 2)

colA, colB, colC = st.columns(3)

colA.markdown(f"<div class='large-text'><b>Total Chronic Admissions:</b> {total}</div>", unsafe_allow_html=True)
colB.markdown(f"<div class='large-text'><b>Severity Available:</b> {available}</div>", unsafe_allow_html=True)
colC.markdown(f"<div class='large-text'><b>Coverage:</b> {coverage}%</div>", unsafe_allow_html=True)
