# P2P Business Process

## Objective
Demonstrate an educational procure-to-pay workflow from purchase order through goods receipt and invoice verification.

## Scope
- Supplier and material master data
- Purchase order creation
- Goods receipt recording
- Invoice recording and simplified three-way matching
- Procurement reporting

## Process
1. A business department identifies a need. In a full ERP process, an internal purchase requisition may be created and approved.
2. Procurement creates a purchase order for a supplier.
3. The receiving team records the actual quantity delivered in a goods receipt.
4. Accounts payable records the supplier invoice.
5. Invoice verification compares purchase order, goods receipt, and invoice information.
6. An invoice that passes the simulation's checks is marked APPROVED; otherwise it is BLOCKED for review.

## Three-way match
The project compares:
- Purchase order: what was ordered and at what price.
- Goods receipt: what quantity was received.
- Supplier invoice: what quantity and amount the supplier billed.

## Important limitation
This application is a self-contained learning simulation. It does not connect to SAP, execute SAP transactions, post accounting documents, or reproduce all SAP configuration, tolerances, tax, freight, approval, and payment controls.
