# =============================================================================
#  PAYROLL MANAGEMENT SYSTEM — Streamlit Frontend
#  File   : main.py
#  Purpose: Full UI for managing employees, salaries, deductions, and payslips.
#
#  HOW TO RUN:
#      streamlit run main.py
#
#  PREREQUISITES:
#      pip install streamlit mysql-connector-python
#      MySQL server running locally with root access
#      Update DB_PASSWORD in db_config.py if needed
# =============================================================================

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import datetime
import functions
from db_config import init_db

# =============================================================================
# PAGE CONFIG — must be the very first Streamlit call
# =============================================================================
st.set_page_config(
    page_title="Payroll Management System",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-initialize the database and tables on first launch
init_db()


# =============================================================================
# CUSTOM CSS — Professional, clean dark-accent styling
# =============================================================================
st.markdown("""
<style>
    /* ── Global font & background ── */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] { 
        font-family: 'Outfit', sans-serif;
    }
    
    /* Elegant app background */
    .stApp {
        background-color: #f3f6fc;
        background-image: radial-gradient(at 0% 0%, hsla(253,16%,7%,0) 0, transparent 50%), 
                          radial-gradient(at 50% 0%, hsla(225,39%,30%,0.03) 0, transparent 50%), 
                          radial-gradient(at 100% 0%, hsla(339,49%,30%,0.03) 0, transparent 50%);
    }

    /* ── Main title banner (Premium Gradient) ── */
    .main-title {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #1d4ed8 100%);
        border-radius: 16px;
        padding: 2.5rem;
        margin-bottom: 2.5rem;
        text-align: center;
        color: #ffffff;
        box-shadow: 0 10px 30px rgba(37, 99, 235, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .main-title h1 { 
        margin: 0; 
        font-size: 2.6rem; 
        font-weight: 700; 
        letter-spacing: -0.5px; 
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .main-title p { 
        margin: 8px 0 0; 
        font-size: 1.1rem; 
        opacity: 0.9; 
        font-weight: 300;
        letter-spacing: 0.5px;
    }

    /* ── Section headers ── */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0f172a;
        padding-bottom: 0.8rem;
        margin-bottom: 1.8rem;
        position: relative;
    }
    .section-header::after {
        content: '';
        position: absolute;
        left: 0;
        bottom: 0;
        height: 4px;
        width: 60px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        border-radius: 4px;
    }

    /* ── Metric cards (Premium Glass Boxes) ── */
    .metric-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 24px rgba(149, 157, 165, 0.1);
        border: 1px solid rgba(226, 232, 240, 0.8);
        margin-bottom: 1.5rem;
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 4px;
    }
    .metric-card.blue::before   { background: linear-gradient(90deg, #60a5fa, #3b82f6); }
    .metric-card.green::before  { background: linear-gradient(90deg, #34d399, #10b981); }
    .metric-card.red::before    { background: linear-gradient(90deg, #f87171, #ef4444); }
    .metric-card.purple::before { background: linear-gradient(90deg, #a78bfa, #8b5cf6); }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 35px rgba(149, 157, 165, 0.15);
    }
    .metric-card-label { 
        font-size: 0.85rem; 
        color: #475569; /* Darker gray for better contrast */
        font-weight: 700; 
        text-transform: uppercase; 
        letter-spacing: 0.08em; 
    }
    .metric-card-value { 
        font-size: 2rem; 
        font-weight: 800; 
        color: #0f172a; 
        margin-top: 5px; 
    }

    /* ── Quick Start Guide Cards ── */
    .guide-card {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }
    .guide-card:hover {
        background: #f8fafc;
        transform: translateX(4px);
        border-left-width: 6px;
    }

    /* ── Payslip container ── */
    .payslip-wrapper {
        background: white;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        border: 1px solid #f1f5f9;
        position: relative;
    }
    .payslip-header {
        text-align: center;
        background: linear-gradient(135deg, #0f172a, #1e293b);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.2);
    }
    .payslip-header h2 { margin: 0; font-size: 1.8rem; font-weight: 600; letter-spacing: 1px; }
    .payslip-header p  { margin: 8px 0 0; opacity: 0.8; font-size: 1rem; }

    /* ── Styled HTML table ── */
    .styled-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 0.95rem;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        border: 1px solid #e2e8f0;
    }
    .styled-table th {
        background: #f8fafc;
        color: #334155;
        padding: 14px 16px;
        text-align: left;
        font-weight: 600;
        border-bottom: 1px solid #e2e8f0;
    }
    .styled-table td {
        padding: 12px 16px;
        border-bottom: 1px solid #f1f5f9;
        color: #475569;
    }
    .styled-table tr:last-child td { border-bottom: none; }
    .styled-table tr:hover td { background: #fdfefe; }

    /* ── Form containers ── */
    [data-testid="stForm"] {
        background: white;
        border-radius: 16px;
        padding: 2rem !important;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    }

    /* ── Net salary highlight box ── */
    .net-salary-box {
        background: linear-gradient(135deg, #10b981, #059669);
        border-radius: 14px;
        padding: 1.8rem;
        text-align: center;
        margin-top: 2rem;
        color: white;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
        transform: scale(1);
        transition: transform 0.3s ease;
    }
    .net-salary-box:hover {
        transform: scale(1.02);
    }
    .net-salary-box h2 { color: white; margin: 5px 0 0; font-size: 2.4rem; text-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .net-salary-box p  { color: rgba(255,255,255,0.9); margin: 0; font-size: 1rem; font-weight: 500; }
    .net-salary-formula { font-size: 0.85rem; background: rgba(0,0,0,0.15); padding: 6px 15px; border-radius: 20px; display: inline-block; margin-top: 15px; font-weight: 400;}

    /* ── Sidebar styling ── */
    [data-testid="stSidebar"] { 
        background: #0f172a !important; /* Solid dark blue for maximum contrast */
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #ffffff !important; /* Force all text to absolute white */
        font-weight: 500 !important;
        opacity: 1 !important;
    }
    
    [data-testid="stSidebar"] .block-container { 
        padding-top: 2.5rem; 
    }
    
    .sidebar-brand {
        text-align:center; 
        padding-bottom: 2rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 2rem;
    }
    
    .sidebar-brand .icon { 
        font-size: 3.5rem; 
        animation: float 3s ease-in-out infinite; 
        display: inline-block;
        filter: drop-shadow(0 0 10px rgba(139, 92, 246, 0.4));
    }
    
    .sidebar-brand .title { 
        font-weight: 700; 
        font-size: 1.35rem; 
        color: #ffffff !important; 
        margin-top: 15px;
        letter-spacing: 0.5px;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .sidebar-brand .subtitle { 
        font-size: 0.75rem; 
        color: #3b82f6 !important; /* Brighter blue for visibility */
        margin-top:4px; 
        font-weight: 700; 
        letter-spacing: 1.5px;
    }
    
    /* Enhance the radio buttons (Navigation items) in the sidebar */
    .stRadio [role="radiogroup"] > div {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        margin-bottom: 8px;
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0);
    }
    
    .stRadio [role="radiogroup"] > div:hover {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255,255,255,0.1);
        transform: translateX(4px);
    }
    
    .stRadio [role="radiogroup"] > div[data-testid="stMarkdownContainer"] {
        padding: 5px;
    }
    
    /* Hide the actual radio circle button to make it look like a clean menu */
    [data-testid="stSidebar"] .stRadio input[type="radio"] { display: none; }
    
    /* Reveal the text inside the radio button labels */
    [data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        margin: 0;
        padding: 8px 12px;
    }
    
    /* Make the selected radio item glow */
    [data-testid="stSidebar"] .stRadio [role="radio"][aria-checked="true"] > div:first-child {
        background: rgba(59, 130, 246, 0.25);
        border: 1px solid rgba(96, 165, 250, 0.4);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
    }
    
    /* Give "Dashboard Overview" and "Quick Setup Guide" headers better contrast in light mode */
    h4 {
        color: #1e293b !important;
        font-weight: 700 !important;
    }

    /* ── Form inputs enhancements ── */
    .stTextInput input, .stNumberInput input, .stDateInput input {
        border-radius: 8px !important;
        border: 1px solid #cbd5e1 !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.2s !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }

    /* ── Primary Form Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #4f46e5);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.25);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #4338ca);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4);
        transform: translateY(-2px);
    }
    .stButton > button:active {
        transform: translateY(1px);
    }

    /* Hide Streamlit branding */
    #MainMenu  { visibility: hidden; }
    footer     { visibility: hidden; }
    
    /* Elegant alerts */
    .stAlert { border-radius: 10px !important; border: none !important; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def fmt(value) -> str:
    """Format a numeric value as Indian Rupee string."""
    try:
        return f"₹{float(value):,.2f}"
    except (TypeError, ValueError):
        return "₹0.00"


def render_html_table(rows: list):
    """Renders a list of dicts as a styled HTML table."""
    if not rows:
        st.info("📭 No records found.")
        return

    headers = list(rows[0].keys())
    # Build table header row
    th_cells = "".join(
        f"<th style='background:#eff6ff;color:#1e3a8a;padding:10px 14px;"
        f"border:1px solid #bfdbfe;text-align:left;font-weight:600;'>"
        f"{h.replace('_', ' ').title()}</th>"
        for h in headers
    )
    # Build data rows
    row_html = ""
    for i, row in enumerate(rows):
        bg = "#f8fafc" if i % 2 == 0 else "white"
        td_cells = "".join(
            f"<td style='padding:9px 14px;border:1px solid #e2e8f0;"
            f"background:{bg};color:#374151;'>{row[h] if row[h] is not None else '—'}</td>"
            for h in headers
        )
        row_html += f"<tr>{td_cells}</tr>"

    html = f"""
    <div style='overflow-x:auto;'>
    <table style='width:100%;border-collapse:collapse;font-size:0.88rem;'>
        <thead><tr>{th_cells}</tr></thead>
        <tbody>{row_html}</tbody>
    </table>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    st.caption(f"📊 {len(rows)} record(s) found.")


def section_header(icon: str, title: str):
    """Renders a styled section header."""
    st.markdown(
        f"<div class='section-header'>{icon} {title}</div>",
        unsafe_allow_html=True
    )


# =============================================================================
# SIDEBAR — Navigation
# =============================================================================
with st.sidebar:
    st.markdown("""
    <div class='sidebar-brand'>
        <span class='icon'>👑</span>
        <div class='title'>Payroll System</div>
        <div class='subtitle'>PREMIUM EDITION</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size: 0.75rem; font-weight: 700; color: #64748b !important; letter-spacing: 2px; margin-bottom: 5px; margin-top: 10px; padding-left: 5px;'>MAIN NAVIGATION</div>", unsafe_allow_html=True)
    
    menu_options = {
        "🏠  Dashboard Overview":    "Dashboard",
        "➕  Add New Employee":      "Add Employee",
        "👥  Employee Directory":    "View Employees",
        "✏️  Manage Employees":      "Update/Delete Employee",
        "💰  Setup Salary Base":     "Add Salary",
        "📉  Setup Deductions":      "Add Deductions",
        "📄  Generate Payslips":     "Generate Payslip",
    }
    choice_label = st.radio(
        "Select Module",
        list(menu_options.keys()),
        label_visibility="collapsed"
    )
    choice = menu_options[choice_label]

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem;color:#94a3b8;'>© 2025 Payroll Management System</div>",
        unsafe_allow_html=True
    )


# =============================================================================
# MAIN PAGE TITLE
# =============================================================================
st.markdown("""
<div class='main-title'>
    <h1>Enterprise Payroll System</h1>
    <p>Elegant • Seamless • Powerful</p>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# MODULE 0 — DASHBOARD
# =============================================================================
if choice == "Dashboard":
    section_header("🏠", "Dashboard Overview")

    # Fetch live data
    all_employees = functions.view_employees()
    payroll_data  = functions.get_all_payroll_summary()

    total_emp        = len(all_employees)
    processed_count  = sum(1 for p in payroll_data if p.get("net_salary") is not None)
    total_payroll    = sum(float(p["net_salary"] or 0) for p in payroll_data)
    avg_net          = total_payroll / processed_count if processed_count else 0

    # ── Metric cards ──
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class='metric-card blue'>
            <div class='metric-card-label'>Total Staff</div>
            <div class='metric-card-value'>{total_emp}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='metric-card purple'>
            <div class='metric-card-label'>Payrolls Issued</div>
            <div class='metric-card-value'>{processed_count}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='metric-card green'>
            <div class='metric-card-label'>Net Payout Volume</div>
            <div class='metric-card-value'>{fmt(total_payroll)}</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class='metric-card red'>
            <div class='metric-card-label'>Average Salary</div>
            <div class='metric-card-value'>{fmt(avg_net)}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Payroll summary table ──
    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.markdown("#### 📋 Payroll Summary")
        render_html_table(payroll_data)

    with col_right:
        st.markdown("#### 🧭 Quick Setup Guide")
        steps = [
            ("1", "Registration",     "Enter personal details into the directory"),
            ("2", "Compensation",     "Set base pay & allowances"),
            ("3", "Tax & PF",         "Configure required deductions"),
            ("4", "Generation",       "Issue automated secure payslips"),
        ]
        for icon, title, desc in steps:
            st.markdown(f"""
            <div class='guide-card'>
                <b style='color:#0f172a; font-size:1.05rem;'>Step {icon}: {title}</b><br>
                <span style='color:#64748b; font-size:0.85rem;'>{desc}</span>
            </div>
            """, unsafe_allow_html=True)


# =============================================================================
# MODULE 1 — ADD EMPLOYEE
# =============================================================================
elif choice == "Add Employee":
    section_header("➕", "Add New Employee")

    with st.form("add_employee_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            emp_id      = st.number_input("Employee ID *", min_value=1, step=1,
                                          help="Unique numeric ID for the employee.")
            name        = st.text_input("Full Name *", placeholder="e.g. Kiran Kumar")
            department  = st.text_input("Department *", placeholder="e.g. Engineering, HR, Finance")
        with col2:
            designation = st.text_input("Designation *", placeholder="e.g. Software Engineer")
            joining_date = st.date_input("Joining Date *", value=datetime.date.today())

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("💾 Add Employee", use_container_width=True)

    if submitted:
        # ── Validation ──
        errors = []
        if not name.strip():        errors.append("Full Name cannot be empty.")
        if not department.strip():  errors.append("Department cannot be empty.")
        if not designation.strip(): errors.append("Designation cannot be empty.")

        if errors:
            for e in errors:
                st.error(f"⚠️ {e}")
        else:
            success = functions.add_employee(
                emp_id, name.strip(), department.strip(),
                designation.strip(), joining_date
            )
            if success:
                st.success(f"✅ Employee **{name.strip()}** (ID: {emp_id}) added successfully!")
                st.balloons()


# =============================================================================
# MODULE 2 — VIEW EMPLOYEES
# =============================================================================
elif choice == "View Employees":
    section_header("👥", "Employee Directory")

    # ── Search bar ──
    col1, col2 = st.columns([3, 1])
    with col1:
        search_id = st.number_input(
            "Search by Employee ID (enter 0 to show all employees)",
            min_value=0, step=1, value=0
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("🔍 Refresh", use_container_width=True)

    rows = functions.view_employees(search_id if search_id > 0 else None)

    if not rows and search_id > 0:
        st.warning(f"⚠️ No employee found with ID **{search_id}**.")
    else:
        render_html_table(rows)


# =============================================================================
# MODULE 3 — UPDATE / DELETE EMPLOYEE
# =============================================================================
elif choice == "Update/Delete Employee":
    section_header("✏️", "Update / Delete Employee")

    tab_update, tab_delete = st.tabs(["✏️ Update Employee", "🗑️ Delete Employee"])

    # --- Update Tab ---
    with tab_update:
        st.markdown("Enter the Employee ID and the new details you'd like to save.")
        with st.form("update_employee_form"):
            emp_id      = st.number_input("Employee ID to Update *", min_value=1, step=1)
            name        = st.text_input("New Full Name *", placeholder="Updated full name")
            department  = st.text_input("New Department *", placeholder="Updated department")
            designation = st.text_input("New Designation *", placeholder="Updated designation")
            upd_btn = st.form_submit_button("✅ Update Employee", use_container_width=True)

        if upd_btn:
            errors = []
            if not name.strip():        errors.append("Full Name cannot be empty.")
            if not department.strip():  errors.append("Department cannot be empty.")
            if not designation.strip(): errors.append("Designation cannot be empty.")

            if errors:
                for e in errors:
                    st.error(f"⚠️ {e}")
            else:
                updated = functions.update_employee(
                    emp_id, name.strip(), department.strip(), designation.strip()
                )
                if updated:
                    st.success(f"✅ Employee ID **{emp_id}** updated successfully!")
                else:
                    st.warning(f"⚠️ No employee found with ID **{emp_id}**.")

    # --- Delete Tab ---
    with tab_delete:
        st.markdown(
            "> ⚠️ **Warning:** Deleting an employee will also remove all their "
            "salary, deduction, and payroll records (CASCADE DELETE)."
        )
        with st.form("delete_employee_form"):
            del_id  = st.number_input("Employee ID to Delete *", min_value=1, step=1)
            confirm = st.checkbox(
                "✔ I confirm — delete this employee and all associated records permanently."
            )
            del_btn = st.form_submit_button("🗑️ Delete Employee", use_container_width=True)

        if del_btn:
            if not confirm:
                st.error("⚠️ Please check the confirmation checkbox first.")
            else:
                deleted = functions.delete_employee(del_id)
                if deleted:
                    st.success(f"✅ Employee ID **{del_id}** and all related records deleted.")
                else:
                    st.warning(f"⚠️ No employee found with ID **{del_id}**.")


# =============================================================================
# MODULE 4 — ADD SALARY
# =============================================================================
elif choice == "Add Salary":
    section_header("💰", "Add / Update Salary Details")

    st.info(
        "If a salary record already exists for this employee, it will be **updated**.  "
        "Otherwise, a new record will be created."
    )

    with st.form("salary_form"):
        emp_id = st.number_input("Employee ID *", min_value=1, step=1)

        col1, col2, col3 = st.columns(3)
        with col1:
            basic = st.number_input("Basic Salary (₹) *", min_value=0.0,
                                    step=1000.0, format="%.2f",
                                    help="Core salary before allowances.")
        with col2:
            hra   = st.number_input("HRA — House Rent Allowance (₹)",
                                    min_value=0.0, step=500.0, format="%.2f",
                                    help="Allowance for accommodation.")
        with col3:
            da    = st.number_input("DA — Dearness Allowance (₹)",
                                    min_value=0.0, step=500.0, format="%.2f",
                                    help="Cost-of-living adjustment allowance.")

        # Live preview
        gross_preview = basic + hra + da
        st.markdown(
            f"<div style='margin-top:1rem;padding:0.8rem 1.2rem;background:#eff6ff;"
            f"border-radius:8px;font-weight:600;color:#1e3a8a;'>"
            f"📊 Estimated Gross Salary: <span style='font-size:1.2rem;'>{fmt(gross_preview)}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        sal_btn = st.form_submit_button("💾 Save Salary", use_container_width=True)

    if sal_btn:
        if basic <= 0:
            st.error("⚠️ Basic Salary must be greater than zero.")
        else:
            success = functions.add_salary(emp_id, basic, hra, da)
            if success:
                st.success(
                    f"✅ Salary saved for Employee **{emp_id}**  "
                    f"| Gross: **{fmt(gross_preview)}**"
                )


# =============================================================================
# MODULE 5 — ADD DEDUCTIONS
# =============================================================================
elif choice == "Add Deductions":
    section_header("📉", "Add / Update Deductions")

    st.info(
        "Deductions are applied to the gross salary to arrive at the net take-home pay.  "
        "If a deductions record already exists for this employee, it will be **updated**."
    )

    with st.form("deductions_form"):
        emp_id = st.number_input("Employee ID *", min_value=1, step=1)

        col1, col2 = st.columns(2)
        with col1:
            tax = st.number_input("Income Tax Deduction (₹)",
                                  min_value=0.0, step=500.0, format="%.2f",
                                  help="TDS / income tax withheld from salary.")
        with col2:
            pf  = st.number_input("Provident Fund — PF (₹)",
                                  min_value=0.0, step=500.0, format="%.2f",
                                  help="Employee PF contribution (usually 12% of basic).")

        # Live preview
        total_ded_preview = tax + pf
        st.markdown(
            f"<div style='margin-top:1rem;padding:0.8rem 1.2rem;background:#fff1f2;"
            f"border-radius:8px;font-weight:600;color:#991b1b;'>"
            f"📊 Total Deductions: <span style='font-size:1.2rem;'>{fmt(total_ded_preview)}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)
        ded_btn = st.form_submit_button("💾 Save Deductions", use_container_width=True)

    if ded_btn:
        success = functions.add_deductions(emp_id, tax, pf)
        if success:
            st.success(
                f"✅ Deductions saved for Employee **{emp_id}**  "
                f"| Total Deductions: **{fmt(total_ded_preview)}**"
            )


# =============================================================================
# MODULE 6 — GENERATE PAYSLIP
# =============================================================================
elif choice == "Generate Payslip":
    section_header("📄", "Generate Payslip")

    col_in, col_empty = st.columns([1, 2])
    with col_in:
        emp_id  = st.number_input("Employee ID", min_value=1, step=1)
        month   = st.selectbox(
            "Payslip Month",
            options=["January","February","March","April","May","June",
                     "July","August","September","October","November","December"],
            index=datetime.date.today().month - 1
        )
        year    = st.number_input("Year", min_value=2000,
                                  max_value=datetime.date.today().year,
                                  value=datetime.date.today().year)
        gen_btn = st.button("▶ Generate Payslip", type="primary", use_container_width=True)

    if gen_btn:
        with st.spinner("Calculating salary..."):
            ok, msg = functions.calculate_salary(emp_id)

        if not ok:
            st.error(f"❌ {msg}")
            st.info(
                "**Checklist before generating payslip:**\n"
                "1. Employee must be added via *Add Employee*.\n"
                "2. Salary details must be added via *Add Salary*.\n"
                "3. Deductions must be added via *Add Deductions*."
            )
        else:
            data = functions.generate_payslip(emp_id)
            if not data:
                st.error("❌ Could not retrieve payslip data. Employee may not exist.")
            else:
                payslip_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
  body {{
    font-family: 'Outfit', sans-serif;
    background: #f3f6fc;
    padding: 20px 10px;
    margin: 0;
  }}
  .wrapper {{
    background: white;
    border-radius: 16px;
    padding: 2.5rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    max-width: 900px;
    margin: auto;
  }}
  .header {{
    text-align: center;
    background: linear-gradient(135deg, #0f172a, #1e3a8a);
    color: white;
    padding: 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
  }}
  .header h2 {{ margin: 0; font-size: 1.8rem; font-weight: 700; letter-spacing: 1px; }}
  .header p  {{ margin: 8px 0 0; opacity: 0.8; font-size: 1rem; }}
  
  table {{ width: 100%; border-collapse: collapse; margin-bottom: 1.5rem; border-radius: 10px; overflow: hidden; border: 1px solid #e2e8f0; }}
  th {{ background: #f8fafc; color: #334155; padding: 14px 16px; text-align: left; font-weight: 600; border-bottom: 1px solid #e2e8f0; }}
  td {{ padding: 12px 16px; border-bottom: 1px solid #f1f5f9; color: #475569; }}
  tr:last-child td {{ border-bottom: none; }}
  
  .earn-header {{ background: #eff6ff !important; color: #1e3a8a !important; }}
  .ded-header  {{ background: #fff1f2 !important; color: #991b1b !important; }}
  .earn-total  {{ background: #ecfdf5 !important; color: #065f46 !important; font-weight: 700; }}
  .ded-total   {{ background: #fff1f2 !important; color: #991b1b !important; font-weight: 700; }}
  .amount      {{ text-align: right; }}
  .red         {{ color: #dc2626; text-align: right; }}
  
  .net-box {{
    background: linear-gradient(135deg, #10b981, #059669);
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    color: white;
    box-shadow: 0 10px 25px rgba(16,185,129,0.3);
  }}
  .net-box .emoji {{ font-size: 40px; }}
  .net-box .label {{ text-transform: uppercase; letter-spacing: 2px; font-size: 0.9rem; margin: 10px 0 5px; opacity: 0.9; }}
  .net-box .amount {{ font-size: 2.8rem; font-weight: 700; margin: 5px 0; color: white !important; text-align: center; }}
  .net-box .formula {{ font-size: 0.85rem; background: rgba(0,0,0,0.15); padding: 6px 20px; border-radius: 20px; display: inline-block; margin-top: 10px; }}
  .formula .g {{ color: #a7f3d0; }} 
  .formula .d {{ color: #fecaca; }}
  
  .footer {{ text-align: center; margin-top: 2rem; color: #94a3b8; font-size: 0.78rem; }}
</style>
</head>
<body>
<div class="wrapper">
  <div class="header">
    <h2>&#127970; Global Tech Solutions Ltd.</h2>
    <p>Official Employee Salary Slip &mdash; {month} {year}</p>
  </div>

  <table>
    <tr>
      <th style="width:22%">Employee ID</th><td>{data.get('emp_id','&mdash;')}</td>
      <th style="width:22%">Employee Name</th><td>{data.get('name','&mdash;')}</td>
    </tr>
    <tr>
      <th>Department</th><td>{data.get('department','&mdash;')}</td>
      <th>Designation</th><td>{data.get('designation','&mdash;')}</td>
    </tr>
    <tr>
      <th>Date of Joining</th><td>{data.get('joining_date','&mdash;')}</td>
      <th>Pay Period</th><td>{month} {year}</td>
    </tr>
  </table>

  <table>
    <thead>
      <tr>
        <th class="earn-header" style="width:30%">Earnings</th>
        <th class="earn-header" style="width:20%;text-align:right">Amount (&#8377;)</th>
        <th class="ded-header"  style="width:30%">Deductions</th>
        <th class="ded-header"  style="width:20%;text-align:right">Amount (&#8377;)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Basic Salary</td><td class="amount">{fmt(data.get('basic_salary',0))}</td>
        <td>Income Tax (TDS)</td><td class="red">{fmt(data.get('tax',0))}</td>
      </tr>
      <tr>
        <td>House Rent Allowance (HRA)</td><td class="amount">{fmt(data.get('hra',0))}</td>
        <td>Provident Fund (PF)</td><td class="red">{fmt(data.get('pf',0))}</td>
      </tr>
      <tr>
        <td>Dearness Allowance (DA)</td><td class="amount">{fmt(data.get('da',0))}</td>
        <td>&mdash;</td><td class="amount">&mdash;</td>
      </tr>
      <tr>
        <td class="earn-total">Gross Salary</td>
        <td class="earn-total amount">{fmt(data.get('gross_salary',0))}</td>
        <td class="ded-total">Total Deductions</td>
        <td class="ded-total amount">{fmt(data.get('total_deductions',0))}</td>
      </tr>
    </tbody>
  </table>

  <div class="net-box">
    <div class="emoji">&#128184;</div>
    <div class="label">Net Take-Home Pay</div>
    <div class="amount">{fmt(data.get('net_salary',0))}</div>
    <div class="formula">
      <span class="g">Gross {fmt(data.get('gross_salary',0))}</span>
      &nbsp;&mdash;&nbsp;
      <span class="d">Deductions {fmt(data.get('total_deductions',0))}</span>
    </div>
  </div>

  <div class="footer">This is a computer-generated payslip and does not require a signature.</div>
</div>
</body>
</html>
"""
                components.html(payslip_html, height=750, scrolling=True)


# =============================================================================
# END OF FILE
# =============================================================================
