import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="TAIVAS Labor Risk | Workforce Resilience Simulator",
    page_icon="🔥",
    layout="wide"
)

st.markdown(
    '''
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #6b7280;
        font-size: 1rem;
        margin-bottom: 1.2rem;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">🔥 Workforce Risk Heatmap</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">A Streamlit-based workforce resilience stress testing demo for staffing pressure, absence scenarios, and operational fragility.</div>',
    unsafe_allow_html=True
)

st.sidebar.header("⚙️ Scenario Settings")

scenario = st.sidebar.selectbox(
    "Scenario",
    ["Normal", "Peak Demand", "High Absence", "Combined Stress"]
)

total_staff = st.sidebar.slider("Total Staff", min_value=1, max_value=30, value=8)
baseline_absence = st.sidebar.slider("Baseline Absence", min_value=0, max_value=10, value=1)
extra_absence = st.sidebar.slider("Extra Absence in Stress Scenario", min_value=0, max_value=10, value=1)
peak_demand_add = st.sidebar.slider("Peak Demand Increase", min_value=0, max_value=5, value=2)

st.sidebar.divider()
st.sidebar.subheader("🕒 Time Demand")

time_slots = [
    "07:00-08:00", "08:00-09:00", "09:00-10:00", "10:00-11:00",
    "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
    "15:00-16:00", "16:00-17:00", "17:00-18:00", "18:00-19:00",
]

default_demand = [3, 4, 3, 3, 4, 5, 4, 3, 4, 5, 6, 4]

demand_values = []
for t, default in zip(time_slots, default_demand):
    demand_values.append(
        st.sidebar.number_input(
            f"{t}",
            min_value=0,
            max_value=30,
            value=default,
            step=1
        )
    )

demand = np.array(demand_values)

effective_absence = baseline_absence
effective_demand = demand.copy()

if scenario == "Peak Demand":
    effective_demand = demand + peak_demand_add
elif scenario == "High Absence":
    effective_absence = baseline_absence + extra_absence
elif scenario == "Combined Stress":
    effective_absence = baseline_absence + extra_absence
    effective_demand = demand + peak_demand_add

available_staff = max(0, total_staff - effective_absence)
supply = np.full(len(time_slots), available_staff)
gap = supply - effective_demand

def risk_level_from_gap(x: int) -> str:
    if x >= 2:
        return "Low"
    if x >= 0:
        return "Moderate"
    if x == -1:
        return "High"
    return "Critical"

risk_levels = [risk_level_from_gap(int(x)) for x in gap]

risk_df = pd.DataFrame(
    {
        "Time Slot": time_slots,
        "Required Staff": effective_demand,
        "Available Staff": supply,
        "Gap": gap,
        "Risk Level": risk_levels,
    }
)

critical_slots = int(np.sum(gap < 0))
worst_gap = int(np.min(gap))
worst_time = time_slots[int(np.argmin(gap))]
risk_score = int(round((critical_slots / len(time_slots)) * 100))

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Available Staff", available_staff)
kpi2.metric("Critical Slots", critical_slots)
kpi3.metric("Worst Gap", worst_gap)
kpi4.metric("Risk Score", f"{risk_score}%")

st.subheader("📊 Workforce Risk Table")

def color_gap(val):
    if val >= 2:
        return "background-color: #dcfce7; color: #166534;"
    if val >= 0:
        return "background-color: #fef9c3; color: #854d0e;"
    if val == -1:
        return "background-color: #fed7aa; color: #9a3412;"
    return "background-color: #fecaca; color: #991b1b; font-weight: bold;"

def color_risk_level(val):
    if val == "Low":
        return "background-color: #dcfce7; color: #166534;"
    if val == "Moderate":
        return "background-color: #fef9c3; color: #854d0e;"
    if val == "High":
        return "background-color: #fed7aa; color: #9a3412;"
    if val == "Critical":
        return "background-color: #fecaca; color: #991b1b; font-weight: bold;"
    return ""

styled_df = risk_df.style.map(color_gap, subset=["Gap"]).map(color_risk_level, subset=["Risk Level"])
st.dataframe(styled_df, use_container_width=True, hide_index=True)

st.subheader("📈 Staffing Gap by Time Slot")
chart_df = risk_df.set_index("Time Slot")[["Gap"]]
st.bar_chart(chart_df, use_container_width=True)

st.subheader("🧠 Key Insights")

if critical_slots > 0:
    st.error(
        f"Critical workforce pressure detected. The weakest time slot is **{worst_time}**, with a staffing gap of **{worst_gap}**."
    )
else:
    st.success("Current staffing structure remains stable under this scenario.")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### 🔍 Diagnosis")
    if critical_slots == 0:
        st.write("- No immediate shortage detected.")
        st.write("- Current staffing has basic resilience under the selected scenario.")
    else:
        st.write(f"- {critical_slots} time slot(s) fall below required staffing.")
        st.write("- The model indicates operational fragility under absence or peak demand.")
        st.write("- This is a structural capacity issue, not merely an individual effort issue.")

with col_b:
    st.markdown("### 🛠 Suggested Actions")
    if critical_slots == 0:
        st.write("- Maintain backup coverage.")
        st.write("- Continue monitoring high-demand periods.")
    else:
        st.write("- Add backup staff during critical time slots.")
        st.write("- Reduce non-essential tasks during peak periods.")
        st.write("- Cross-train at least one additional person for critical duties.")
        st.write("- Automate repetitive administrative work where possible.")

st.subheader("⚡ Stress Test Summary")

summary_df = pd.DataFrame(
    {
        "Metric": [
            "Scenario",
            "Total Staff",
            "Effective Absence",
            "Available Staff",
            "Highest Required Staff",
            "Critical Slots",
            "Risk Score"
        ],
        "Value": [
            scenario,
            total_staff,
            effective_absence,
            available_staff,
            int(np.max(effective_demand)),
            critical_slots,
            f"{risk_score}%"
        ]
    }
)

st.dataframe(summary_df, use_container_width=True, hide_index=True)

st.caption("V1 demo | Workforce Resilience Simulator | Decision-support only, not an automatic staffing decision system.")
