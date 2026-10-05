import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Incident Response",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD CSS
# =========================================================

css_path = Path(__file__).parent / "style.css"

with open(css_path, "r", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )


# =========================================================
# SESSION STATE
# =========================================================

if "selected_module" not in st.session_state:
    st.session_state.selected_module = "Dashboard"

if "incidents" not in st.session_state:
    st.session_state.incidents = []

if "analysis" not in st.session_state:
    st.session_state.analysis = None


# =========================================================
# MODULES
# =========================================================

modules = {

    "Dashboard": {
        "icon": "📊",
        "purpose": "Provides an overall view of incidents, severity, impact, risk and response status.",
        "points": [
            "View total incidents",
            "View critical incidents",
            "View high-risk incidents",
            "View affected users",
            "View severity distribution",
            "View incident history"
        ]
    },

    "Incident Input": {
        "icon": "📋",
        "purpose": "Collects the information required to analyze an incident.",
        "points": [
            "Enter incident description",
            "Select incident category",
            "Enter affected users",
            "Submit incident for analysis"
        ]
    },

    "AI Analysis": {
        "icon": "🤖",
        "purpose": "Analyzes the incident description and identifies important information.",
        "points": [
            "Understand incident description",
            "Identify possible problem",
            "Analyze incident keywords",
            "Support severity assessment",
            "Support risk assessment"
        ]
    },

    "Severity Analysis": {
        "icon": "🎯",
        "purpose": "Determines how serious the incident is.",
        "points": [
            "Low severity",
            "Medium severity",
            "High severity",
            "Critical severity"
        ]
    },

    "Root Cause Analysis": {
        "icon": "🔍",
        "purpose": "Identifies the possible reason behind the incident.",
        "points": [
            "CPU problems",
            "Memory problems",
            "Database problems",
            "Network problems",
            "Security problems",
            "Application failures"
        ]
    },

    "Impact Assessment": {
        "icon": "👥",
        "purpose": "Determines how strongly the incident affects users or services.",
        "points": [
            "Number of affected users",
            "Service impact",
            "Operational impact",
            "Impact classification"
        ]
    },

    "Risk Assessment": {
        "icon": "⚠️",
        "purpose": "Determines the overall risk created by the incident.",
        "points": [
            "Analyze severity",
            "Analyze impact",
            "Classify overall risk",
            "Prioritize incident"
        ]
    },

    "Decision Intelligence": {
        "icon": "🧠",
        "purpose": "Uses the incident analysis to support better response decisions.",
        "points": [
            "Evaluate response options",
            "Prioritize actions",
            "Generate decision score",
            "Support faster decision-making"
        ]
    },

    "Recommendation": {
        "icon": "💡",
        "purpose": "Provides the recommended action that should be taken.",
        "points": [
            "Immediate response",
            "Investigation",
            "Corrective action",
            "Monitoring"
        ]
    },

    "Incident Report": {
        "icon": "📝",
        "purpose": "Generates a complete summary of the analyzed incident.",
        "points": [
            "Incident details",
            "Severity",
            "Root cause",
            "Impact",
            "Risk",
            "Recommendation"
        ]
    }
}


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="main-title">
        🚨 AI Incident Response & Decision Intelligence
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Intelligent incident analysis, risk assessment and decision support system
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <div class="sidebar-title">
        📌 Project Modules
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <div class="sidebar-subtitle">
        Select a module
    </div>
    """,
    unsafe_allow_html=True
)


for name, data in modules.items():

    if st.sidebar.button(
        f"{data['icon']}  {name}",
        key=f"btn_{name}",
        use_container_width=True
    ):
        st.session_state.selected_module = name


# =========================================================
# SELECTED MODULE
# =========================================================

selected = st.session_state.selected_module
module = modules[selected]


st.markdown(
    f"""
    <div class="module-heading">
        {module['icon']} {selected}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PURPOSE
# =========================================================

st.markdown(
    f"""
    <div class="purpose-box">
        <div class="purpose-title">
            🎯 Purpose
        </div>

        <div class="purpose-text">
            {module['purpose']}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MODULE FUNCTIONS
# =========================================================

if selected not in ["Incident Input", "Dashboard"]:

    st.markdown(
        """
        <div class="section-title">
            What this module does
        </div>
        """,
        unsafe_allow_html=True
    )

    for point in module["points"]:
        st.markdown(
            f"""
            <div class="feature-item">
                <span class="check">✓</span>
                {point}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# DASHBOARD
# =========================================================

if selected == "Dashboard":

    st.markdown(
        """
        <div class="section-title">
            📈 Incident Overview
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.incidents:

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Incidents", 0)
        col2.metric("Critical Incidents", 0)
        col3.metric("High Risk", 0)
        col4.metric("Affected Users", 0)

        st.info(
            "No incidents available. Go to Incident Input and analyze an incident."
        )

    else:

        df = pd.DataFrame(st.session_state.incidents)

        total = len(df)

        critical = len(
            df[df["Severity"] == "Critical"]
        )

        high_risk = len(
            df[df["Risk"].isin(["High", "Very High"])]
        )

        users = int(df["Affected Users"].sum())

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Incidents", total)
        col2.metric("Critical Incidents", critical)
        col3.metric("High Risk", high_risk)
        col4.metric("Affected Users", users)

        st.markdown("### Severity Distribution")

        severity_data = df["Severity"].value_counts()

        st.bar_chart(severity_data)

        st.markdown("### Incident Categories")

        category_data = df["Category"].value_counts()

        st.bar_chart(category_data)

        st.markdown("### Incident History")

        st.dataframe(
            df,
            use_container_width=True
        )


# =========================================================
# INCIDENT INPUT
# =========================================================

elif selected == "Incident Input":

    st.markdown(
        """
        <div class="section-title">
            📋 Enter Incident Details
        </div>
        """,
        unsafe_allow_html=True
    )

    description = st.text_area(
        "Describe the Incident",
        placeholder=(
            "Example: Production server CPU reached 98% "
            "and 500 users are experiencing slow response."
        ),
        height=150
    )

    category = st.selectbox(
        "Incident Category",
        [
            "Server",
            "Network",
            "Security",
            "Application",
            "Database",
            "Service",
            "Other"
        ]
    )

    affected_users = st.number_input(
        "Number of Affected Users",
        min_value=0,
        value=50,
        step=1
    )

    if st.button(
        "🚀 Analyze Incident",
        use_container_width=True
    ):

        if not description.strip():

            st.warning(
                "Please enter an incident description."
            )

        else:

            text = description.lower()


            # =============================================
            # SEVERITY
            # =============================================

            if (
                "ransomware" in text
                or "data breach" in text
                or "server down" in text
                or "database unavailable" in text
                or affected_users >= 1000
            ):

                severity = "Critical"

            elif (
                "crash" in text
                or "failure" in text
                or "98%" in text
                or "99%" in text
                or affected_users >= 500
            ):

                severity = "High"

            elif affected_users >= 50:

                severity = "Medium"

            else:

                severity = "Low"


            # =============================================
            # ROOT CAUSE
            # =============================================

            if "cpu" in text:

                root_cause = (
                    "Possible CPU resource exhaustion "
                    "or high processing workload."
                )

            elif "memory" in text or "ram" in text:

                root_cause = (
                    "Possible memory exhaustion "
                    "or high memory consumption."
                )

            elif "database" in text:

                root_cause = (
                    "Possible database connectivity "
                    "or performance problem."
                )

            elif "network" in text:

                root_cause = (
                    "Possible network connectivity "
                    "or infrastructure problem."
                )

            elif (
                "ransomware" in text
                or "malware" in text
                or "attack" in text
                or "unauthorized" in text
            ):

                root_cause = (
                    "Possible cybersecurity threat "
                    "or unauthorized activity."
                )

            elif "crash" in text:

                root_cause = (
                    "Possible application software failure."
                )

            else:

                root_cause = (
                    "Root cause requires further investigation."
                )


            # =============================================
            # IMPACT
            # =============================================

            if affected_users >= 1000:

                impact = "Very High"

            elif affected_users >= 500:

                impact = "High"

            elif affected_users >= 50:

                impact = "Medium"

            else:

                impact = "Low"


            # =============================================
            # RISK
            # =============================================

            if severity == "Critical":

                risk = "Very High"

            elif severity == "High":

                risk = "High"

            elif severity == "Medium":

                risk = "Medium"

            else:

                risk = "Low"


            # =============================================
            # DECISION INTELLIGENCE
            # =============================================

            if severity == "Critical":

                actions = [
                    "Immediately escalate the incident",
                    "Investigate the root cause",
                    "Apply corrective action",
                    "Monitor the affected service"
                ]

                recommendation = (
                    "Immediately escalate the incident "
                    "and apply corrective action."
                )

                decision_score = 95


            elif severity == "High":

                actions = [
                    "Prioritize root-cause investigation",
                    "Apply corrective action",
                    "Monitor the affected service",
                    "Escalate if the issue continues"
                ]

                recommendation = (
                    "Prioritize investigation and "
                    "apply corrective action."
                )

                decision_score = 88


            elif severity == "Medium":

                actions = [
                    "Investigate the incident",
                    "Monitor the service",
                    "Apply corrective action if required"
                ]

                recommendation = (
                    "Investigate the incident and "
                    "closely monitor the service."
                )

                decision_score = 75


            else:

                actions = [
                    "Monitor the incident",
                    "Document the incident"
                ]

                recommendation = (
                    "Monitor and document the incident."
                )

                decision_score = 60


            # =============================================
            # SAVE ANALYSIS
            # =============================================

            st.session_state.analysis = {

                "description": description,

                "category": category,

                "affected_users": affected_users,

                "severity": severity,

                "root_cause": root_cause,

                "impact": impact,

                "risk": risk,

                "actions": actions,

                "recommendation": recommendation,

                "decision_score": decision_score
            }


            # =============================================
            # SAVE INCIDENT
            # =============================================

            st.session_state.incidents.append({

                "Time": datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                ),

                "Category": category,

                "Severity": severity,

                "Impact": impact,

                "Risk": risk,

                "Affected Users": affected_users
            })


            st.success(
                "✅ Incident analyzed successfully!"
            )

            st.info(
                "Now open the other modules from the sidebar "
                "to view the analysis."
            )


# =========================================================
# AI ANALYSIS
# =========================================================

elif selected == "AI Analysis":

    if st.session_state.analysis:

        data = st.session_state.analysis

        st.markdown("### 🤖 AI Analysis Result")

        st.write(
            "**Incident:**",
            data["description"]
        )

        st.write(
            "**Category:**",
            data["category"]
        )

        st.write(
            "**Affected Users:**",
            data["affected_users"]
        )

        st.write(
            "**Detected Problem:**",
            data["root_cause"]
        )

    else:

        st.info(
            "Analyze an incident first from Incident Input."
        )


# =========================================================
# SEVERITY
# =========================================================

elif selected == "Severity Analysis":

    if st.session_state.analysis:

        severity = st.session_state.analysis["severity"]

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">
                    Incident Severity
                </div>

                <div class="result-value">
                    {severity}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "Analyze an incident first."
        )


# =========================================================
# ROOT CAUSE
# =========================================================

elif selected == "Root Cause Analysis":

    if st.session_state.analysis:

        st.markdown("### 🔍 Possible Root Cause")

        st.info(
            st.session_state.analysis["root_cause"]
        )

    else:

        st.info(
            "Analyze an incident first."
        )


# =========================================================
# IMPACT
# =========================================================

elif selected == "Impact Assessment":

    if st.session_state.analysis:

        data = st.session_state.analysis

        col1, col2 = st.columns(2)

        col1.metric(
            "Affected Users",
            data["affected_users"]
        )

        col2.metric(
            "Impact Level",
            data["impact"]
        )

    else:

        st.info(
            "Analyze an incident first."
        )


# =========================================================
# RISK
# =========================================================

elif selected == "Risk Assessment":

    if st.session_state.analysis:

        risk = st.session_state.analysis["risk"]

        st.markdown(
            f"""
            <div class="risk-card">

                <div class="risk-title">
                    ⚠️ Overall Risk
                </div>

                <div class="risk-value">
                    {risk}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "Analyze an incident first."
        )


# =========================================================
# DECISION INTELLIGENCE
# =========================================================

elif selected == "Decision Intelligence":

    if st.session_state.analysis:

        data = st.session_state.analysis

        st.markdown(
            "### 🧠 Intelligent Response Options"
        )

        for number, action in enumerate(
            data["actions"],
            start=1
        ):

            st.markdown(
                f"**{number}.** {action}"
            )

        st.markdown("### Decision Score")

        st.progress(
            data["decision_score"] / 100
        )

        st.write(
            f"Decision Confidence: "
            f"**{data['decision_score']}%**"
        )

    else:

        st.info(
            "Analyze an incident first."
        )


# =========================================================
# RECOMMENDATION
# =========================================================

elif selected == "Recommendation":

    if st.session_state.analysis:

        st.markdown(
            "### 💡 Recommended Action"
        )

        st.success(
            st.session_state.analysis[
                "recommendation"
            ]
        )

    else:

        st.info(
            "Analyze an incident first."
        )


# =========================================================
# INCIDENT REPORT
# =========================================================

elif selected == "Incident Report":

    if st.session_state.analysis:

        data = st.session_state.analysis

        report = f"""
AI INCIDENT RESPONSE & DECISION INTELLIGENCE
INCIDENT REPORT

Date:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

==================================================

INCIDENT
{data["description"]}

CATEGORY
{data["category"]}

AFFECTED USERS
{data["affected_users"]}

SEVERITY
{data["severity"]}

ROOT CAUSE
{data["root_cause"]}

IMPACT
{data["impact"]}

RISK
{data["risk"]}

RECOMMENDATION
{data["recommendation"]}

DECISION SCORE
{data["decision_score"]}%

==================================================

Generated by AI Incident Response & Decision Intelligence
"""

        st.text_area(
            "Generated Incident Report",
            report,
            height=450
        )

        st.download_button(
            "📥 Download Report",
            report,
            file_name="AI_Incident_Report.txt",
            mime="text/plain",
            use_container_width=True
        )

    else:

        st.info(
            "Analyze an incident first to generate a report."
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🚨 AI Incident Response & Decision Intelligence
        | B.Tech AIML Project
    </div>
    """,
    unsafe_allow_html=True
)