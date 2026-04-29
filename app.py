import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Workforce Resilience Simulator",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Workforce Resilience Simulator V1")
st.caption("A decision-support demo for stress-testing workforce capacity under absence and peak demand scenarios.")

# =========================
# Sidebar Inputs
# =========================
st.sidebar.header("⚙️ Input Settings")

st.sidebar.subheader("Workforce Capacity")
total_staff = st.sidebar.slider("Total Staff", 1, 30, 6)
absence = st.sidebar.slider("Simulated Absence", 0, total_staff, 1)

available_staff = total_staff - absence

st.sidebar.subheader("Demand per Time Slot")
time_slots = [
    "07:00", "08:00", "09:00", "10:00",
    "11:00", "12:00", "13:00", "14:00",
    "15:00", "16:00", "17:00", "18:00"
]

default_demand = [2, 3, 3, 3, 5, 5, 3, 3, 4, 5, 6, 4]
demand = []

for t, default in zip(time_slots, default_demand):
    val = st.sidebar.number_input(
        f"{t} Required Staff",
        min_value=0,
        max_value=20,
        value=default,
        step=1
    )
    demand.append(val)

demand = np.array(demand)

# =========================
# Scenario Selection
# =========================
st.sidebar.subheader("Scenario")
scenario = st.sidebar.selectbox(
    "Select Stress Test Scenario",
    [
        "Baseline",
        "Peak Demand +2",
        "High Absence +2",
        "Critical Peak: Demand +2 and Absence +2"
    ]
)

scenario_demand = demand.copy()
scenario_supply_value = available_staff

if scenario == "Peak Demand +2":
    scenario_demand = demand + 2
elif scenario == "High Absence +2":
    scenario_supply_value = max(0, available_staff - 2)
elif scenario == "Critical Peak: Demand +2 and Absence +2":
    scenario_demand = demand + 2
    scenario_supply_value = max(0, available_staff - 2)

supply = np.full(len(time_slots), scenario_supply_value)
gap = supply - scenario_demand
critical_slots = int(np.sum(gap < 0))
risk_score = int((critical_slots / len(time_slots)) * 100)
minimum_backup_needed = int(abs(min(gap))) if min(gap) < 0 else 0

# =========================
# KPI Cards
# =========================
st.subheader("📌 Workforce Risk Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Available Staff", scenario_supply_value)

with col2:
    st.metric("Critical Slots", critical_slots)

with col3:
    st.metric("Risk Score", f"{risk_score}%")

with col4:
    st.metric("Minimum Backup Needed", minimum_backup_needed)

# =========================
# Dataframe / Heatmap
# =========================
st.subheader("🔥 Workforce Risk Heatmap")

risk_df = pd.DataFrame({
    "Time Slot": time_slots,
    "Required Staff": scenario_demand,
    "Available Staff": supply,
    "Gap": gap
})

risk_df["Risk Level"] = np.where(
    risk_df["Gap"] < 0,
    "High Risk",
    np.where(risk_df["Gap"] == 0, "Tight", "Stable")
)

def color_gap(val):
    if val < 0:
        return "background-color: #ffb3b3; color: #7a0000; font-weight: bold;"
    elif val == 0:
        return "background-color: #fff1a8; color: #5c4a00; font-weight: bold;"
    return "background-color: #bff0c2; color: #064d1f; font-weight: bold;"

def color_risk_level(val):
    if val == "High Risk":
        return "background-color: #ffb3b3; color: #7a0000; font-weight: bold;"
    elif val == "Tight":
        return "background-color: #fff1a8; color: #5c4a00; font-weight: bold;"
    return "background-color: #bff0c2; color: #064d1f; font-weight: bold;"

styled_df = risk_df.style.applymap(color_gap, subset=["Gap"]).applymap(color_risk_level, subset=["Risk Level"])
st.dataframe(styled_df, use_container_width=True, hide_index=True)

# =========================
# Chart
# =========================
st.subheader("📊 Demand vs Available Staff")

chart_df = risk_df.set_index("Time Slot")[["Required Staff", "Available Staff"]]
st.line_chart(chart_df, use_container_width=True)

# =========================
# Key Insights
# =========================
st.subheader("🧩 Key Insights")

if critical_slots > 0:
    worst_idx = int(np.argmin(gap))
    worst_time = time_slots[worst_idx]
    worst_gap = int(gap[worst_idx])

    st.error(f"Critical workforce failure detected at {worst_time}. Gap: {worst_gap} staff.")

    st.markdown("""
### Recommended Actions
- Add temporary backup staff during high-risk time slots.
- Reduce non-essential tasks during peak hours.
- Cross-train staff for critical functions.
- Automate repetitive administrative work where possible.
- Review whether current service scope exceeds actual workforce capacity.
""")
else:
    st.success("The workforce system remains stable under the selected scenario.")
    st.markdown("""
### Recommended Actions
- Maintain current staffing structure.
- Continue monitoring peak-hour pressure.
- Build backup capability before shortage becomes visible.
""")

# =========================
# Product Positioning Note
# =========================
st.divider()
st.caption(
    "This tool is a decision-support prototype. It does not replace professional HR, legal, or operational judgment. "
    "Its purpose is to visualize workforce fragility and operational risk under stress scenarios."
)
