# Project Scope and Requirements

## Business problem
A company needs a simple way to track supplier orders, received quantities, and supplier invoices so that discrepancies can be identified before invoice approval.

## Users
- Procurement coordinator
- Warehouse / receiving user
- Accounts payable reviewer

## Functional requirements
- FR01: Display supplier and material master data.
- FR02: Add supplier and material records.
- FR03: Create a purchase order for a supplier and material.
- FR04: Record goods receipts against an order without exceeding the remaining order quantity.
- FR05: Record an invoice against a purchase order.
- FR06: Block an invoice when invoiced quantity exceeds ordered or received quantity.
- FR07: Block an invoice when the amount does not match the simplified expected amount.
- FR08: Display order, receipt, and invoice information.
- FR09: Run read-only SQL reports.

## Non-functional requirements
- NFR01: Store data in a relational database.
- NFR02: Use database constraints for basic data integrity.
- NFR03: Provide a browser-based user interface.
- NFR04: Document setup, workflow, and test scenarios.

## Out of scope
Live SAP connectivity, SAP configuration, SAP authorization roles, real accounting postings, tax calculations, payment gateway integration, and production-grade security.
