-- =============================================================================
--  PAYROLL MANAGEMENT SYSTEM — Database Schema (SQLite Version)
--  File   : schema.sql
--  Purpose: Creates the SQLite tables. Automatically executed by db_config.py
-- =============================================================================

-- =============================================================================
-- TABLE 1: Employee
-- Stores basic information about each employee.
-- =============================================================================
CREATE TABLE IF NOT EXISTS Employee (
    emp_id       INTEGER PRIMARY KEY,         -- Unique Employee ID (manual)
    name         TEXT NOT NULL,               -- Full name of the employee
    department   TEXT NOT NULL,               -- Department (e.g., HR, IT)
    designation  TEXT NOT NULL,               -- Job title / role
    joining_date TEXT NOT NULL                -- Date the employee joined (YYYY-MM-DD format)
);

-- =============================================================================
-- TABLE 2: Salary
-- =============================================================================
CREATE TABLE IF NOT EXISTS Salary (
    salary_id    INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-generated
    emp_id       INTEGER NOT NULL,                  -- Foreign key → Employee
    basic_salary REAL NOT NULL DEFAULT 0.00,        -- Basic pay
    hra          REAL NOT NULL DEFAULT 0.00,        -- House Rent Allowance
    da           REAL NOT NULL DEFAULT 0.00,        -- Dearness Allowance
    FOREIGN KEY (emp_id) REFERENCES Employee(emp_id) ON DELETE CASCADE
);

-- =============================================================================
-- TABLE 3: Deductions
-- =============================================================================
CREATE TABLE IF NOT EXISTS Deductions (
    ded_id INTEGER PRIMARY KEY AUTOINCREMENT,       -- Auto-generated
    emp_id INTEGER NOT NULL,                        -- Foreign key → Employee
    tax    REAL NOT NULL DEFAULT 0.00,              -- Income Tax deduction
    pf     REAL NOT NULL DEFAULT 0.00,              -- Provident Fund deduction
    FOREIGN KEY (emp_id) REFERENCES Employee(emp_id) ON DELETE CASCADE
);

-- =============================================================================
-- TABLE 4: Payroll
-- Stores the computed payroll results.
-- =============================================================================
CREATE TABLE IF NOT EXISTS Payroll (
    payroll_id       INTEGER PRIMARY KEY AUTOINCREMENT, 
    emp_id           INTEGER NOT NULL,          
    gross_salary     REAL NOT NULL,          
    total_deductions REAL NOT NULL,          
    net_salary       REAL NOT NULL,          
    FOREIGN KEY (emp_id) REFERENCES Employee(emp_id) ON DELETE CASCADE
);
