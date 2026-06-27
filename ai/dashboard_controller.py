import re


def get_filters(question):

    question = question.lower()

    filters = {}

    # =====================================
    # Question Type
    # =====================================

    analysis_keywords = [
        "why",
        "explain",
        "recommend",
        "summary",
        "summarize",
        "insight",
        "analysis",
        "risk",
        "suggest"
    ]

    filters["type"] = "filter"

    for word in analysis_keywords:
        if word in question:
            filters["type"] = "analysis"
            return filters

    # =====================================
    # Gender
    # =====================================

    if "female" in question:
        filters["gender"] = "Female"

    elif "male" in question:
        filters["gender"] = "Male"

    # =====================================
    # Age
    # =====================================

    age_match = re.search(r"above\s+(\d+)", question)

    if age_match:
        filters["age_min"] = int(age_match.group(1))

    age_match = re.search(r"below\s+(\d+)", question)

    if age_match:
        filters["age_max"] = int(age_match.group(1))

    # =====================================
    # Readmission
    # =====================================

    if "readmitted" in question:

        filters["readmitted"] = True

    # =====================================
    # High Risk
    # =====================================

    if "high risk" in question:

        filters["high_risk"] = True

    return filters