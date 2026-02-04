# Payroll Calculator - Build Challenge Assignment 1

An employee payroll calculator with tax and deduction rules, implemented in Python with object-oriented design.

## Requirements Coverage

- **Object-oriented design**: `Employee`, `PaySlip`, and `PayrollProcessor` classes
- **Arithmetic with precision**: Uses `Decimal` for currency calculations
- **Conditional business logic**: Tax brackets, deduction rules
- **Enum usage**: `EmployeeType` enum for FULL_TIME, PART_TIME, CONTRACTOR

## Employee Types

| Type | Pay Formula |
|------|-------------|
| FULL_TIME | Fixed monthly salary |
| PART_TIME | Hourly rate × hours worked (max 120 hrs/month) |
| CONTRACTOR | Daily rate × days worked |

## Tax Brackets (Progressive)

| Gross Salary | Tax Rate |
|--------------|----------|
| $0 - $1,000 | 0% |
| $1,001 - $3,000 | 10% |
| $3,001 - $5,000 | 20% |
| Above $5,000 | 30% |

## Deductions

- **Health Insurance**: $150 flat (FULL_TIME only)
- **Retirement**: 5% of gross (optional per employee)
- **Union Dues**: $50 flat (if union member)

## Project Structure

```
payroll_calculator/
├── employee.py          # Employee class and EmployeeType enum
├── payslip.py           # PaySlip class
├── payroll_processor.py # PayrollProcessor with all calculation logic
├── test_payroll.py      # Comprehensive unit tests
├── main.py              # Demo with 6 employees
├── requirements.txt     # Dependencies (standard library only)
└── README.md            # This file
```

## Usage

### Run Demo (6 employees, all types and deduction combos)

```bash
cd payroll_calculator
python3 main.py
```

### Run Tests

```bash
cd payroll_calculator
python3 -m unittest test_payroll -v
```

### Programmatic Usage

```python
from employee import Employee, EmployeeType
from payroll_processor import PayrollProcessor

processor = PayrollProcessor()
emp = Employee(1, "John Doe", EmployeeType.FULL_TIME, 5000, True, True)
payslip = processor.generate_pay_slip(emp, 0)
print(f"Net Pay: ${payslip.net_pay}")
```

## Running Tests

```bash
python -m unittest discover -v
```


