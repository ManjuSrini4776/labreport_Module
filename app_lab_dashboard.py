import streamlit as st
import pandas as pd

# ============================================
# Page Config
# ============================================

st.set_page_config(
    page_title="Lab Severity Module",
    layout="wide"
)

# ============================================
# Load Data
# ============================================

@st.cache_data
def load_data():
    return pd.read_parquet("NB06_MULTIMODAL_SEVERITY_FUSION.parquet")

df = load_data()

# ============================================
# Sidebar - Patient Selection
# ============================================

st.sidebar.title("🔎 Select Patient Admission")

hadm_list = df['hadm_id'].unique()

selected_hadm = st.sidebar.selectbox(
    "Admission ID",
    hadm_list
)

patient = df[df['hadm_id'] == selected_hadm].iloc[0]

# ============================================
# Title
# ============================================

st.markdown(
    "<h1 style='text-align: center; color: #2C3E50;'>Chronic OPD Lab Severity Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown("---")

# ============================================
# Top Patient Summary Section
# ============================================

col1, col2 = st.columns([1,2])

with col1:
    st.markdown("### 🧾 Patient Information")
    st.markdown(f"**Subject ID:** {patient['subject_id']}")
    st.markdown(f"**Admission ID:** {patient['hadm_id']}")

    # Disease Badges
    diseases = []
    if patient['has_ckd']:
        diseases.append("🩺 CKD")
    if patient['has_diabetes']:
        diseases.append("🩸 Diabetes")
    if patient['has_thyroid']:
        diseases.append("🧬 Thyroid")

    if diseases:
        st.markdown("**Chronic Conditions:**")
        st.markdown(" | ".join(diseases))
    else:
        st.markdown("No chronic disease recorded.")

with col2:
    st.markdown("### 📊 Severity Summary")

    severity = patient['final_severity_label']
    score = patient['final_severity_score']

    if severity == "Stable":
        color = "#2ECC71"
    elif severity == "Mild":
        color = "#F1C40F"
    elif severity == "Moderate":
        color = "#E67E22"
    elif severity == "Severe":
        color = "#E74C3C"
    else:
        color = "#95A5A6"

    st.markdown(
        f"""
        <div style="
            padding: 30px;
            border-radius: 12px;
            background-color: {color};
            color: white;
            text-align: center;
            font-size: 28px;
            font-weight: bold;">
            {severity} (Score: {score})
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# ============================================
# Individual Disease Severity
# ============================================

st.markdown("## 🧪 Individual Disease Severity")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### CKD")
    st.info(str(patient.get('ckd_severity', 'N/A')))

with col2:
    st.markdown("### Diabetes")
    st.info(str(patient.get('diabetes_severity_final', 'N/A')))

with col3:
    st.markdown("### Thyroid")
    st.info(str(patient.get('thyroid_severity_final', 'N/A')))

st.markdown("---")

# ============================================
# Cohort Distribution
# ============================================

st.markdown("## 📈 Cohort Severity Distribution")

order = ["Stable", "Mild", "Moderate", "Severe", "Unknown"]

distribution = df['final_severity_label'].value_counts().reindex(order)

st.bar_chart(distribution)
