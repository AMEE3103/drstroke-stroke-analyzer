import pandas as pd

INPUT_CSV = "healthcare-dataset-stroke-data.csv"
OUTPUT_CSV = "healthcare-dataset-stroke-data_processed.csv"


def calculate_stroke_risk(row):
    score = 0
    drivers = []

    if row["age"] >= 60:
        score += 3
        drivers.append("Age ≥ 60")

    if row["hypertension"] == 1:
        score += 3
        drivers.append("Hypertension")

    if row["heart_disease"] == 1:
        score += 4
        drivers.append("Heart Disease")

    if row["avg_glucose_level"] > 160:
        score += 3
        drivers.append("High Glucose")

    if row["bmi"] > 25:
        score += 1
        drivers.append("High BMI")

    if row["smoking_status"] in ["formerly smoked", "smokes"]:
        score += 2
        drivers.append("Smoking History")

    if score <= 2:
        tier = "Low"
    elif score <= 5:
        tier = "Elevated"
    elif score <= 8:
        tier = "High"
    else:
        tier = "Critical"

    return score, tier, ", ".join(drivers)


def update_csv_with_risk():
    df = pd.read_csv(INPUT_CSV)

    df[["risk_score", "risk_tier", "risk_drivers"]] = df.apply(
        lambda row: pd.Series(calculate_stroke_risk(row)), axis=1
    )

    # WRITE TO NEW FILE (SAFE)
    df.to_csv(OUTPUT_CSV, index=False)

    return df
