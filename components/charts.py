import plotly.express as px

def age_distribution(df):

    age_counts = df["age"].value_counts().sort_index()

    fig = px.bar(
        x=age_counts.index,
        y=age_counts.values,
        labels={
            "x":"Age Group",
            "y":"Patients"
        },
        title="Patient Distribution by Age Group"
    )

    fig.update_traces(
        marker_color="#1f77b4"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        showlegend=False
    )

    return fig
def gender_distribution(df):

    gender_counts = df["gender"].value_counts()

    fig = px.pie(
        values=gender_counts.values,
        names=gender_counts.index,
        hole=0.5,
        title="Patient Distribution by Gender"
    )
    fig.update_traces(
    textinfo="percent+label"
)

    fig.update_layout(
    template="plotly_dark",
    height=400,
    showlegend=False
)

    return fig

def readmission_distribution(df):

    import plotly.express as px

    readmission_counts = df["readmitted"].value_counts()

    fig = px.pie(
        values=readmission_counts.values,
        names=readmission_counts.index,
        hole=0.5,
        title="Readmission Status"
    )

    fig.update_traces(
        textinfo="percent+label"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        showlegend=False
    )

    return fig

def medical_specialty_distribution(df):

    import plotly.express as px

    specialty = (
        df["medical_specialty"]
        .fillna("Unknown")
        .value_counts()
        .head(10)
    )

    fig = px.bar(
        x=specialty.values,
        y=specialty.index,
        orientation="h",
        title="Top 10 Medical Specialties"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        xaxis_title="Number of Patients",
        yaxis_title="Medical Specialty"
    )

    return fig
def feature_importance_chart():

    import pandas as pd
    import plotly.express as px

    feature_df = pd.DataFrame({
        "Feature": [
            "Lab Procedures",
            "Medications",
            "Hospital Stay",
            "Diagnoses",
            "Procedures",
            "Inpatient Visits",
            "Outpatient Visits",
            "Emergency Visits"
        ],
        "Importance": [
            42.47,
            25.43,
            11.44,
            7.01,
            6.65,
            2.81,
            2.73,
            1.45
        ]
    })

    fig = px.bar(
        feature_df,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top Predictors of Patient Readmission"
    )

    fig.update_traces(
        marker_color="#4CAF50"
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        xaxis_title="Importance Score (%)",
        yaxis_title=""
    )

    return fig

import pandas as pd
import plotly.express as px

def admissions_forecast(df):

    admissions = (
        df.groupby("time_in_hospital")
        .size()
        .reset_index(name="Patients")
    )

    fig = px.line(
        admissions,
        x="time_in_hospital",
        y="Patients",
        markers=True,
        title="Hospital Admission Trend"
    )

    fig.update_traces(
        line_color="#00CC96",
        line_width=3
    )

    fig.update_layout(
        template="plotly_dark",
        height=400,
        xaxis_title="Hospital Stay (Days)",
        yaxis_title="Number of Patients"
    )

    return fig