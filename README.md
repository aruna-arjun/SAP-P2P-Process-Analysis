# SAP P2P Process Analysis – Educational Simulation

**Author:** Aruna Arjun  
**Technologies:** Python, Streamlit, SQLite, SQL, Pandas  
**Domain:** ERP concepts, procurement, Procure-to-Pay (P2P), functional testing

> **Important:** This is an independent educational simulation inspired by common procure-to-pay concepts. It is not an SAP implementation, does not connect to SAP S/4HANA or SAP HANA, and is not affiliated with or certified by SAP or PwC.

## 1. Project overview

This project demonstrates a simplified procurement workflow:
1. Maintain supplier and material records.
2. Create purchase orders.
3. Record partial or complete goods receipts.
4. Record supplier invoices.
5. Run simplified three-way matching checks.
6. Review procurement data and exceptions.

The three-way match compares the purchase order, goods receipt, and supplier invoice. In this simulation, an invoice is approved only when the invoiced quantity does not exceed the ordered or received quantity and the invoice amount equals invoiced quantity multiplied by the purchase-order unit price.

Real ERP invoice verification can include configurable tolerances, taxes, freight, delivery costs, account assignment, approvals, and other controls not represented here.

## 2. Tools to install

- Python 3.11 or newer: https://www.python.org/downloads/
- Visual Studio Code: https://code.visualstudio.com/
- Git: https://git-scm.com/downloads/
- GitHub account: https://github.com/

No SAP license or SAP system access is required to run this simulation.

## 3. Installation

### Windows

1. Download and install Python 3.11+.
2. During installation, select **Add Python to PATH**.
3. Install VS Code and Git.
4. Download or clone this repository.
5. Open the project folder in VS Code.
6. Open Terminal → New Terminal.

Check installations:

```bash
python --version
git --version
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Initialize the database and sample data:

```bash
python database/init_db.py
```

Run the application:

```bash
streamlit run app.py
```

Streamlit normally opens the application in your browser at:

```text
http://localhost:8501
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python database/init_db.py
streamlit run app.py
```

## 4. Suggested demo workflow

The database starts with sample records, including a deliberately blocked invoice.

1. Open **Overview** and review the seeded purchase orders.
2. Open **Purchase Orders** and create a new order.
3. Open **Goods Receipts** and record a partial or complete delivery.
4. Open **Invoice Verification** and enter an invoice.
5. Try an invoice quantity greater than the received quantity. It should be blocked.
6. Try a matching quantity and amount. It should pass the simplified checks.
7. Open **SQL Explorer** and run the example SELECT queries.

## 5. Project structure

```text
SAP-P2P-Process-Analysis/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── database/
│   ├── schema.sql
│   ├── seed.sql
│   └── init_db.py
├── sql/
│   └── analysis_queries.sql
├── test-cases/
│   └── test_cases.csv
├── docs/
│   ├── business_process.md
│   └── test_strategy.md
└── data/
    └── p2p.db  (created locally; ignored by Git)
```

## 6. Database entities

- `suppliers`: supplier master data.
- `materials`: material master data.
- `purchase_orders`: order header and item information in a simplified single-table design.
- `goods_receipts`: quantities received against purchase orders.
- `invoices`: supplier invoice records and simulated verification status.

The schema uses primary keys, foreign keys, unique identifiers, and basic check constraints.

## 7. Testing

Use `test-cases/test_cases.csv` as the functional test checklist. Record actual results and pass/fail status in your own test execution log. The CSV contains expected outcomes; it is not evidence that tests have already been executed.

## 8. SQL practice

Open `sql/analysis_queries.sql` and practice:
- JOIN
- GROUP BY
- SUM
- COALESCE
- ORDER BY
- HAVING

The Streamlit SQL Explorer accepts read-only SELECT queries.

## 9. GitHub publishing

From the project root:

```bash
git init
git add .
git commit -m "Initial P2P procurement simulation"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/SAP-P2P-Process-Analysis.git
git push -u origin main
```

Create an empty public repository on GitHub with the name `SAP-P2P-Process-Analysis` before adding the remote. Replace `YOUR-USERNAME` with your GitHub username. Do not commit passwords, access tokens, virtual environments, or your local database file.

## 10. Resume wording

Only after you have started the work, you may describe it as:

**Procure-to-Pay (P2P) Process Analysis & Testing – Educational Project (In Progress)**  
Technologies: Python, SQLite, SQL, Streamlit, Excel

- Developed an educational procurement workflow simulation covering purchase orders, goods receipts, supplier invoices, and simplified three-way matching.
- Designed a relational database using primary keys, foreign keys, and validation constraints to manage supplier, material, order, receipt, and invoice records.
- Prepared functional test scenarios for partial deliveries, invoice quantity mismatches, amount discrepancies, and duplicate invoice identifiers.

After completing and testing the project, update the wording to reflect the features you actually implemented and validated.

## 11. Learning extensions

- Study SAP MM procurement concepts and map the simulation's steps to the relevant SAP process.
- Learn SAP HANA SQL syntax and database concepts separately.
- If eligible, explore SAP's official learning journeys and available practice systems.
- Extend the project with approval workflows, taxes, delivery costs, and a separate payment-status process.

## 12. Disclaimer

This portfolio project is a learning exercise using generic ERP concepts. It does not demonstrate hands-on SAP configuration, SAP implementation, or SAP HANA system administration.
