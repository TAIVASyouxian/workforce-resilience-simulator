import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="TAIVAS Labor Risk | Workforce Resilience Simulator V2",
    page_icon="🔥",
    layout="wide"
)

st.markdown(
    '''
    <style>
    .main-title {
        font-size: 2.35rem;
        font-weight: 900;
        margin-bottom: 0.15rem;
    }
    .subtitle {
        color: #6b7280;
        font-size: 1rem;
        margin-bottom: 1.3rem;
    }
    .note-box {
        padding: 0.9rem 1rem;
        border-left: 5px solid #2563eb;
        background: #eff6ff;
        border-radius: 0.7rem;
        margin-bottom: 1rem;
    }
    .section-label {
        font-size: 1.1rem;
        font-weight: 800;
        margin-top: 0.5rem;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">🔥 Workforce Resilience Simulator V2</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Skill matrix + single-point-of-failure stress test + operational risk dashboard.</div>',
    unsafe_allow_html=True
)

st.markdown(
    '''
    <div class="note-box">
    <b>Positioning:</b> This is not a scheduling tool. It is a workforce stress-testing model for operational risk.
    It helps identify fragile time windows, overloaded roles, missing backup skills, and single-point-of-failure exposure.
    </div>
    ''',
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar scenario settings
# -----------------------------
st.sidebar.header("⚙️ Scenario Control")

scenario = st.sidebar.selectbox(
    "Stress Scenario",
    ["Normal", "Peak Demand", "High Absence", "Combined Stress", "Single Person Absence"]
)

baseline_absence = st.sidebar.slider("General Absence Count", min_value=0, max_value=5, value=0)
peak_demand_add = st.sidebar.slider("Peak Demand Increase", min_value=0, max_value=5, value=1)

st.sidebar.divider()
st.sidebar.subheader("👥 Staff Skill Matrix")

default_staff = pd.DataFrame(
    {
        "Staff": ["A Teacher", "B Teacher", "C Admin", "D Reception", "E Support", "F Assistant", "G Floater"],
        "Front Desk": [0, 0, 1, 1, 0, 0, 1],
        "Classroom": [1, 1, 0, 0, 1, 1, 1],
        "Meal Support": [1, 1, 0, 0, 1, 1, 1],
        "Pickup": [0, 1, 0, 1, 1, 0, 1],
        "Admin": [0, 0, 1, 1, 0, 0, 1],
        "Cleaning": [0, 0, 0, 0, 1, 1, 1],
        "Emergency": [1, 1, 0, 1, 1, 0, 1],
    }
)

skill_columns = [
    "Front Desk",
    "Classroom",
    "Meal Support",
    "Pickup",
    "Admin",
    "Cleaning",
    "Emergency",
]

staff_df = st.sidebar.data_editor(
    default_staff,
    use_container_width=True,
    hide_index=True,
    num_rows="dynamic",
    key="staff_editor"
)

staff_names = staff_df["Staff"].dropna().astype(str).tolist()

selected_absent_staff = None
if scenario == "Single Person Absence" and staff_names:
    selected_absent_staff = st.sidebar.selectbox("Absent Staff", staff_names)

st.sidebar.divider()
st.sidebar.subheader("🕒 Role Demand by Time")

time_slots = [
    "07:00-08:00",
    "08:00-09:00",
    "09:00-10:00",
    "10:00-11:00",
    "11:00-12:00",
    "12:00-13:00",
    "13:00-14:00",
    "14:00-15:00",
    "15:00-16:00",
    "16:00-17:00",
    "17:00-18:00",
    "18:00-19:00",
]

default_demand = pd.DataFrame(
    {
        "Time Slot": time_slots,
        "Front Desk": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
        "Classroom": [2, 3, 2, 2, 2, 2, 2, 2, 3, 3, 3, 2],
        "Meal Support": [0, 0, 0, 0, 2, 3, 2, 0, 0, 0, 0, 0],
        "Pickup": [1, 1, 0, 0, 0, 0, 0, 0, 1, 2, 3, 2],
        "Admin": [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
        "Cleaning": [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1],
        "Emergency": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    }
)

demand_df = st.sidebar.data_editor(
    default_demand,
    use_container_width=True,
    hide_index=True,
    key="demand_editor"
)

# -----------------------------
# Clean and prepare data
# -----------------------------
staff_df = staff_df.dropna(subset=["Staff"]).copy()
for col in skill_columns:
    if col not in staff_df.columns:
        staff_df[col] = 0
    staff_df[col] = pd.to_numeric(staff_df[col], errors="coerce").fillna(0).clip(0, 1).astype(int)

demand_df = demand_df.copy()
for col in skill_columns:
    if col not in demand_df.columns:
        demand_df[col] = 0
    demand_df[col] = pd.to_numeric(demand_df[col], errors="coerce").fillna(0).astype(int)

active_staff_df = staff_df.copy()

if scenario == "Single Person Absence" and selected_absent_staff:
    active_staff_df = active_staff_df[active_staff_df["Staff"] != selected_absent_staff].copy()
elif baseline_absence > 0:
    active_staff_df = active_staff_df.iloc[max(0, baseline_absence):].copy()

role_capacity = {}
for role in skill_columns:
    role_capacity[role] = int(active_staff_df[role].sum())

effective_demand_df = demand_df.copy()
if scenario in ["Peak Demand", "Combined Stress"]:
    peak_roles = ["Front Desk", "Classroom", "Pickup", "Meal Support"]
    for role in peak_roles:
        effective_demand_df[role] = effective_demand_df[role] + peak_demand_add

if scenario == "High Absence":
    active_staff_df = active_staff_df.iloc[max(0, baseline_absence + 1):].copy()
    role_capacity = {role: int(active_staff_df[role].sum()) for role in skill_columns}
elif scenario == "Combined Stress":
    active_staff_df = active_staff_df.iloc[max(0, baseline_absence + 1):].copy()
    role_capacity = {role: int(active_staff_df[role].sum()) for role in skill_columns}

# -----------------------------
# Risk calculation
# -----------------------------
risk_rows = []
for _, row in effective_demand_df.iterrows():
    time_slot = row["Time Slot"]
    total_gap = 0
    critical_roles = []
    for role in skill_columns:
        demand = int(row[role])
        capacity = int(role_capacity.get(role, 0))
        gap = capacity - demand
        total_gap += min(0, gap)
        if gap < 0:
            critical_roles.append(f"{role} ({gap})")

    if total_gap >= 0:
        risk_level = "Low"
    elif total_gap == -1:
        risk_level = "High"
    else:
        risk_level = "Critical"

    risk_rows.append(
        {
            "Time Slot": time_slot,
            "Total Shortfall": total_gap,
            "Risk Level": risk_level,
            "Critical Roles": ", ".join(critical_roles) if critical_roles else "None"
        }
    )

risk_df = pd.DataFrame(risk_rows)

critical_slots = int((risk_df["Total Shortfall"] < 0).sum())
worst_idx = int(risk_df["Total Shortfall"].idxmin())
worst_time = str(risk_df.loc[worst_idx, "Time Slot"])
worst_gap = int(risk_df.loc[worst_idx, "Total Shortfall"])
risk_score = int(round((critical_slots / len(risk_df)) * 100)) if len(risk_df) else 0

# -----------------------------
# Single point analysis
# -----------------------------
spof_rows = []
for staff_name in staff_df["Staff"].astype(str).tolist():
    test_staff_df = staff_df[staff_df["Staff"].astype(str) != staff_name].copy()
    test_capacity = {role: int(test_staff_df[role].sum()) for role in skill_columns}

    test_critical_slots = 0
    missing_roles = set()
    worst_test_gap = 0

    for _, row in effective_demand_df.iterrows():
        slot_gap = 0
        for role in skill_columns:
            demand = int(row[role])
            capacity = int(test_capacity.get(role, 0))
            gap = capacity - demand
            slot_gap += min(0, gap)
            if gap < 0:
                missing_roles.add(role)
        if slot_gap < 0:
            test_critical_slots += 1
        worst_test_gap = min(worst_test_gap, slot_gap)

    impact_score = int(round((test_critical_slots / len(effective_demand_df)) * 100)) if len(effective_demand_df) else 0
    skills_count = int(staff_df.loc[staff_df["Staff"].astype(str) == staff_name, skill_columns].sum(axis=1).iloc[0])
    spof_rows.append(
        {
            "Staff": staff_name,
            "Skills Covered": skills_count,
            "Critical Slots if Absent": test_critical_slots,
            "Worst Shortfall if Absent": worst_test_gap,
            "Impact Score": f"{impact_score}%",
            "Exposed Roles": ", ".join(sorted(missing_roles)) if missing_roles else "None"
        }
    )

spof_df = pd.DataFrame(spof_rows)
spof_df = spof_df.sort_values(
    by=["Critical Slots if Absent", "Skills Covered"],
    ascending=[False, False]
).reset_index(drop=True)

# -----------------------------
# Dashboard KPIs
# -----------------------------
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Active Staff", len(active_staff_df))
kpi2.metric("Critical Time Slots", critical_slots)
kpi3.metric("Worst Shortfall", worst_gap)
kpi4.metric("Risk Score", f"{risk_score}%")
kpi5.metric("Roles Monitored", len(skill_columns))

if critical_slots > 0:
    st.error(f"Critical pressure detected. Weakest window: **{worst_time}**, total shortfall: **{worst_gap}**.")
else:
    st.success("No critical shortfall detected under the current scenario.")

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Risk Dashboard", "🧩 Skill Matrix", "⚠️ Single-Point Failure", "🛠 Recommendations"]
)

with tab1:
    st.markdown('<div class="section-label">Workforce Risk Heatmap</div>', unsafe_allow_html=True)

    def color_shortfall(val):
        if val >= 0:
            return "background-color: #dcfce7; color: #166534;"
        if val == -1:
            return "background-color: #fed7aa; color: #9a3412; font-weight: bold;"
        return "background-color: #fecaca; color: #991b1b; font-weight: bold;"

    def color_risk(val):
        if val == "Low":
            return "background-color: #dcfce7; color: #166534;"
        if val == "High":
            return "background-color: #fed7aa; color: #9a3412; font-weight: bold;"
        if val == "Critical":
            return "background-color: #fecaca; color: #991b1b; font-weight: bold;"
        return ""

    styled_risk = risk_df.style.map(color_shortfall, subset=["Total Shortfall"]).map(color_risk, subset=["Risk Level"])
    st.dataframe(styled_risk, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-label">Shortfall Trend</div>', unsafe_allow_html=True)
    chart_df = risk_df.set_index("Time Slot")[["Total Shortfall"]]
    st.bar_chart(chart_df, use_container_width=True)

    st.markdown('<div class="section-label">Role Capacity</div>', unsafe_allow_html=True)
    capacity_df = pd.DataFrame(
        {
            "Role": list(role_capacity.keys()),
            "Available Skilled Staff": list(role_capacity.values())
        }
    )
    st.dataframe(capacity_df, use_container_width=True, hide_index=True)

with tab2:
    st.markdown('<div class="section-label">Current Skill Matrix</div>', unsafe_allow_html=True)
    st.dataframe(staff_df, use_container_width=True, hide_index=True)

    st.markdown('<div class="section-label">Role Coverage Summary</div>', unsafe_allow_html=True)
    coverage_df = pd.DataFrame(
        {
            "Role": skill_columns,
            "Total Skilled Staff": [int(staff_df[role].sum()) for role in skill_columns],
            "Active Skilled Staff": [int(active_staff_df[role].sum()) for role in skill_columns],
        }
    )
    coverage_df["Backup Status"] = coverage_df["Active Skilled Staff"].apply(
        lambda x: "No Backup" if x <= 1 else ("Thin Backup" if x == 2 else "Basic Backup")
    )

    def color_backup(val):
        if val == "Basic Backup":
            return "background-color: #dcfce7; color: #166534;"
        if val == "Thin Backup":
            return "background-color: #fef9c3; color: #854d0e;"
        return "background-color: #fecaca; color: #991b1b; font-weight: bold;"

    styled_coverage = coverage_df.style.map(color_backup, subset=["Backup Status"])
    st.dataframe(styled_coverage, use_container_width=True, hide_index=True)

with tab3:
    st.markdown('<div class="section-label">Single-Point-of-Failure Analysis</div>', unsafe_allow_html=True)
    st.caption("This table simulates the impact if each staff member becomes unavailable.")

    def color_impact(val):
        try:
            number = int(str(val).replace("%", ""))
        except ValueError:
            number = 0
        if number == 0:
            return "background-color: #dcfce7; color: #166534;"
        if number <= 30:
            return "background-color: #fef9c3; color: #854d0e;"
        if number <= 60:
            return "background-color: #fed7aa; color: #9a3412; font-weight: bold;"
        return "background-color: #fecaca; color: #991b1b; font-weight: bold;"

    styled_spof = spof_df.style.map(color_impact, subset=["Impact Score"])
    st.dataframe(styled_spof, use_container_width=True, hide_index=True)

    if not spof_df.empty:
        top_risk = spof_df.iloc[0]
        st.warning(
            f"Highest dependency: **{top_risk['Staff']}**. If absent, critical slots: "
            f"**{top_risk['Critical Slots if Absent']}**, exposed roles: **{top_risk['Exposed Roles']}**."
        )

with tab4:
    st.markdown('<div class="section-label">Recommended Actions</div>', unsafe_allow_html=True)

    no_backup_roles = [
        role for role in skill_columns
        if int(active_staff_df[role].sum()) <= 1
    ]

    if critical_slots == 0 and not no_backup_roles:
        st.success("Current structure has basic operational resilience. Continue monitoring demand changes and absence patterns.")
    else:
        st.error("The current workforce structure shows operational fragility.")

    st.markdown("### Immediate Actions")
    if critical_slots > 0:
        st.write(f"- Add backup coverage around **{worst_time}**.")
        st.write("- Reduce non-essential duties during critical time windows.")
        st.write("- Assign a floating support person during peak periods.")
    else:
        st.write("- No immediate critical shortage detected.")

    st.markdown("### Skill / Backup Actions")
    if no_backup_roles:
        st.write("- Roles with weak backup: " + ", ".join(no_backup_roles))
        st.write("- Cross-train at least one additional person for each weak role.")
    else:
        st.write("- Current role backup is acceptable.")

    st.markdown("### Structural Actions")
    st.write("- Automate repetitive administrative tasks such as payment tracking, reminders, document checks, and routine reporting.")
    st.write("- Separate high-value human work from repetitive operational work.")
    st.write("- Treat absence and peak demand as normal operating conditions, not rare accidents.")

st.divider()
st.caption("TAIVAS Labor Risk V2 | Decision-support only. This simulator does not automatically make staffing or employment decisions.")
