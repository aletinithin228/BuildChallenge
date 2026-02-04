"""
PaySlip module for the payroll calculator system.

Contains the PaySlip class that holds calculated payroll information
for an employee including gross pay, taxes, deductions, and net pay.
"""

from decimal import Decimal
from typing import Dict

from employee import Employee


class PaySlip:
    """
    Represents a payslip with calculated payroll details for an employee.

    Attributes:
        employee: The employee this payslip belongs to
        gross_pay: Total earnings before taxes and deductions
        tax_amount: Total tax withheld based on tax brackets
        deductions: Dictionary mapping deduction names to amounts
        net_pay: Take-home pay after taxes and deductions
    """

    def __init__(
        self,
        employee: Employee,
        gross_pay: Decimal,
        tax_amount: Decimal,
        deductions: Dict[str, Decimal],
        net_pay: Decimal,
    ) -> None:
        """
        Initialize a PaySlip.

        Args:
            employee: The employee for this payslip
            gross_pay: Pre-tax earnings
            tax_amount: Tax withheld
            deductions: Map of deduction name to amount
            net_pay: Final take-home amount
        """
        self.employee = employee
        self.gross_pay = gross_pay
        self.tax_amount = tax_amount
        self.deductions = deductions
        self.net_pay = net_pay

    def total_deductions(self) -> Decimal:
        """Return the sum of all deductions."""
        return sum(self.deductions.values())

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"PaySlip(employee={self.employee.name}, gross={self.gross_pay}, "
            f"tax={self.tax_amount}, net={self.net_pay})"
        )
