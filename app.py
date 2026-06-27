import streamlit as st
from datetime import datetime

from utils.load_data import load_data

from components.charts import (
    age_distribution,
    gender_distribution,
    medical_specialty_distribution,
    readmission_distribution,
    feature_importance_chart,
    admissions_forecast
)

from ai.dashboard_controller import get_filters
from ai.gemini import ask_gemini
from ai.insights import generate_insights
from ai.response_generator import generate_response
from streamlit_mic_recorder import speech_to_text


# ===========================================================
# PAGE CONFIG
# ===========================================================

st.set_page_config(
    page_title="AI Healthcare Analytics Platform",
    page_icon="🏥",
    layout="wide"
)


# ===========================================================
# SESSION STATE
# ===========================================================

session_defaults = {
    "filters": {},
    "ai_response": "",
    "chat_history": [],
    "recommendation": "",
    "dashboard_action": "",
    "voice_trigger": False,
    "voice_question": "",
    "last_question": ""
}

for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ===========================================================
# LOAD DATA
# ===========================================================

df = load_data()

filtered_df = df.copy()

filters = st.session_state.filters


# ===========================================================
# AGE MAP
# ===========================================================

age_map = {
    "[0-10)":5,
    "[10-20)":15,
    "[20-30)":25,
    "[30-40)":35,
    "[40-50)":45,
    "[50-60)":55,
    "[60-70)":65,
    "[70-80)":75,
    "[80-90)":85,
    "[90-100)":95
}


# ===========================================================
# APPLY FILTERS
# ===========================================================

if "gender" in filters:

    filtered_df = filtered_df[
        filtered_df["gender"] == filters["gender"]
    ]


if "age_min" in filters:

    filtered_df = filtered_df[
        filtered_df["age"].map(age_map) >= filters["age_min"]
    ]


if "age_max" in filters:

    filtered_df = filtered_df[
        filtered_df["age"].map(age_map) <= filters["age_max"]
    ]


# ===========================================================
# KPI CALCULATIONS
# ===========================================================

total_patients = len(filtered_df)

readmission_rate = (
    (filtered_df["readmitted"] != "NO").mean()
    * 100
)

avg_stay = filtered_df["time_in_hospital"].mean()

avg_medications = filtered_df["num_medications"].mean()

female_patients = (
    filtered_df["gender"] == "Female"
).sum()

male_patients = (
    filtered_df["gender"] == "Male"
).sum()


# Highest Specialty

specialty_counts = (
    filtered_df["medical_specialty"]
    .replace("?", None)
    .dropna()
)

if len(specialty_counts) > 0:
    highest_specialty = (
        specialty_counts
        .value_counts()
        .idxmax()
    )
else:
    highest_specialty = "Unknown"


# Most Common Readmission

common_readmission = (
    filtered_df["readmitted"]
    .value_counts()
    .idxmax()
)


# ===========================================================
# DASHBOARD SUMMARY
# ===========================================================

dashboard_summary = f"""
Total Patients : {total_patients:,}

Female Patients : {female_patients:,}

Male Patients : {male_patients:,}

Readmission Rate : {readmission_rate:.2f}%

Average Stay : {avg_stay:.2f} Days

Average Medications : {avg_medications:.2f}

Highest Specialty : {highest_specialty}

Most Common Readmission : {common_readmission}
"""


# ===========================================================
# AI INSIGHTS
# ===========================================================

insights = generate_insights(filtered_df)


# ===========================================================
# DETERMINE QUERY TYPE
# ===========================================================

question = st.session_state.last_question

query_type = filters.get("type", "filter")



# ===========================================================
# HEADER
# ===========================================================

st.title("🏥 AI Healthcare Analytics Platform")

st.markdown(
    """
Real-Time Patient Readmission Risk Analysis and AI-Powered Healthcare Insights
"""
)

st.divider()


# ===========================================================
# KPI CARDS
# ===========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "👥 Total Patients",
        f"{total_patients:,}"
    )

with col2:

    st.metric(
        "📈 Readmission Rate",
        f"{readmission_rate:.2f}%"
    )

with col3:

    st.metric(
        "🏥 Average Stay",
        f"{avg_stay:.2f} Days"
    )

with col4:

    st.metric(
        "💊 Avg Medications",
        f"{avg_medications:.2f}"
    )


st.divider()


# ===========================================================
# MAIN DASHBOARD
# ===========================================================

dashboard_col, ai_col = st.columns([2.5, 1])


# ===========================================================
# LEFT PANEL (Charts)
# ===========================================================

with dashboard_col:

    st.subheader("📊 Healthcare Dashboard")

    st.plotly_chart(
        age_distribution(filtered_df),
        use_container_width=True
    )

    st.plotly_chart(
        gender_distribution(filtered_df),
        use_container_width=True
    )

    st.plotly_chart(
        medical_specialty_distribution(filtered_df),
        use_container_width=True
    )

    st.plotly_chart(
        readmission_distribution(filtered_df),
        use_container_width=True
    )

    st.plotly_chart(
        feature_importance_chart(),
        use_container_width=True
    )

    st.plotly_chart(
        admissions_forecast(filtered_df),
        use_container_width=True
    )


# ===========================================================
# RIGHT PANEL (AI)
# ===========================================================

with ai_col:

    st.subheader("🤖 AI Healthcare Assistant")

    question = st.text_input(
        "Ask a healthcare question",
        placeholder="Example: Show female patients above 70"
    )


    # ==========================================
    # Voice Assistant
    # ==========================================

    st.markdown("### 🎤 Voice Assistant")

    voice_text = speech_to_text(
        language="en",
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        just_once=True,
        use_container_width=True,
        key="voice_input"
    )

    if voice_text:

        st.success(f"You said: {voice_text}")

        question = voice_text

        st.session_state.voice_question = voice_text

        st.session_state.voice_trigger = True


    # ==========================================
    # Buttons
    # ==========================================

    btn1, btn2 = st.columns(2)

    with btn1:

        analyze = st.button(
            "🔍 Analyze",
            use_container_width=True
        )

    with btn2:

        clear = st.button(
            "🗑 Clear",
            use_container_width=True
        )


    if clear:

        st.session_state.filters = {}

        st.session_state.ai_response = ""

        st.session_state.chat_history = []

        st.session_state.recommendation = ""

        st.session_state.dashboard_action = ""

        st.session_state.voice_trigger = False

        st.session_state.voice_question = ""

        st.session_state.last_question = ""

        st.rerun()


    # ==========================================
    # Dashboard Summary
    # ==========================================

    st.divider()

    st.markdown("### 📊 Dashboard Summary")

    st.info(dashboard_summary)


    # ==========================================
    # AI Insights
    # ==========================================

    st.divider()

    st.markdown("### 🧠 AI Insights")

    st.success(f"""
    👥 Total Patients: {insights["Total Patients"]:,}

    👩 Female Patients: {insights["Female Patients"]:,}

    🏥 Average Stay: {insights["Average Stay"]:.2f} Days

    📈 Readmission Rate: {insights["Readmission Rate"]:.2f}%%

    🩺 Highest Specialty: {insights["Highest Specialty"]}

    📋 Most Common Readmission: {insights["Most Common Readmission"]}

    🚨 High Risk Patients: {insights["High Risk Patients"]:,}

    🎯 Risk Level: {insights["Risk Level"]}
    """)

    # ===========================================================
    # AI RESPONSE
    # ===========================================================

    st.divider()

    st.markdown("### 💡 AI Response")

    response_box = st.empty()

    if st.session_state.ai_response != "":

        response_box.success(
            st.session_state.ai_response
        )

    else:

        response_box.info(
            "Ask a healthcare question and click Analyze."
        )


    # ===========================================================
    # CHAT HISTORY
    # ===========================================================

    st.divider()

    st.markdown("### 💬 Chat History")

    if len(st.session_state.chat_history) == 0:

        st.info("No conversation yet.")

    else:

        for chat in reversed(st.session_state.chat_history):

         st.markdown(
            f"**👤 You:** {chat['question']}"
            )

        st.success(chat["answer"])

        st.divider()


    # ===========================================================
    # RECOMMENDATIONS
    # ===========================================================

    st.divider()

    st.markdown("### 📋 Recommendations")

    if st.session_state.recommendation != "":

        st.success(
        st.session_state.recommendation
    )

    else:

        st.info(
        "Recommendations will appear here."
    )


    # ===========================================================
    # DASHBOARD ACTIONS
    # ===========================================================

    st.divider()

    st.markdown("### ⚡ Dashboard Actions")

    if st.session_state.dashboard_action != "":

        st.success(
        st.session_state.dashboard_action
    )

    else:

        st.info(
        "No dashboard actions yet."
    )


    # ===========================================================
    # SUGGESTED QUESTIONS
    # ===========================================================

    st.divider()

    st.markdown("### 💬 Suggested Questions")

    if st.button("Highest Readmission"):

        question = "Which age group has highest readmission?"

    if st.button("High Risk Patients"):

     question = "Show high risk patients"

    if st.button("Dashboard Summary"):

     question = "Summarize dashboard"

    if st.button("Top Risk Factors"):

        question = "What are the top risk factors?"


# ===========================================================
# ANALYZE BUTTON
# ===========================================================

if analyze or st.session_state.voice_trigger:

    # -----------------------------
    # Voice Assistant
    # -----------------------------

    if st.session_state.voice_trigger:

        question = st.session_state.voice_question

        st.session_state.voice_trigger = False

    # Save question

    st.session_state.last_question = question

    # Extract filters

    filters = get_filters(question)

    # Save filters

    st.session_state.filters = filters

    query_type = filters.get("type", "filter")

    # -----------------------------
    # FILTER QUESTIONS
    # -----------------------------

    if query_type == "filter":

        answer = generate_response(filtered_df)

    # -----------------------------
    # ANALYSIS QUESTIONS
    # -----------------------------

    else:

        answer = ask_gemini(
            question,
            dashboard_summary
        )

    # -----------------------------
    # Save AI Response
    # -----------------------------

    st.session_state.ai_response = answer

    # -----------------------------
    # Chat History
    # -----------------------------

    st.session_state.chat_history.append(
        {
            "question": question,
            "answer": answer
        }
    )

    # -----------------------------
    # Recommendations
    # -----------------------------

    st.session_state.recommendation = f"""
✓ Monitor elderly patients regularly

✓ Increase follow-up visits

✓ Review medication plans

✓ Prioritize high-risk patients

Current Records : {total_patients:,}
"""

    # -----------------------------
    # Dashboard Actions
    # -----------------------------

    st.session_state.dashboard_action = f"""
✔ Dashboard Updated

✔ Filters Applied

✔ KPI Cards Updated

✔ Charts Refreshed

✔ Patient Table Updated

Records Displayed : {total_patients:,}
"""

    st.rerun()

# ===========================================================
# GENERATE RESPONSE AFTER FILTERS ARE APPLIED
# ===========================================================

if st.session_state.last_question != "":

    current_filters = st.session_state.filters

    query_type = current_filters.get("type", "filter")

    # Generate response AFTER filtered_df has been created

    if query_type == "filter":

        answer = generate_response(filtered_df)

    else:

        answer = ask_gemini(
            st.session_state.last_question,
            dashboard_summary
        )

    # Save latest response

    st.session_state.ai_response = answer

    # Update chat history only if this question is new

    if (
        len(st.session_state.chat_history) == 0
        or
        st.session_state.chat_history[-1]["question"]
        != st.session_state.last_question
    ):

        st.session_state.chat_history.append(
            {
                "question": st.session_state.last_question,
                "answer": answer
            }
        )

    # Dynamic Recommendations

    st.session_state.recommendation = f"""
✓ Review elderly patients regularly

✓ Increase follow-up visits

✓ Monitor medication adherence

✓ Highest Specialty : {highest_specialty}

✓ Current Readmission Rate : {readmission_rate:.2f}%
"""

    # Dynamic Dashboard Actions

    st.session_state.dashboard_action = f"""
✔ Dashboard Updated Successfully

✔ Filters Applied

✔ Total Patients : {total_patients:,}

✔ Charts Updated

✔ Patient Table Updated
"""


# ===========================================================
# PATIENT RECORDS
# ===========================================================

st.divider()

st.subheader("📋 Patient Records")

st.dataframe(
    filtered_df[
        [
            "patient_nbr",
            "gender",
            "age",
            "medical_specialty",
            "time_in_hospital",
            "num_medications",
            "readmitted"
        ]
    ],
    use_container_width=True,
    hide_index=True
)


# ===========================================================
# EXPORT FILTERED DATA
# ===========================================================

st.divider()

st.subheader("📥 Export Filtered Data")

current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.info(f"""
📄 Report Summary

• Total Records : {len(filtered_df):,}

• Readmission Rate : {readmission_rate:.2f}%

• Average Stay : {avg_stay:.2f} Days

• Generated : {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}
""")

st.download_button(
    label="⬇ Download Filtered Patients",
    data=csv,
    file_name=f"Healthcare_Report_{current_time}.csv",
    mime="text/csv",
    use_container_width=True
)


# ===========================================================
# FOOTER
# ===========================================================

st.divider()

st.caption(
    "🏥 AI Healthcare Analytics Platform | Built with Streamlit, Plotly & Google Gemini"
)