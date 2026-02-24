import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_parquet("NB06_MULTIMODAL_SEVERITY_FUSION.parquet")

df = load_data()

st.title("🧪 Lab Severity Dashboard (Chronic OPD)")

hadm_list = df['hadm_id'].unique()
selected_hadm = st.selectbox("Select Admission ID", hadm_list)

patient = df[df['hadm_id'] == selected_hadm].iloc[0]

st.subheader("Patient Details")
st.write(f"Subject ID: {patient['subject_id']}")
st.write(f"Final Lab Severity: {patient['lab_severity_label']}")
st.write(f"Severity Score: {patient['lab_severity_score']}")

severity = patient['lab_severity_label']

if severity == "Stable":
    st.success("🟢 Stable")
elif severity == "Mild":
    st.info("🟡 Mild")
elif severity == "Moderate":
    st.warning("🟠 Moderate")
elif severity == "Severe":
    st.error("🔴 Severe")
else:
    st.write("⚪ Unknown")

st.subheader("Cohort Distribution")
st.bar_chart(df['lab_severity_label'].value_counts())

if st.button("Approve & Send Summary"):
    st.success("Lab summary approved.")

if severity == "Severe":
    st.warning("Automatic appointment scheduling recommended.")
