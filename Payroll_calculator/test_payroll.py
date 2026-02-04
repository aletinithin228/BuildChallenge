"""
Comprehensive unit tests for the payroll calculator system.

Tests cover:
- Employee class and EmployeeType enum
- PayrollProcessor: calculateGrossPay, calculateTax, calculateDeductions
- PaySlip generation and processMonthlyPayroll
"""

import unittest
from decimal import Decimal

from employee import Employee, EmployeeType
from payslip import PaySlip
from payroll_processor import PayrollProcessor


class TestEmployee(unittest.TestCase):
    """Unit tests for the Employee class."""

    def test_employee_creation_full_time(self):
        """Test creating a FULL_TIME employee."""
        emp = Employee(1, "Alice Smith", EmployeeType.FULL_TIME, 5000, False, False)
        self.assertEqual(emp.id, 1)
        self.assertEqual(emp.name, "Alice Smith")
        self.assertEqual(emp.employee_type, EmployeeType.FULL_TIME)
        self.assertEqual(emp.pay_rate, Decimal("5000"))
        self.assertFalse(emp.is_union_member)
        self.assertFalse(emp.has_retirement)

    def test_employee_creation_with_deductions(self):
        """Test creating employee with union and retirement flags."""
        emp = Employee(2, "Bob Jones", EmployeeType.PART_TIME, 25.50, True, True)
        self.assertTrue(emp.is_union_member)
        self.assertTrue(emp.has_retirement)

    def test_employee_type_enum_values(self):
        """Test EmployeeType enum has correct values."""
        self.assertEqual(EmployeeType.FULL_TIME.value, "FULL_TIME")
        self.assertEqual(EmployeeType.PART_TIME.value, "PART_TIME")
        self.assertEqual(EmployeeType.CONTRACTOR.value, "CONTRACTOR")


class TestPayrollProcessorGrossPay(unittest.TestCase):
    """Unit tests for calculateGrossPay method."""

    def setUp(self):
        self.processor = PayrollProcessor()

    def test_full_time_gross_pay(self):
        """FULL_TIME: gross = fixed monthly salary."""
        emp = Employee(1, "Alice", EmployeeType.FULL_TIME, 4500, False, False)
        gross = self.processor.calculate_gross_pay(emp, 0)
        self.assertEqual(gross, Decimal("4500.00"))

    def test_part_time_gross_pay(self):
        """PART_TIME: gross = hourly rate × hours worked."""
        emp = Employee(2, "Bob", EmployeeType.PART_TIME, 25.00, False, False)
        gross = self.processor.calculate_gross_pay(emp, 80)
        self.assertEqual(gross, Decimal("2000.00"))

    def test_part_time_max_hours(self):
        """PART_TIME: max 120 hours."""
        emp = Employee(3, "Carol", EmployeeType.PART_TIME, 30.00, False, False)
        gross = self.processor.calculate_gross_pay(emp, 120)
        self.assertEqual(gross, Decimal("3600.00"))

    def test_part_time_exceeds_max_hours_raises(self):
        """PART_TIME: exceeding 120 hours raises ValueError."""
        emp = Employee(4, "Dave", EmployeeType.PART_TIME, 25.00, False, False)
        with self.assertRaises(ValueError) as context:
            self.processor.calculate_gross_pay(emp, 121)
        self.assertIn("120", str(context.exception))

    def test_contractor_gross_pay(self):
        """CONTRACTOR: gross = daily rate × days worked."""
        emp = Employee(5, "Eve", EmployeeType.CONTRACTOR, 200.00, False, False)
        gross = self.processor.calculate_gross_pay(emp, 15)
        self.assertEqual(gross, Decimal("3000.00"))

    def test_currency_rounding(self):
        """Gross pay rounds to 2 decimal places."""
        emp = Employee(6, "Frank", EmployeeType.PART_TIME, 33.33, False, False)
        gross = self.processor.calculate_gross_pay(emp, 10)
        self.assertEqual(gross, Decimal("333.30"))


class TestPayrollProcessorTax(unittest.TestCase):
    """Unit tests for calculateTax method."""

    def setUp(self):
        self.processor = PayrollProcessor()

    def test_tax_bracket_1_zero_tax(self):
        """0% tax for first $1000."""
        tax = self.processor.calculate_tax(1000)
        self.assertEqual(tax, Decimal("0.00"))

    def test_tax_bracket_1_partial(self):
        """0% tax for amounts under $1000."""
        tax = self.processor.calculate_tax(500)
        self.assertEqual(tax, Decimal("0.00"))

    def test_tax_bracket_2(self):
        """10% for $1001-$3000."""
        tax = self.processor.calculate_tax(2000)
        # (2000 - 1000) * 0.10 = 100
        self.assertEqual(tax, Decimal("100.00"))

    def test_tax_bracket_2_boundary(self):
        """10% at $3000 boundary."""
        tax = self.processor.calculate_tax(3000)
        # (3000 - 1000) * 0.10 = 200
        self.assertEqual(tax, Decimal("200.00"))

    def test_tax_bracket_3(self):
        """20% for $3001-$5000."""
        tax = self.processor.calculate_tax(4000)
        # 200 + (4000 - 3000) * 0.20 = 200 + 200 = 400
        self.assertEqual(tax, Decimal("400.00"))

    def test_tax_bracket_3_boundary(self):
        """20% at $5000 boundary."""
        tax = self.processor.calculate_tax(5000)
        # 200 + (5000 - 3000) * 0.20 = 200 + 400 = 600
        self.assertEqual(tax, Decimal("600.00"))

    def test_tax_bracket_4(self):
        """30% above $5000."""
        tax = self.processor.calculate_tax(6000)
        # 600 + (6000 - 5000) * 0.30 = 600 + 300 = 900
        self.assertEqual(tax, Decimal("900.00"))

    def test_tax_rounding(self):
        """Tax rounds to 2 decimal places."""
        tax = self.processor.calculate_tax(1555.55)
        # (1555.55 - 1000) * 0.10 = 55.555 -> 55.56
        self.assertEqual(tax, Decimal("55.56"))


class TestPayrollProcessorDeductions(unittest.TestCase):
    """Unit tests for calculateDeductions method."""

    def setUp(self):
        self.processor = PayrollProcessor()

    def test_health_insurance_full_time_only(self):
        """Health insurance $150 for FULL_TIME only."""
        emp = Employee(1, "Alice", EmployeeType.FULL_TIME, 4000, False, False)
        ded = self.processor.calculate_deductions(emp, 4000)
        self.assertIn("health_insurance", ded)
        self.assertEqual(ded["health_insurance"], Decimal("150"))

    def test_no_health_insurance_part_time(self):
        """No health insurance for PART_TIME."""
        emp = Employee(2, "Bob", EmployeeType.PART_TIME, 25, False, False)
        ded = self.processor.calculate_deductions(emp, 2000)
        self.assertNotIn("health_insurance", ded)

    def test_no_health_insurance_contractor(self):
        """No health insurance for CONTRACTOR."""
        emp = Employee(3, "Carol", EmployeeType.CONTRACTOR, 200, False, False)
        ded = self.processor.calculate_deductions(emp, 3000)
        self.assertNotIn("health_insurance", ded)

    def test_retirement_contribution(self):
        """Retirement: 5% of gross when has_retirement."""
        emp = Employee(4, "Dave", EmployeeType.PART_TIME, 25, False, True)
        ded = self.processor.calculate_deductions(emp, 2000)
        self.assertIn("retirement", ded)
        self.assertEqual(ded["retirement"], Decimal("100.00"))

    def test_no_retirement_when_not_opted_in(self):
        """No retirement when has_retirement is False."""
        emp = Employee(5, "Eve", EmployeeType.FULL_TIME, 5000, False, False)
        ded = self.processor.calculate_deductions(emp, 5000)
        self.assertNotIn("retirement", ded)

    def test_union_dues(self):
        """Union dues $50 when is_union_member."""
        emp = Employee(6, "Frank", EmployeeType.FULL_TIME, 4000, True, False)
        ded = self.processor.calculate_deductions(emp, 4000)
        self.assertIn("union_dues", ded)
        self.assertEqual(ded["union_dues"], Decimal("50"))

    def test_no_union_dues_when_not_member(self):
        """No union dues when not union member."""
        emp = Employee(7, "Grace", EmployeeType.FULL_TIME, 4000, False, False)
        ded = self.processor.calculate_deductions(emp, 4000)
        self.assertNotIn("union_dues", ded)

    def test_all_deductions_combined(self):
        """FULL_TIME with health, retirement, and union."""
        emp = Employee(8, "Henry", EmployeeType.FULL_TIME, 6000, True, True)
        ded = self.processor.calculate_deductions(emp, 6000)
        self.assertEqual(ded["health_insurance"], Decimal("150"))
        self.assertEqual(ded["retirement"], Decimal("300.00"))  # 5% of 6000
        self.assertEqual(ded["union_dues"], Decimal("50"))


class TestGeneratePaySlip(unittest.TestCase):
    """Unit tests for generatePaySlip method."""

    def setUp(self):
        self.processor = PayrollProcessor()

    def test_payslip_structure(self):
        """PaySlip contains all required fields."""
        emp = Employee(1, "Alice", EmployeeType.FULL_TIME, 4000, False, False)
        ps = self.processor.generate_pay_slip(emp, 0)
        self.assertIsInstance(ps, PaySlip)
        self.assertEqual(ps.employee, emp)
        self.assertIsInstance(ps.gross_pay, Decimal)
        self.assertIsInstance(ps.tax_amount, Decimal)
        self.assertIsInstance(ps.deductions, dict)
        self.assertIsInstance(ps.net_pay, Decimal)

    def test_net_pay_calculation(self):
        """Net pay = gross - tax - total deductions."""
        emp = Employee(2, "Bob", EmployeeType.FULL_TIME, 4000, False, False)
        ps = self.processor.generate_pay_slip(emp, 0)
        # Gross 4000, tax = (4000-3000)*0.2 + 200 = 400, health = 150
        # Net = 4000 - 400 - 150 = 3450
        expected_net = Decimal("3450.00")
        self.assertEqual(ps.net_pay, expected_net)
        self.assertEqual(ps.gross_pay - ps.tax_amount - ps.total_deductions(), ps.net_pay)


class TestProcessMonthlyPayroll(unittest.TestCase):
    """Unit tests for processMonthlyPayroll method."""

    def setUp(self):
        self.processor = PayrollProcessor()

    def test_process_multiple_employees(self):
        """Process payroll for multiple employees."""
        employees = [
            Employee(1, "Alice", EmployeeType.FULL_TIME, 4000, False, False),
            Employee(2, "Bob", EmployeeType.PART_TIME, 25, False, False),
            Employee(3, "Carol", EmployeeType.CONTRACTOR, 200, False, False),
        ]
        hours_map = {2: 80, 3: 20}
        payslips = self.processor.process_monthly_payroll(employees, hours_map)
        self.assertEqual(len(payslips), 3)
        self.assertEqual(payslips[0].employee.name, "Alice")
        self.assertEqual(payslips[1].gross_pay, Decimal("2000.00"))
        self.assertEqual(payslips[2].gross_pay, Decimal("4000.00"))

    def test_process_with_default_hours(self):
        """Uses default hours/days when map not provided."""
        employees = [
            Employee(1, "Alice", EmployeeType.FULL_TIME, 4000, False, False),
            Employee(2, "Bob", EmployeeType.PART_TIME, 25, False, False),
        ]
        payslips = self.processor.process_monthly_payroll(employees)
        self.assertEqual(payslips[0].gross_pay, Decimal("4000.00"))
        self.assertEqual(payslips[1].gross_pay, Decimal("2000.00"))  # 80 * 25 default


if __name__ == "__main__":
    unittest.main(verbosity=2)
