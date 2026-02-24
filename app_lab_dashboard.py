import streamlit as st
import pandas as pd

# ============================================
# Page Config
# ============================================

st.set_page_config(
    page_title="Lab Severity Dashboard",
    layout="wide"
)

st.title("🧪 Lab Severity Dashboard (Chronic OPD Cohort)")

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

st.sidebar.header("Patient Selection")

hadm_list = df['hadm_id'].unique()

selected_hadm = st.sidebar.selectbox(
    "Select Admission ID",
    hadm_list
)

patient = df[df['hadm_id'] == selected_hadm].iloc[0]

# ============================================
# Patient Details Section
# ============================================

st.subheader("Patient Details")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Subject ID", patient['subject_id'])

with col2:
    st.metric("Severity Score", patient['final_severity_score'])

with col3:
    st.metric("Final Lab Severity", patient['final_severity_label'])

# ============================================
# Severity Indicator
# ============================================

severity = patient['final_severity_label']

st.subheader("Severity Indicator")

if severity == "Stable":
    st.success("🟢 Stable - No major lab abnormality detected")
elif severity == "Mild":
    st.info("🟡 Mild - Minor lab deviation")
elif severity == "Moderate":
    st.warning("🟠 Moderate - Clinical attention recommended")
elif severity == "Severe":
    st.error("🔴 Severe - Immediate review recommended")
else:
    st.write("⚪ Unknown - No biomarker available")

# ============================================
# Cohort-Level Distribution
# ============================================

st.subheader("Cohort Severity Distribution")

distribution = df['final_severity_label'].value_counts()

st.bar_chart(distribution)

# ============================================
# Doctor Workflow Simulation
# ============================================

st.subheader("Doctor Action")

approve = st.button("Approve & Send Lab Summary")

if approve:
    st.success("Lab summary approved and ready for patient communication.")

if severity == "Severe":
    st.warning("⚠ Automatic appointment scheduling recommended.")
