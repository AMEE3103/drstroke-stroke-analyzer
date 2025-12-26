import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from risk_engine import update_csv_with_risk
from ml_model import train_model
from pdf_report import generate_pdf


# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="DrStroke",
    page_icon="🧠",
    layout="wide"
)

# ================= HEADER =================
st.title("🧠 DrStroke")
st.subheader("Stroke Risk Analysis & Patient Guidance System")
st.divider()


# ================= RISK COLOR LOGIC =================
def risk_color(tier):
    if tier == "Low":
        return "#2ecc71"   # Green (Safe)
    elif tier == "Elevated":
        return "#f1c40f"   # Yellow (Caution)
    elif tier == "High":
        return "#e67e22"   # Orange (Danger)
    else:
        return "#e74c3c"   # Red (Critical)


# ================= RISK CRITERIA =================
def risk_criteria_explanation():
    return [
        "Age ≥ 60 years increases stroke risk",
        "Hypertension (high blood pressure) damages blood vessels",
        "Heart disease increases embolic stroke risk",
        "Average glucose level > 160 mg/dL indicates metabolic risk",
        "BMI > 25 indicates overweight/obesity-related risk",
        "Smoking history causes long-term vascular damage"
    ]


# ================= RECOVERY GUIDANCE =================
def recovery_guidance(risk_tier):
    data = {
        "Low": {
            "precautions": ["Maintain physical activity", "Annual BP check"],
            "diet": ["Balanced meals", "Adequate hydration"],
            "sleep": "7–8 hours daily"
        },
        "Elevated": {
            "precautions": ["Monitor BP regularly", "Control body weight"],
            "diet": ["Low salt and sugar diet", "Increase vegetables"],
            "sleep": "7–8 hours, sleep before 11 PM"
        },
        "High": {
            "precautions": ["Frequent BP & glucose checks", "Avoid heavy exertion"],
            "diet": ["Low sodium foods", "Avoid sugary drinks"],
            "sleep": "At least 8 hours"
        },
        "Critical": {
            "precautions": ["Immediate medical supervision"],
            "diet": ["Doctor-recommended diet only"],
            "sleep": "8–9 hours with strict routine"
        }
    }
    return data.get(risk_tier)


# ================= SAFE LOAD =================
@st.cache_data(show_spinner=True)
def load_data():
    return update_csv_with_risk()

@st.cache_resource(show_spinner=True)
def load_model():
    return train_model("healthcare-dataset-stroke-data_processed.csv")


df = load_data()
model, accuracy = load_model()


# ================= PATIENT SEARCH =================
st.sidebar.title("🔍 Patient Search")
patient_id_input = st.sidebar.text_input("Enter Patient ID (numeric)")


# ================= MAIN VIEW =================
if patient_id_input:
    try:
        patient_id = int(patient_id_input)
        patient = df[df["id"] == patient_id]

        if patient.empty:
            st.error("❌ Patient ID not found")
        else:
            # Extract values
            tier = patient["risk_tier"].values[0]
            score = patient["risk_score"].values[0]
            color = risk_color(tier)
            guide = recovery_guidance(tier)

            # ================= RISK DISPLAY =================
            st.markdown(
                f"""
                <div style="
                    padding:22px;
                    background-color:{color};
                    border-radius:12px;
                    text-align:center;
                    color:black;">
                    <h2>⚠️ Stroke Risk Level</h2>
                    <h1 style="font-size:54px;">{tier}</h1>
                    <h3>Risk Score: {score}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.divider()

            # ================= PATIENT DETAILS =================
            st.subheader("🧍 Patient Clinical Overview")

            c1, c2 = st.columns(2)

            with c1:
                st.markdown(
                    f"""
                    **Patient ID:** {patient_id}  
                    **Gender:** {patient["gender"].values[0]}  
                    **Age:** {patient["age"].values[0]}  
                    """
                )

            with c2:
                st.markdown(
                    f"""
                    **Hypertension:** {patient["hypertension"].values[0]}  
                    **Heart Disease:** {patient["heart_disease"].values[0]}  
                    **Avg Glucose:** {patient["avg_glucose_level"].values[0]}  
                    **BMI:** {patient["bmi"].values[0]}  
                    """
                )

            st.divider()

            # ================= RISK CRITERIA =================
            st.subheader("📌 Stroke Risk Classification Criteria")
            for c in risk_criteria_explanation():
                st.write("•", c)

            st.caption(
                "Risk tier is computed using a weighted clinical scoring model "
                "based on the above factors."
            )

            # ================= PATIENT-SPECIFIC DRIVERS =================
            st.subheader("🔍 Key Risk Drivers for This Patient")
            drivers = patient["risk_drivers"].values[0]

            if drivers:
                for d in drivers.split(","):
                    st.write("•", d.strip())
            else:
                st.write("No significant risk drivers detected.")

            st.divider()

            # ================= GUIDANCE =================
            st.subheader("🛡️ Recovery & Prevention Guidance")

            g1, g2, g3 = st.columns(3)

            with g1:
                st.markdown("### ⚠️ Precautions")
                for p in guide["precautions"]:
                    st.write("•", p)

            with g2:
                st.markdown("### 🥗 Diet")
                for d in guide["diet"]:
                    st.write("•", d)

            with g3:
                st.markdown("### 😴 Sleep")
                st.write(guide["sleep"])

            st.divider()

            if st.button("📄 Generate PDF Report"):
                pdf = generate_pdf(patient)
                st.success(f"PDF generated: `{pdf}`")

    except ValueError:
        st.error("❌ Please enter a valid numeric Patient ID")


# ================= ANALYTICS =================
with st.expander("📊 Dataset Analytics"):
    colA, colB = st.columns(2)

    with colA:
        fig, ax = plt.subplots()
        df["risk_tier"].value_counts().plot(kind="bar", ax=ax)
        ax.set_title("Risk Tier Distribution")
        st.pyplot(fig)

    with colB:
        fig, ax = plt.subplots()
        ax.scatter(df["age"], df["stroke"], alpha=0.5)
        ax.set_xlabel("Age")
        ax.set_ylabel("Stroke")
        st.pyplot(fig)


# ================= FOOTER =================
st.divider()
st.caption("DrStroke © Educational Project | Not a Medical Diagnostic System")
