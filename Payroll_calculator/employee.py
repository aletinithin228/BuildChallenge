"""
Employee module for the payroll calculator system.

Contains the Employee class and EmployeeType enum for representing
employees with different compensation structures.
"""

from enum import Enum
from decimal import Decimal
from typing import Union


class EmployeeType(Enum):
    """Enum representing the three types of employees in the payroll system."""

    FULL_TIME = "FULL_TIME"  # Fixed monthly salary
    PART_TIME = "PART_TIME"  # Hourly rate × hours worked (max 120 hours/month)
    CONTRACTOR = "CONTRACTOR"  # Daily rate × days worked


class Employee:
    """
    Represents an employee in the payroll system.

    Attributes:
        id: Unique identifier for the employee
        name: Full name of the employee
        employee_type: Type of employment (FULL_TIME, PART_TIME, or CONTRACTOR)
        pay_rate: Monthly salary (FULL_TIME), hourly rate (PART_TIME), or daily rate (CONTRACTOR)
        is_union_member: Whether the employee pays union dues ($50 flat)
        has_retirement: Whether the employee contributes to retirement (5% of gross)
    """

    # Constants for validation
    MAX_PART_TIME_HOURS = 120

    def __init__(
        self,
        id: Union[str, int],
        name: str,
        employee_type: EmployeeType,
        pay_rate: Union[float, Decimal],
        is_union_member: bool = False,
        has_retirement: bool = False,
    ) -> None:
        """
        Initialize an Employee.

        Args:
            id: Unique employee identifier
            name: Employee's full name
            employee_type: Type of employment
            pay_rate: Compensation rate based on employee type
            is_union_member: Whether employee pays union dues
            has_retirement: Whether employee has retirement contribution
        """
        self.id = id
        self.name = name
        self.employee_type = employee_type
        self.pay_rate = Decimal(str(pay_rate))
        self.is_union_member = is_union_member
        self.has_retirement = has_retirement

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"Employee(id={self.id!r}, name={self.name!r}, "
            f"type={self.employee_type.value}, pay_rate={self.pay_rate})"
        )
