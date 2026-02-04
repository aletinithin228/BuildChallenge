"""
Payroll Calculator Demo - Build Challenge Assignment 1

Demonstrates the payroll system with at least 6 employees covering
all employee types (FULL_TIME, PART_TIME, CONTRACTOR) and all
deduction combinations (health insurance, retirement, union dues).
"""

from employee import Employee, EmployeeType
from payroll_processor import PayrollProcessor


def print_payslip(payslip) -> None:
    """Print a formatted payslip for an employee."""
    print("\n" + "=" * 60)
    print(f"PAYSLIP - {payslip.employee.name} (ID: {payslip.employee.id})")
    print(f"Employee Type: {payslip.employee.employee_type.value}")
    print("-" * 60)
    print(f"  Gross Pay:                    ${payslip.gross_pay:>10.2f}")
    print(f"  Tax Withheld:                 ${payslip.tax_amount:>10.2f}")
    for name, amount in payslip.deductions.items():
        label = name.replace("_", " ").title()
        print(f"  {label + ':':<26} ${amount:>10.2f}")
    print("-" * 60)
    print(f"  NET PAY:                      ${payslip.net_pay:>10.2f}")
    print("=" * 60)


def main() -> None:
    """Run payroll demo with 6 employees covering all types and deduction combos."""
    processor = PayrollProcessor()

    # Create 6 employees covering all types and deduction combinations:
    # 1. FULL_TIME - no deductions
    # 2. FULL_TIME - health only (default)
    # 3. FULL_TIME - health + retirement + union (all deductions)
    # 4. PART_TIME - no deductions
    # 5. PART_TIME - retirement + union
    # 6. CONTRACTOR - union dues only

    employees = [
        Employee(101, "Alice Smith", EmployeeType.FULL_TIME, 3500.00, False, False),
        Employee(102, "Bob Johnson", EmployeeType.FULL_TIME, 4500.00, False, True),
        Employee(103, "Carol Williams", EmployeeType.FULL_TIME, 6000.00, True, True),
        Employee(104, "David Brown", EmployeeType.PART_TIME, 28.50, False, False),
        Employee(105, "Eva Martinez", EmployeeType.PART_TIME, 32.00, True, True),
        Employee(106, "Frank Chen", EmployeeType.CONTRACTOR, 250.00, True, False),
    ]

    # Hours/days for PART_TIME and CONTRACTOR
    hours_or_days = {
        101: 0,   # FULL_TIME - ignored
        102: 0,   # FULL_TIME - ignored
        103: 0,   # FULL_TIME - ignored
        104: 100, # PART_TIME - 100 hours
        105: 80,  # PART_TIME - 80 hours
        106: 18,  # CONTRACTOR - 18 days
    }

    print("\n" + "#" * 60)
    print("# MONTHLY PAYROLL PROCESSING")
    print("#" * 60)

    payslips = processor.process_monthly_payroll(employees, hours_or_days)

    for payslip in payslips:
        print_payslip(payslip)

    # Summary
    total_gross = sum(ps.gross_pay for ps in payslips)
    total_tax = sum(ps.tax_amount for ps in payslips)
    total_net = sum(ps.net_pay for ps in payslips)

    print("\n" + "#" * 60)
    print("# PAYROLL SUMMARY")
    print("#" * 60)
    print(f"  Total Gross Payroll:     ${total_gross:>10.2f}")
    print(f"  Total Tax Withheld:      ${total_tax:>10.2f}")
    print(f"  Total Net Payroll:       ${total_net:>10.2f}")
    print("#" * 60 + "\n")


if __name__ == "__main__":
    main()
