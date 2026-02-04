"""
PayrollProcessor module for the payroll calculator system.

Handles all payroll calculations including gross pay, taxes, deductions,
and generates payslips for employees.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Union

from employee import Employee, EmployeeType
from payslip import PaySlip


# Tax bracket constants (progressive tax)
TAX_BRACKET_1_MAX = Decimal("1000")   # 0% for first $1000
TAX_BRACKET_2_MAX = Decimal("3000")   # 10% for $1001-$3000
TAX_BRACKET_3_MAX = Decimal("5000")   # 20% for $3001-$5000
# 30% above $5000

# Deduction constants
HEALTH_INSURANCE = Decimal("150")   # Flat, FULL_TIME only
RETIREMENT_RATE = Decimal("0.05")   # 5% of gross
UNION_DUES = Decimal("50")          # Flat, if union member


class PayrollProcessor:
    """
    Processes payroll for employees with various types and deduction rules.

    Provides methods to calculate gross pay, taxes, deductions, and
    generate complete payslips. All currency values are rounded to 2 decimal places.
    """

    @staticmethod
    def _round_currency(value: Union[Decimal, float]) -> Decimal:
        """Round currency to 2 decimal places."""
        return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def calculate_gross_pay(
        self, employee: Employee, hours_or_days: Union[float, Decimal, int]
    ) -> Decimal:
        """
        Calculate gross pay for an employee based on their type.

        Args:
            employee: The employee to calculate for
            hours_or_days: Hours worked (PART_TIME) or days worked (CONTRACTOR).
                          Ignored for FULL_TIME (uses fixed salary).

        Returns:
            Gross pay amount, rounded to 2 decimal places

        Raises:
            ValueError: If PART_TIME hours exceed 120
        """
        hours_or_days = Decimal(str(hours_or_days))
        pay_rate = employee.pay_rate

        if employee.employee_type == EmployeeType.FULL_TIME:
            gross = pay_rate

        elif employee.employee_type == EmployeeType.PART_TIME:
            if hours_or_days > Employee.MAX_PART_TIME_HOURS:
                raise ValueError(
                    f"PART_TIME employees cannot exceed {Employee.MAX_PART_TIME_HOURS} hours/month"
                )
            gross = pay_rate * hours_or_days

        elif employee.employee_type == EmployeeType.CONTRACTOR:
            gross = pay_rate * hours_or_days

        else:
            raise ValueError(f"Unknown employee type: {employee.employee_type}")

        return self._round_currency(gross)

    def calculate_tax(self, gross_pay: Union[Decimal, float]) -> Decimal:
        """
        Calculate tax using progressive tax brackets.

        Tax brackets:
        - 0% for first $1000
        - 10% for $1001-$3000
        - 20% for $3001-$5000
        - 30% above $5000

        Args:
            gross_pay: Gross salary amount

        Returns:
            Tax amount, rounded to 2 decimal places
        """
        gross = Decimal(str(gross_pay))
        tax = Decimal("0")

        if gross <= TAX_BRACKET_1_MAX:
            tax = Decimal("0")
        elif gross <= TAX_BRACKET_2_MAX:
            tax = (gross - TAX_BRACKET_1_MAX) * Decimal("0.10")
        elif gross <= TAX_BRACKET_3_MAX:
            tax = (TAX_BRACKET_2_MAX - TAX_BRACKET_1_MAX) * Decimal("0.10")
            tax += (gross - TAX_BRACKET_2_MAX) * Decimal("0.20")
        else:
            tax = (TAX_BRACKET_2_MAX - TAX_BRACKET_1_MAX) * Decimal("0.10")
            tax += (TAX_BRACKET_3_MAX - TAX_BRACKET_2_MAX) * Decimal("0.20")
            tax += (gross - TAX_BRACKET_3_MAX) * Decimal("0.30")

        return self._round_currency(tax)

    def calculate_deductions(
        self, employee: Employee, gross_pay: Union[Decimal, float]
    ) -> Dict[str, Decimal]:
        """
        Calculate all applicable deductions for an employee.

        Deductions:
        - Health insurance: $150 flat (FULL_TIME only)
        - Retirement: 5% of gross (if has_retirement flag)
        - Union dues: $50 flat (if union member)

        Args:
            employee: The employee to calculate deductions for
            gross_pay: Gross salary amount

        Returns:
            Dictionary mapping deduction names to amounts
        """
        deductions: Dict[str, Decimal] = {}
        gross = Decimal(str(gross_pay))

        # Health insurance - FULL_TIME only
        if employee.employee_type == EmployeeType.FULL_TIME:
            deductions["health_insurance"] = HEALTH_INSURANCE

        # Retirement contribution - 5% of gross if opted in
        if employee.has_retirement:
            deductions["retirement"] = self._round_currency(gross * RETIREMENT_RATE)

        # Union dues - if union member
        if employee.is_union_member:
            deductions["union_dues"] = UNION_DUES

        return deductions

    def generate_pay_slip(
        self, employee: Employee, hours_or_days: Union[float, Decimal, int] = 0
    ) -> PaySlip:
        """
        Generate a complete payslip for an employee.

        Args:
            employee: The employee to generate payslip for
            hours_or_days: Hours (PART_TIME) or days (CONTRACTOR). Use 0 for FULL_TIME.

        Returns:
            Complete PaySlip with all calculations
        """
        gross_pay = self.calculate_gross_pay(employee, hours_or_days)
        tax_amount = self.calculate_tax(gross_pay)
        deductions = self.calculate_deductions(employee, gross_pay)
        total_deductions = sum(deductions.values())
        net_pay = self._round_currency(gross_pay - tax_amount - total_deductions)

        return PaySlip(
            employee=employee,
            gross_pay=gross_pay,
            tax_amount=tax_amount,
            deductions=deductions,
            net_pay=net_pay,
        )

    def process_monthly_payroll(
        self,
        employee_list: List[Employee],
        hours_or_days_map: Dict[Union[str, int], Union[float, Decimal, int]] = None,
    ) -> List[PaySlip]:
        """
        Process payroll for a list of employees.

        Args:
            employee_list: List of employees to process
            hours_or_days_map: Optional dict mapping employee id to hours/days.
                             Defaults to 0 for FULL_TIME, 80 for PART_TIME, 20 for CONTRACTOR.

        Returns:
            List of PaySlips for each employee
        """
        if hours_or_days_map is None:
            hours_or_days_map = {}

        payslips: List[PaySlip] = []

        for employee in employee_list:
            # Default hours/days based on employee type if not in map
            if employee.id in hours_or_days_map:
                h_or_d = hours_or_days_map[employee.id]
            elif employee.employee_type == EmployeeType.PART_TIME:
                h_or_d = 80  # Default 80 hours
            elif employee.employee_type == EmployeeType.CONTRACTOR:
                h_or_d = 20  # Default 20 days
            else:
                h_or_d = 0  # FULL_TIME doesn't use this

            payslip = self.generate_pay_slip(employee, h_or_d)
            payslips.append(payslip)

        return payslips
