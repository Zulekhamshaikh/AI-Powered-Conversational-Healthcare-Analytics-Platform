def generate_insights(df):

    total_patients = len(df)

    female_patients = len(
        df[df["gender"] == "Female"]
    )

    avg_stay = round(
        df["time_in_hospital"].mean(),
        2
    )

    readmission_rate = round(
        (df["readmitted"] != "NO").mean() * 100,
        2
    )

    highest_specialty = (
        df["medical_specialty"]
        .fillna("Unknown")
        .value_counts()
        .idxmax()
    )

    common_readmission = (
        df["readmitted"]
        .value_counts()
        .idxmax()
    )

    # ----------------------------
    # High Risk Patients
    # ----------------------------

    high_risk = df[
        (df["time_in_hospital"] >= 7) &
        (df["num_medications"] >= 15)
    ]

    high_risk_count = len(high_risk)

    # ----------------------------
    # Risk Level
    # ----------------------------

    if readmission_rate >= 50:
        risk_level = "🔴 High"

    elif readmission_rate >= 35:
        risk_level = "🟠 Medium"

    else:
        risk_level = "🟢 Low"

    return {

        "Total Patients": total_patients,

        "Female Patients": female_patients,

        "Average Stay": avg_stay,

        "Readmission Rate": readmission_rate,

        "Highest Specialty": highest_specialty,

        "Most Common Readmission": common_readmission,

        "High Risk Patients": high_risk_count,

        "Risk Level": risk_level
    }