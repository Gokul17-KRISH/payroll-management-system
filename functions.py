# =============================================================================
#  PAYROLL MANAGEMENT SYSTEM — Business Logic / Backend Functions (SQLite)
#  File   : functions.py
#  Purpose: All database operations. Modified for SQLite syntax (`?` instead of `%s`).
# =============================================================================

import sqlite3
import streamlit as st
from db_config import get_connection

# =============================================================================
# SECTION 1 — EMPLOYEE MANAGEMENT
# =============================================================================

def add_employee(emp_id: int, name: str, department: str,
                 designation: str, joining_date) -> bool:
    """Inserts a new employee record into the Employee table."""
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        sql = """
            INSERT INTO Employee (emp_id, name, department, designation, joining_date)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (emp_id, name, department, designation, str(joining_date)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error(f"⚠️ Employee with ID {emp_id} already exists!")
        return False
    except sqlite3.Error as e:
        st.error(f"Error adding employee: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def view_employees(search_id: int = None) -> list:
    """Retrieves employee records from the database as a list of dicts."""
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        if search_id:
            cursor.execute("SELECT * FROM Employee WHERE emp_id = ?", (search_id,))
        else:
            cursor.execute("SELECT * FROM Employee ORDER BY emp_id")
        
        # Convert sqlite3.Row objects to standard python dictionaries
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        st.error(f"Error viewing employees: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def update_employee(emp_id: int, name: str, department: str, designation: str) -> bool:
    """Updates an existing employee's details."""
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        sql = """
            UPDATE Employee
            SET name = ?, department = ?, designation = ?
            WHERE emp_id = ?
        """
        cursor.execute(sql, (name, department, designation, emp_id))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        st.error(f"Error updating employee: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def delete_employee(emp_id: int) -> bool:
    """Deletes an employee and all related records (CASCADE)."""
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Employee WHERE emp_id = ?", (emp_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        st.error(f"Error deleting employee: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# =============================================================================
# SECTION 2 — SALARY & DEDUCTIONS
# =============================================================================

def add_salary(emp_id: int, basic_salary: float, hra: float, da: float) -> bool:
    """Inserts or updates salary details for an employee (UPSERT pattern)."""
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT salary_id FROM Salary WHERE emp_id = ?", (emp_id,))
        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                "UPDATE Salary SET basic_salary=?, hra=?, da=? WHERE emp_id=?",
                (basic_salary, hra, da, emp_id)
            )
        else:
            cursor.execute(
                "INSERT INTO Salary (emp_id, basic_salary, hra, da) VALUES (?, ?, ?, ?)",
                (emp_id, basic_salary, hra, da)
            )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error("⚠️ Invalid Employee ID. Please add the employee first.")
        return False
    except sqlite3.Error as e:
        st.error(f"Error saving salary: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def add_deductions(emp_id: int, tax: float, pf: float) -> bool:
    """Inserts or updates deduction details for an employee (UPSERT pattern)."""
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ded_id FROM Deductions WHERE emp_id = ?", (emp_id,))
        if cursor.fetchone():
            cursor.execute(
                "UPDATE Deductions SET tax=?, pf=? WHERE emp_id=?",
                (tax, pf, emp_id)
            )
        else:
            cursor.execute(
                "INSERT INTO Deductions (emp_id, tax, pf) VALUES (?, ?, ?)",
                (emp_id, tax, pf)
            )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error("⚠️ Invalid Employee ID. Please add the employee first.")
        return False
    except sqlite3.Error as e:
        st.error(f"Error saving deductions: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

# =============================================================================
# SECTION 3 — PAYROLL CALCULATION
# =============================================================================

def calculate_salary(emp_id: int) -> tuple:
    """Reads salary and deductions, computes net, saves to Payroll."""
    conn = get_connection()
    if not conn: return False, "Database connection error."
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT basic_salary, hra, da FROM Salary WHERE emp_id = ?", (emp_id,))
        salary = cursor.fetchone()
        if not salary:
            return False, "No salary record found. Please add salary details first."

        cursor.execute("SELECT tax, pf FROM Deductions WHERE emp_id = ?", (emp_id,))
        deductions = cursor.fetchone()
        if not deductions:
            return False, "No deductions record found. Please add deductions first."

        # Compute
        gross_salary     = float(salary['basic_salary']) + float(salary['hra']) + float(salary['da'])
        total_deductions = float(deductions['tax']) + float(deductions['pf'])
        net_salary       = gross_salary - total_deductions

        # UPSERT into Payroll table
        cursor.execute("SELECT payroll_id FROM Payroll WHERE emp_id = ?", (emp_id,))
        if cursor.fetchone():
            cursor.execute(
                """UPDATE Payroll
                   SET gross_salary=?, total_deductions=?, net_salary=?
                   WHERE emp_id=?""",
                (gross_salary, total_deductions, net_salary, emp_id)
            )
        else:
            cursor.execute(
                """INSERT INTO Payroll (emp_id, gross_salary, total_deductions, net_salary)
                   VALUES (?, ?, ?, ?)""",
                (emp_id, gross_salary, total_deductions, net_salary)
            )

        conn.commit()
        return True, f"Net Salary = ₹{net_salary:,.2f}"

    except sqlite3.Error as e:
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def generate_payslip(emp_id: int) -> dict:
    """Retrieves all payslip data by joining the tables."""
    conn = get_connection()
    if not conn: return None
    try:
        cursor = conn.cursor()
        sql = """
            SELECT
                e.emp_id, e.name, e.department, e.designation, e.joining_date,
                s.basic_salary, s.hra, s.da,
                d.tax, d.pf,
                p.gross_salary, p.total_deductions, p.net_salary
            FROM Employee e
            LEFT JOIN Salary     s ON e.emp_id = s.emp_id
            LEFT JOIN Deductions d ON e.emp_id = d.emp_id
            LEFT JOIN Payroll    p ON e.emp_id = p.emp_id
            WHERE e.emp_id = ?
        """
        cursor.execute(sql, (emp_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    except sqlite3.Error as e:
        st.error(f"Error generating payslip: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_all_payroll_summary() -> list:
    """Returns a summary of all employees with their payroll data."""
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        sql = """
            SELECT
                e.emp_id, e.name, e.department, e.designation,
                p.gross_salary, p.total_deductions, p.net_salary
            FROM Employee e
            LEFT JOIN Payroll p ON e.emp_id = p.emp_id
            ORDER BY e.emp_id
        """
        cursor.execute(sql)
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        st.error(f"Error fetching payroll summary: {e}")
        return []
    finally:
        cursor.close()
        conn.close()
