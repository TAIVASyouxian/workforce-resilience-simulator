import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="TAIVAS Labor Risk | Workforce Resilience Simulator V3",
    page_icon="🔥",
    layout="wide"
)

# -----------------------------
# Language text
# -----------------------------
LANG_TEXT = {
    "English": {
        "title": "🔥 Workforce Resilience Simulator V3",
        "subtitle": "Skill matrix + single-point-of-failure + system status + Monte Carlo break-risk simulation.",
        "positioning": "<b>Positioning:</b> This is not a scheduling tool. It is a workforce stress-testing model for operational risk. It helps identify fragile time windows, overloaded roles, missing backup skills, single-point-of-failure exposure, and probabilistic break risk.",
        "language_header": "🌐 Language / 語言",
        "language_select": "Select language / 選擇語言",
        "scenario_control": "⚙️ Scenario Control",
        "stress_scenario": "Stress Scenario",
        "general_absence": "General Absence Count",
        "peak_demand": "Peak Demand Increase",
        "staff_matrix": "👥 Staff Skill Matrix",
        "absent_staff": "Absent Staff",
        "role_demand": "🕒 Role Demand by Time",
        "simulation": "🎲 Break-Risk Simulation",
        "simulation_runs": "Simulation Runs",
        "absence_probability": "Random Absence Probability",
        "normal": "Normal",
        "peak": "Peak Demand",
        "absence": "High Absence",
        "combined": "Combined Stress",
        "single": "Single Person Absence",
        "active_staff": "Active Staff",
        "critical_slots": "Critical Slots",
        "worst_shortfall": "Worst Shortfall",
        "risk_score": "Risk Score",
        "break_probability": "Break Probability",
        "roles_monitored": "Roles Monitored",
        "system_status": "🧠 System Status",
        "stable": "🟢 System Stable",
        "warning": "🟡 System Under Pressure",
        "critical": "🔴 System Critical",
        "stable_desc": "No critical risk detected under the current scenario.",
        "warning_desc": "Some operational risk detected. Backup planning is recommended.",
        "critical_desc": "High workforce failure risk detected. Immediate mitigation is recommended.",
        "scenario_summary": "📌 Current Scenario Summary",
        "tab_dashboard": "📊 Risk Dashboard",
        "tab_skill": "🧩 Skill Matrix",
        "tab_spof": "⚠️ Single-Point Failure",
        "tab_simulation": "🎲 Break Simulation",
        "tab_recommend": "🛠 Recommendations",
        "risk_heatmap": "Workforce Risk Heatmap",
        "shortfall_trend": "Shortfall Trend",
        "role_capacity": "Role Capacity",
        "current_skill_matrix": "Current Skill Matrix",
        "coverage_summary": "Role Coverage Summary",
        "spof_title": "Single-Point-of-Failure Analysis",
        "spof_caption": "This table simulates the impact if each staff member becomes unavailable.",
        "highest_dependency": "Highest dependency: **{staff}**. If absent, critical slots: **{slots}**, exposed roles: **{roles}**.",
        "simulation_title": "Monte Carlo Break-Risk Simulation",
        "simulation_caption": "This simulation randomly removes staff based on absence probability and estimates how often the organization enters a critical shortfall state.",
        "recommended_actions": "Recommended Actions",
        "fragility": "The current workforce structure shows operational fragility.",
        "resilient": "Current structure has basic operational resilience. Continue monitoring demand changes and absence patterns.",
        "immediate": "Immediate Actions",
        "skill_backup": "Skill / Backup Actions",
        "structural": "Structural Actions",
        "add_backup": "- Add backup coverage around **{time}**.",
        "reduce_tasks": "- Reduce non-essential duties during critical time windows.",
        "floater": "- Assign a floating support person during peak periods.",
        "no_immediate": "- No immediate critical shortage detected.",
        "weak_roles": "- Roles with weak backup: {roles}",
        "cross_train": "- Cross-train at least one additional person for each weak role.",
        "backup_ok": "- Current role backup is acceptable.",
        "auto_admin": "- Automate repetitive administrative tasks such as payment tracking, reminders, document checks, and routine reporting.",
        "separate_work": "- Separate high-value human work from repetitive operational work.",
        "normal_absence": "- Treat absence and peak demand as normal operating conditions, not rare accidents.",
        "caption": "TAIVAS Labor Risk V3 | Decision-support only. This simulator does not automatically make staffing or employment decisions.",
    },
    "繁體中文": {
        "title": "🔥 人力韌性模擬器 V3",
        "subtitle": "技能矩陣＋單點故障＋系統狀態＋蒙地卡羅爆線風險模擬。",
        "positioning": "<b>定位：</b>這不是排班工具，而是用來檢測人力承載與營運風險的壓力測試模型。它可以協助辨識脆弱時段、過載角色、缺乏備援技能、單點故障風險，以及爆線機率。",
        "language_header": "🌐 Language / 語言",
        "language_select": "Select language / 選擇語言",
        "scenario_control": "⚙️ 情境控制",
        "stress_scenario": "壓力情境",
        "general_absence": "一般缺勤人數",
        "peak_demand": "尖峰需求增加",
        "staff_matrix": "👥 人員技能矩陣",
        "absent_staff": "缺勤人員",
        "role_demand": "🕒 各時段角色需求",
        "simulation": "🎲 爆線風險模擬",
        "simulation_runs": "模擬次數",
        "absence_probability": "隨機缺勤機率",
        "normal": "正常情境",
        "peak": "尖峰需求",
        "absence": "高缺勤",
        "combined": "複合壓力",
        "single": "單人缺勤",
        "active_staff": "可用人員",
        "critical_slots": "高風險時段",
        "worst_shortfall": "最大缺口",
        "risk_score": "風險分數",
        "break_probability": "爆線機率",
        "roles_monitored": "監測角色",
        "system_status": "🧠 系統狀態",
        "stable": "🟢 系統穩定",
        "warning": "🟡 系統承壓",
        "critical": "🔴 系統危急",
        "stable_desc": "目前情境下未偵測到關鍵風險。",
        "warning_desc": "偵測到部分營運風險，建議提前規劃備援。",
        "critical_desc": "偵測到高度人力失效風險，建議立即處理。",
        "scenario_summary": "📌 目前情境摘要",
        "tab_dashboard": "📊 風險儀表板",
        "tab_skill": "🧩 技能矩陣",
        "tab_spof": "⚠️ 單點故障",
        "tab_simulation": "🎲 爆線模擬",
        "tab_recommend": "🛠 改善建議",
        "risk_heatmap": "人力風險熱區表",
        "shortfall_trend": "人力缺口趨勢",
        "role_capacity": "角色可用能力",
        "current_skill_matrix": "目前技能矩陣",
        "coverage_summary": "角色備援摘要",
        "spof_title": "單點故障分析",
        "spof_caption": "此表模擬每位人員無法到班時，對整體營運造成的影響。",
        "highest_dependency": "最高依賴人員：**{staff}**。若此人缺勤，高風險時段：**{slots}**，受影響角色：**{roles}**。",
        "simulation_title": "蒙地卡羅爆線風險模擬",
        "simulation_caption": "此模擬會依照隨機缺勤機率移除人員，估算組織進入關鍵人力缺口狀態的比例。",
        "recommended_actions": "改善建議",
        "fragility": "目前人力結構顯示出營運脆弱性。",
        "resilient": "目前結構具備基本營運韌性，建議持續監測需求變化與缺勤情境。",
        "immediate": "立即處理",
        "skill_backup": "技能／備援調整",
        "structural": "結構性調整",
        "add_backup": "- 在 **{time}** 增加備援人力。",
        "reduce_tasks": "- 在關鍵時段減少非必要工作。",
        "floater": "- 尖峰時段配置機動支援人員。",
        "no_immediate": "- 目前未偵測到立即性關鍵缺口。",
        "weak_roles": "- 備援薄弱角色：{roles}",
        "cross_train": "- 針對每個薄弱角色，至少訓練一名額外備援人員。",
        "backup_ok": "- 目前角色備援狀態尚可。",
        "auto_admin": "- 將重複行政工作自動化，例如繳費追蹤、提醒、文件檢查與例行報表。",
        "separate_work": "- 將高價值人工作業與重複性營運工作分開。",
        "normal_absence": "- 將缺勤與尖峰需求視為正常營運條件，而不是罕見意外。",
        "caption": "TAIVAS Labor Risk V3｜僅供決策輔助，不會自動做出人事或排班決策。",
    }
}

# -----------------------------
# Sidebar language
# -----------------------------
st.sidebar.header("🌐 Language / 語言")
language = st.sidebar.selectbox("Select language / 選擇語言", ["English", "繁體中文"])
T = LANG_TEXT[language]

scenario_display_options = [T["normal"], T["peak"], T["absence"], T["combined"], T["single"]]
scenario_key_map = {
    T["normal"]: "Normal",
    T["peak"]: "Peak Demand",
    T["absence"]: "High Absence",
    T["combined"]: "Combined Stress",
    T["single"]: "Single Person Absence",
}

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    '''
    <style>
    .main-title {
        font-size: 2.35rem;
        font-weight: 900;
        margin-bottom: 0.15rem;
    }
    .subtitle {
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 1.3rem;
    }
    .note-box {
        padding: 0.9rem 1rem;
        border-left: 5px solid #2563eb;
        background: #eff6ff;
        color: #1f2937 !important;
        border-radius: 0.7rem;
        margin-bottom: 1rem;
        font-size: 0.98rem;
        line-height: 1.65;
    }
    .note-box b { color: #111827 !important; }
    .section-label {
        font-size: 1.1rem;
        font-weight: 800;
        margin-top: 0.5rem;
    }
    .summary-box {
        padding: 1rem;
        border-radius: 0.8rem;
        border: 1px solid #374151;
        margin-bottom: 1rem;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

st.markdown(f'<div class="main-title">{T["title"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtitle">{T["subtitle"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="note-box">{T["positioning"]}</div>', unsafe_allow_html=True)

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header(T["scenario_control"])
scenario_display = st.sidebar.selectbox(T["stress_scenario"], scenario_display_options)
scenario = scenario_key_map[scenario_display]
baseline_absence = st.sidebar.slider(T["general_absence"], min_value=0, max_value=5, value=0)
peak_demand_add = st.sidebar.slider(T["peak_demand"], min_value=0, max_value=5, value=1)

st.sidebar.divider()
st.sidebar.subheader(T["simulation"])
simulation_runs = st.sidebar.slider(T["simulation_runs"], min_value=100, max_value=2000, value=500, step=100)
absence_probability = st.sidebar.slider(T["absence_probability"], min_value=0.00, max_value=0.50, value=0.10, step=0.01)

st.sidebar.divider()
st.sidebar.subheader(T["staff_matrix"])

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

skill_columns = ["Front Desk", "Classroom", "Meal Support", "Pickup", "Admin", "Cleaning", "Emergency"]

staff_df = st.sidebar.data_editor(
    default_staff,
    use_container_width=True,
    hide_index=True,
    num_rows="dynamic",
    key=f"staff_editor_{language}"
)

staff_names = staff_df["Staff"].dropna().astype(str).tolist()
selected_absent_staff = None
if scenario == "Single Person Absence" and staff_names:
    selected_absent_staff = st.sidebar.selectbox(T["absent_staff"], staff_names)

st.sidebar.divider()
st.sidebar.subheader(T["role_demand"])

time_slots = [
    "07:00-08:00", "08:00-09:00", "09:00-10:00", "10:00-11:00",
    "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
    "15:00-16:00", "16:00-17:00", "17:00-18:00", "18:00-19:00",
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
    key=f"demand_editor_{language}"
)

# -----------------------------
# Prepare data
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

def apply_scenario_to_staff(staff_input: pd.DataFrame) -> pd.DataFrame:
    active = staff_input.copy()
    if scenario == "Single Person Absence" and selected_absent_staff:
        active = active[active["Staff"] != selected_absent_staff].copy()
    elif baseline_absence > 0:
        active = active.iloc[max(0, baseline_absence):].copy()

    if scenario == "High Absence":
        active = active.iloc[max(0, baseline_absence + 1):].copy()
    elif scenario == "Combined Stress":
        active = active.iloc[max(0, baseline_absence + 1):].copy()
    return active

def apply_scenario_to_demand(demand_input: pd.DataFrame) -> pd.DataFrame:
    effective = demand_input.copy()
    if scenario in ["Peak Demand", "Combined Stress"]:
        peak_roles = ["Front Desk", "Classroom", "Pickup", "Meal Support"]
        for role in peak_roles:
            effective[role] = effective[role] + peak_demand_add
    return effective

active_staff_df = apply_scenario_to_staff(staff_df)
effective_demand_df = apply_scenario_to_demand(demand_df)
role_capacity = {role: int(active_staff_df[role].sum()) for role in skill_columns}

def calculate_risk_rows(capacity: dict, demand_table: pd.DataFrame):
    rows = []
    for _, row in demand_table.iterrows():
        time_slot = row["Time Slot"]
        total_gap = 0
        critical_roles = []
        for role in skill_columns:
            demand = int(row[role])
            cap = int(capacity.get(role, 0))
            gap = cap - demand
            total_gap += min(0, gap)
            if gap < 0:
                critical_roles.append(f"{role} ({gap})")

        if total_gap >= 0:
            risk_level = "Low" if language == "English" else "低"
        elif total_gap == -1:
            risk_level = "High" if language == "English" else "高"
        else:
            risk_level = "Critical" if language == "English" else "極高"

        rows.append(
            {
                "Time Slot": time_slot,
                "Total Shortfall": total_gap,
                "Risk Level": risk_level,
                "Critical Roles": ", ".join(critical_roles) if critical_roles else ("None" if language == "English" else "無")
            }
        )
    return pd.DataFrame(rows)

risk_df = calculate_risk_rows(role_capacity, effective_demand_df)
critical_slots = int((risk_df["Total Shortfall"] < 0).sum())
worst_idx = int(risk_df["Total Shortfall"].idxmin())
worst_time = str(risk_df.loc[worst_idx, "Time Slot"])
worst_gap = int(risk_df.loc[worst_idx, "Total Shortfall"])
risk_score = int(round((critical_slots / len(risk_df)) * 100)) if len(risk_df) else 0

# -----------------------------
# Monte Carlo break simulation
# -----------------------------
rng = np.random.default_rng(42)
break_count = 0
sim_records = []

base_names = staff_df["Staff"].astype(str).tolist()
for i in range(simulation_runs):
    if len(base_names) == 0:
        sim_active = staff_df.iloc[0:0].copy()
    else:
        absent_mask = rng.random(len(staff_df)) < absence_probability
        sim_active = staff_df.loc[~absent_mask].copy()

    sim_capacity = {role: int(sim_active[role].sum()) for role in skill_columns}
    sim_risk_df = calculate_risk_rows(sim_capacity, effective_demand_df)
    sim_critical_slots = int((sim_risk_df["Total Shortfall"] < 0).sum())
    sim_worst_gap = int(sim_risk_df["Total Shortfall"].min())
    broke = sim_critical_slots > 0
    if broke:
        break_count += 1

    sim_records.append(
        {
            "Run": i + 1,
            "Active Staff": len(sim_active),
            "Critical Slots": sim_critical_slots,
            "Worst Shortfall": sim_worst_gap,
            "Break": 1 if broke else 0
        }
    )

sim_df = pd.DataFrame(sim_records)
break_probability = int(round((break_count / simulation_runs) * 100)) if simulation_runs else 0
avg_active_staff = round(float(sim_df["Active Staff"].mean()), 2) if not sim_df.empty else 0
avg_critical_slots = round(float(sim_df["Critical Slots"].mean()), 2) if not sim_df.empty else 0

# -----------------------------
# SPOF
# -----------------------------
spof_rows = []
for staff_name in staff_df["Staff"].astype(str).tolist():
    test_staff_df = staff_df[staff_df["Staff"].astype(str) != staff_name].copy()
    test_capacity = {role: int(test_staff_df[role].sum()) for role in skill_columns}
    test_risk_df = calculate_risk_rows(test_capacity, effective_demand_df)
    test_critical_slots = int((test_risk_df["Total Shortfall"] < 0).sum())
    worst_test_gap = int(test_risk_df["Total Shortfall"].min())
    missing_roles = set()
    for _, row in effective_demand_df.iterrows():
        for role in skill_columns:
            if int(test_capacity.get(role, 0)) - int(row[role]) < 0:
                missing_roles.add(role)
    impact_score = int(round((test_critical_slots / len(effective_demand_df)) * 100)) if len(effective_demand_df) else 0
    skills_count = int(staff_df.loc[staff_df["Staff"].astype(str) == staff_name, skill_columns].sum(axis=1).iloc[0])
    spof_rows.append(
        {
            "Staff": staff_name,
            "Skills Covered": skills_count,
            "Critical Slots if Absent": test_critical_slots,
            "Worst Shortfall if Absent": worst_test_gap,
            "Impact Score": f"{impact_score}%",
            "Exposed Roles": ", ".join(sorted(missing_roles)) if missing_roles else ("None" if language == "English" else "無")
        }
    )

spof_df = pd.DataFrame(spof_rows)
if not spof_df.empty:
    spof_df = spof_df.sort_values(
        by=["Critical Slots if Absent", "Skills Covered"],
        ascending=[False, False]
    ).reset_index(drop=True)

# -----------------------------
# System status
# -----------------------------
if risk_score == 0 and break_probability < 20:
    status_label = T["stable"]
    status_desc = T["stable_desc"]
    status_func = st.success
elif risk_score <= 30 and break_probability < 50:
    status_label = T["warning"]
    status_desc = T["warning_desc"]
    status_func = st.warning
else:
    status_label = T["critical"]
    status_desc = T["critical_desc"]
    status_func = st.error

# -----------------------------
# KPIs and status
# -----------------------------
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
kpi1.metric(T["active_staff"], len(active_staff_df))
kpi2.metric(T["critical_slots"], critical_slots)
kpi3.metric(T["worst_shortfall"], worst_gap)
kpi4.metric(T["risk_score"], f"{risk_score}%")
kpi5.metric(T["break_probability"], f"{break_probability}%")
kpi6.metric(T["roles_monitored"], len(skill_columns))

st.markdown(f"## {T['system_status']}")
status_func(f"**{status_label}** — {status_desc}")

with st.expander(T["scenario_summary"], expanded=True):
    summary_df = pd.DataFrame(
        {
            "Metric": [
                "Scenario",
                "General Absence Count",
                "Peak Demand Increase",
                "Active Staff",
                "Critical Slots",
                "Worst Shortfall",
                "Risk Score",
                "Break Probability",
                "Simulation Runs",
                "Random Absence Probability",
            ],
            "Value": [
                scenario_display,
                baseline_absence,
                peak_demand_add,
                len(active_staff_df),
                critical_slots,
                worst_gap,
                f"{risk_score}%",
                f"{break_probability}%",
                simulation_runs,
                f"{int(absence_probability * 100)}%",
            ],
        }
    )
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [T["tab_dashboard"], T["tab_skill"], T["tab_spof"], T["tab_simulation"], T["tab_recommend"]]
)

with tab1:
    st.markdown(f'<div class="section-label">{T["risk_heatmap"]}</div>', unsafe_allow_html=True)

    def color_shortfall(val):
        if val >= 0:
            return "background-color: #dcfce7; color: #166534;"
        if val == -1:
            return "background-color: #fed7aa; color: #9a3412; font-weight: bold;"
        return "background-color: #fecaca; color: #991b1b; font-weight: bold;"

    def color_risk(val):
        if val in ["Low", "低"]:
            return "background-color: #dcfce7; color: #166534;"
        if val in ["High", "高"]:
            return "background-color: #fed7aa; color: #9a3412; font-weight: bold;"
        if val in ["Critical", "極高"]:
            return "background-color: #fecaca; color: #991b1b; font-weight: bold;"
        return ""

    styled_risk = risk_df.style.map(color_shortfall, subset=["Total Shortfall"]).map(color_risk, subset=["Risk Level"])
    st.dataframe(styled_risk, use_container_width=True, hide_index=True)

    st.markdown(f'<div class="section-label">{T["shortfall_trend"]}</div>', unsafe_allow_html=True)
    st.bar_chart(risk_df.set_index("Time Slot")[["Total Shortfall"]], use_container_width=True)

    st.markdown(f'<div class="section-label">{T["role_capacity"]}</div>', unsafe_allow_html=True)
    capacity_df = pd.DataFrame({"Role": list(role_capacity.keys()), "Available Skilled Staff": list(role_capacity.values())})
    st.dataframe(capacity_df, use_container_width=True, hide_index=True)

with tab2:
    st.markdown(f'<div class="section-label">{T["current_skill_matrix"]}</div>', unsafe_allow_html=True)
    st.dataframe(staff_df, use_container_width=True, hide_index=True)

    st.markdown(f'<div class="section-label">{T["coverage_summary"]}</div>', unsafe_allow_html=True)
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

    st.dataframe(coverage_df.style.map(color_backup, subset=["Backup Status"]), use_container_width=True, hide_index=True)

with tab3:
    st.markdown(f'<div class="section-label">{T["spof_title"]}</div>', unsafe_allow_html=True)
    st.caption(T["spof_caption"])

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

    if not spof_df.empty:
        st.dataframe(spof_df.style.map(color_impact, subset=["Impact Score"]), use_container_width=True, hide_index=True)
        top_risk = spof_df.iloc[0]
        st.warning(T["highest_dependency"].format(staff=top_risk["Staff"], slots=top_risk["Critical Slots if Absent"], roles=top_risk["Exposed Roles"]))
    else:
        st.info("No staff data available.")

with tab4:
    st.markdown(f'<div class="section-label">{T["simulation_title"]}</div>', unsafe_allow_html=True)
    st.caption(T["simulation_caption"])

    sim_kpi1, sim_kpi2, sim_kpi3 = st.columns(3)
    sim_kpi1.metric(T["break_probability"], f"{break_probability}%")
    sim_kpi2.metric("Average Active Staff" if language == "English" else "平均可用人員", avg_active_staff)
    sim_kpi3.metric("Average Critical Slots" if language == "English" else "平均高風險時段", avg_critical_slots)

    sim_chart = sim_df.groupby("Critical Slots").size().reset_index(name="Runs")
    st.bar_chart(sim_chart.set_index("Critical Slots"), use_container_width=True)

    st.dataframe(sim_df.head(100), use_container_width=True, hide_index=True)

with tab5:
    st.markdown(f'<div class="section-label">{T["recommended_actions"]}</div>', unsafe_allow_html=True)
    no_backup_roles = [role for role in skill_columns if int(active_staff_df[role].sum()) <= 1]

    if critical_slots == 0 and not no_backup_roles and break_probability < 20:
        st.success(T["resilient"])
    else:
        st.error(T["fragility"])

    st.markdown(f"### {T['immediate']}")
    if critical_slots > 0:
        st.write(T["add_backup"].format(time=worst_time))
        st.write(T["reduce_tasks"])
        st.write(T["floater"])
    else:
        st.write(T["no_immediate"])

    st.markdown(f"### {T['skill_backup']}")
    if no_backup_roles:
        st.write(T["weak_roles"].format(roles=", ".join(no_backup_roles)))
        st.write(T["cross_train"])
    else:
        st.write(T["backup_ok"])

    st.markdown(f"### {T['structural']}")
    st.write(T["auto_admin"])
    st.write(T["separate_work"])
    st.write(T["normal_absence"])

st.divider()
st.caption(T["caption"])
