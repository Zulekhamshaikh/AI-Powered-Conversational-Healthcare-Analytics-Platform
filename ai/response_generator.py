def generate_response(filtered_df):

    total_patients = len(filtered_df)

    female_patients = (
        filtered_df["gender"] == "Female"
    ).sum()

    male_patients = (
        filtered_df["gender"] == "Male"
    ).sum()

    avg_stay = (
        filtered_df["time_in_hospital"]
        .mean()
    )

    avg_medications = (
        filtered_df["num_medications"]
        .mean()
    )

    readmission_rate = (
        (filtered_df["readmitted"] != "NO")
        .mean() * 100
    )

    highest_specialty = (
        filtered_df["medical_specialty"]
        .fillna("Unknown")
        .value_counts()
        .idxmax()
    )

    common_readmission = (
        filtered_df["readmitted"]
        .value_counts()
        .idxmax()
    )

    response = f"""
## 📊 Analysis Results

👥 Total Patients : {total_patients:,}

👩 Female Patients : {female_patients:,}

👨 Male Patients : {male_patients:,}

🏥 Average Stay : {avg_stay:.2f} Days

💊 Average Medications : {avg_medications:.2f}

📈 Readmission Rate : {readmission_rate:.2f}%

🩺 Highest Specialty : {highest_specialty}

📋 Most Common Readmission : {common_readmission}

✅ Dashboard updated successfully.
"""

    return response