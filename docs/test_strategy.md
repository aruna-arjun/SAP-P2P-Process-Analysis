# Test Strategy

## Objective
Validate the main procurement workflow and its data checks.

## Test levels
- Functional testing: create orders, record receipts, enter invoices.
- Data validation: required fields, positive quantities, unique identifiers, and foreign keys.
- Integration-style workflow testing: use the same purchase order across goods receipt and invoice verification.
- Negative testing: mismatched quantities, mismatched amounts, duplicate invoice identifiers.

## Entry criteria
Database initialized with sample records.

## Exit criteria
All high-priority test cases pass and known limitations are documented.

## Defect template
- Defect ID:
- Summary:
- Preconditions:
- Steps to reproduce:
- Expected result:
- Actual result:
- Severity:
- Status:
