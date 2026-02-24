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
# CUSTOM STYLING (Professional Clinical Theme)
# ==========================================================

st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 10px;
}
.section-title {
    font-size: 24px;
    font-weight: 600;
    margin-top: 25px;
    margin-bottom: 15px;
}
.info-box {
    padding: 18px;
    border-radius: 10px;
    background-color: #111827;
    border: 1px solid #374151;
}
.metric-card {
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    font-size: 22px;
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
# SIDEBAR – PATIENT SELECTION
# ==========================================================

st.sidebar.title("Patient Selection")

selected_hadm = st.sidebar.selectbox(
    "Admission ID",
    df["hadm_id"].unique()
)

patient = df[df["hadm_id"] == selected_hadm].iloc[0]

# ==========================================================
# MAIN TITLE
# ==========================================================

st.markdown("<div class='main-title'>Chronic OPD Lab Severity Dashboard</div>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================================
# SECTION 1 – PATIENT PROFILE
# ==========================================================

st.markdown("<div class='section-title'>Patient Profile</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.write(f"**Subject ID:** {patient['subject_id']}")
    st.write(f"**Admission ID:** {patient['hadm_id']}")

    diseases = []
    if patient["has_ckd"]:
        diseases.append("CKD")
    if patient["has_diabetes"]:
        diseases.append("Diabetes")
    if patient["has_thyroid"]:
        diseases.append("Thyroid")

    if diseases:
        st.write("**Chronic Conditions:**")
        st.write(" | ".join(diseases))
    else:
        st.write("No chronic disease identified")

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    severity = patient["final_severity_label"]
    score = patient["final_severity_score"]

    color_map = {
        "Stable": "#2ECC71",
        "Mild": "#F1C40F",
        "Moderate": "#E67E22",
        "Severe": "#E74C3C",
        "Unknown": "#6B7280"
    }

    box_color = color_map.get(severity, "#6B7280")

    st.markdown(
        f"""
        <div class='metric-card' style='background-color:{box_color}; color:white;'>
            {severity} <br>
            Severity Score: {score}
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================================
# SECTION 2 – INDIVIDUAL DISEASE SEVERITY
# ==========================================================

st.markdown("<div class='section-title'>Individual Disease Severity</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.write("**CKD Severity**")
    st.write(patient.get("ckd_severity", "N/A"))
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.write("**Diabetes Severity**")
    st.write(patient.get("diabetes_severity_final", "N/A"))
    st.markdown("</div>", unsafe_allow_html=True)

with c3:
    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
    st.write("**Thyroid Severity**")
    st.write(patient.get("thyroid_severity_final", "N/A"))
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================================
# SECTION 3 – COHORT DISTRIBUTION (MULTICOLOR)
# ==========================================================

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
    "Unknown": "#6B7280"
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
    template="plotly_dark",
    showlegend=False,
    xaxis_title="Severity Level",
    yaxis_title="Number of Admissions",
    font=dict(size=14)
)

fig.update_traces(textposition="outside")

st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# SECTION 4 – DATA COVERAGE SUMMARY
# ==========================================================

st.markdown("<div class='section-title'>Data Coverage Summary</div>", unsafe_allow_html=True)

total = len(df)
available = df["final_severity_label"].notna().sum()
coverage = round((available / total) * 100, 2)

colA, colB, colC = st.columns(3)

colA.metric("Total Chronic Admissions", total)
colB.metric("Severity Available", available)
colC.metric("Coverage (%)", coverage)
