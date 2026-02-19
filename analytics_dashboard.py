import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(
    page_title="IDALS Agent Analytics",
    layout="wide"
)

st.title("📊 IDALS Customer Care Agent – Analytics Dashboard")

FILE_PATH = "agent_analytics.csv"

# -------------------------
# Load data
# -------------------------
if not os.path.exists(FILE_PATH):
    st.error("No analytics data found yet. Please interact with the agent first.")
    st.stop()

df = pd.read_csv(FILE_PATH)

# -------------------------
# High-level metrics
# -------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Questions", len(df))
col2.metric("Escalations", df["escalation"].sum())
col3.metric(
    "Escalation Rate",
    f"{round((df['escalation'].sum() / len(df)) * 100, 1)}%"
)
col4.metric(
    "Avg Response Length",
    int(df["response_length"].mean())
)

st.divider()

# -------------------------
# Intent Distribution
# -------------------------
st.subheader("🎯 Intent Distribution")

intent_counts = df["intent"].value_counts()

fig1, ax1 = plt.subplots()
sns.barplot(
    x=intent_counts.index,
    y=intent_counts.values,
    ax=ax1
)
ax1.set_ylabel("Count")
ax1.set_xlabel("Intent")
st.pyplot(fig1)

st.divider()

# -------------------------
# Language Distribution
# -------------------------
st.subheader("🌐 Language Usage")

lang_counts = df["language"].value_counts()

fig2, ax2 = plt.subplots()
ax2.pie(
    lang_counts.values,
    labels=lang_counts.index,
    autopct="%1.1f%%",
    startangle=90
)
ax2.axis("equal")
st.pyplot(fig2)

st.divider()

# -------------------------
# Hallucination Risk
# -------------------------
st.subheader("⚠️ Hallucination Risk Overview")

risk_counts = df["hallucination_risk"].value_counts()

fig3, ax3 = plt.subplots()
sns.barplot(
    x=risk_counts.index,
    y=risk_counts.values,
    ax=ax3
)
ax3.set_ylabel("Count")
ax3.set_xlabel("Risk Level")
st.pyplot(fig3)

st.divider()

# -------------------------
# Escalation Reasons
# -------------------------
st.subheader("📞 Escalation Reasons")

esc_df = df[df["escalation"] == True]

if esc_df.empty:
    st.info("No escalations recorded yet.")
else:
    reason_counts = esc_df["reason"].value_counts()
    fig4, ax4 = plt.subplots()
    sns.barplot(
        x=reason_counts.index,
        y=reason_counts.values,
        ax=ax4
    )
    ax4.set_ylabel("Count")
    ax4.set_xlabel("Reason")
    st.pyplot(fig4)

st.divider()

# -------------------------
# Raw Data Viewer
# -------------------------
st.subheader("📋 Raw Interaction Logs")

st.dataframe(
    df.sort_values("timestamp", ascending=False),
    use_container_width=True
)
