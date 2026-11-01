from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st

ROOT = Path(__file__).parent
DB_PATH = ROOT / "data" / "p2p.db"

st.set_page_config(page_title="P2P Procurement Workbench", page_icon="📦", layout="wide")

def connect():
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)

def query(sql, params=()):
    with connect() as con:
        return pd.read_sql_query(sql, con, params=params)

def execute(sql, params=()):
    with connect() as con:
        cur = con.execute(sql, params)
        con.commit()
        return cur.lastrowid

def money(value):
    return f"₹{value:,.2f}"

st.title("📦 Procure-to-Pay (P2P) Workbench")
st.caption("Educational procurement-process simulation | SQLite + Python + Streamlit")
st.info("Learning project only: this is a simulated workflow, not a live SAP system or SAP implementation.")

# Sidebar
page = st.sidebar.radio("Navigate", ["Overview", "Suppliers & Materials", "Purchase Orders", "Goods Receipts", "Invoice Verification", "SQL Explorer"])
st.sidebar.markdown("---")
st.sidebar.caption("Process: Purchase Order → Goods Receipt → Invoice Verification → Payment status")

if page == "Overview":
    st.subheader("Procurement overview")
    po = query("SELECT COUNT(*) AS n, COALESCE(SUM(quantity * unit_price),0) AS value FROM purchase_orders")
    gr = query("SELECT COALESCE(SUM(quantity_received),0) AS qty FROM goods_receipts")
    inv = query("SELECT COUNT(*) AS n FROM invoices")
    pending = query("SELECT COUNT(*) AS n FROM invoices WHERE status != 'APPROVED'")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Purchase orders", int(po.loc[0,"n"]))
    c2.metric("Ordered value", money(float(po.loc[0,"value"])))
    c3.metric("Units received", int(gr.loc[0,"qty"]))
    c4.metric("Invoices to review", int(pending.loc[0,"n"]))

    st.markdown("### Purchase order register")
    st.dataframe(query("""
        SELECT po.po_number, s.supplier_name, m.material_name, po.quantity,
               po.unit_price, po.quantity * po.unit_price AS order_value, po.status
        FROM purchase_orders po
        JOIN suppliers s ON s.supplier_id=po.supplier_id
        JOIN materials m ON m.material_id=po.material_id
        ORDER BY po.po_id DESC
    """), use_container_width=True, hide_index=True)

    st.markdown("### Invoice matching exceptions")
    exceptions = query("""
        SELECT i.invoice_number, po.po_number, s.supplier_name,
               po.quantity AS ordered_qty,
               COALESCE(SUM(gr.quantity_received),0) AS received_qty,
               i.quantity_invoiced,
               i.amount AS invoice_amount,
               CASE
                 WHEN i.quantity_invoiced > COALESCE(SUM(gr.quantity_received),0)
                   THEN 'Invoice quantity exceeds received quantity'
                 WHEN i.quantity_invoiced > po.quantity
                   THEN 'Invoice quantity exceeds ordered quantity'
                 ELSE 'Review price / quantity'
               END AS exception
        FROM invoices i
        JOIN purchase_orders po ON po.po_id=i.po_id
        JOIN suppliers s ON s.supplier_id=po.supplier_id
        LEFT JOIN goods_receipts gr ON gr.po_id=po.po_id
        WHERE i.status != 'APPROVED'
        GROUP BY i.invoice_id
    """)
    if exceptions.empty:
        st.success("No pending invoice exceptions.")
    else:
        st.dataframe(exceptions, use_container_width=True, hide_index=True)

elif page == "Suppliers & Materials":
    st.subheader("Master data")
    left,right = st.columns(2)
    with left:
        st.markdown("#### Suppliers")
        st.dataframe(query("SELECT supplier_id, supplier_name, city, email FROM suppliers"), use_container_width=True, hide_index=True)
        with st.form("supplier_form"):
            name = st.text_input("Supplier name")
            city = st.text_input("City")
            email = st.text_input("Email")
            submitted = st.form_submit_button("Add supplier")
            if submitted:
                if name.strip():
                    execute("INSERT INTO suppliers(supplier_name,city,email) VALUES(?,?,?)",(name.strip(),city.strip(),email.strip()))
                    st.success("Supplier added. Refresh the page to see it.")
                else:
                    st.error("Supplier name is required.")
    with right:
        st.markdown("#### Materials")
        st.dataframe(query("SELECT material_id, material_code, material_name, unit FROM materials"), use_container_width=True, hide_index=True)
        with st.form("material_form"):
            code = st.text_input("Material code")
            material = st.text_input("Material name")
            unit = st.selectbox("Unit", ["EA", "KG", "BOX", "L"])
            submitted2 = st.form_submit_button("Add material")
            if submitted2:
                if code.strip() and material.strip():
                    try:
                        execute("INSERT INTO materials(material_code,material_name,unit) VALUES(?,?,?)",(code.strip().upper(),material.strip(),unit))
                        st.success("Material added. Refresh the page to see it.")
                    except sqlite3.IntegrityError:
                        st.error("That material code already exists.")
                else:
                    st.error("Material code and name are required.")

elif page == "Purchase Orders":
    st.subheader("Create purchase order")
    suppliers = query("SELECT supplier_id, supplier_name FROM suppliers ORDER BY supplier_name")
    materials = query("SELECT material_id, material_name FROM materials ORDER BY material_name")
    if suppliers.empty or materials.empty:
        st.warning("Add at least one supplier and one material first.")
    else:
        with st.form("po_form"):
            supplier_map = dict(zip(suppliers.supplier_name, suppliers.supplier_id))
            material_map = dict(zip(materials.material_name, materials.material_id))
            supplier_name = st.selectbox("Supplier", list(supplier_map))
            material_name = st.selectbox("Material", list(material_map))
            qty = st.number_input("Order quantity", min_value=1, value=10, step=1)
            price = st.number_input("Unit price (₹)", min_value=0.01, value=1000.0, step=100.0)
            po_date = st.date_input("Order date")
            create = st.form_submit_button("Create purchase order")
            if create:
                count = query("SELECT COUNT(*) AS n FROM purchase_orders").loc[0,"n"] + 1
                po_number = f"PO{int(count):04d}"
                execute("""INSERT INTO purchase_orders(po_number,supplier_id,material_id,quantity,unit_price,order_date,status)
                           VALUES(?,?,?,?,?,?,?)""",
                        (po_number,supplier_map[supplier_name],material_map[material_name],int(qty),float(price),str(po_date),"OPEN"))
                st.success(f"Created {po_number}.")
    st.markdown("#### Purchase order register")
    st.dataframe(query("""
        SELECT po.po_number, po.order_date, s.supplier_name, m.material_name,
               po.quantity, po.unit_price, po.quantity*po.unit_price AS total_value, po.status
        FROM purchase_orders po
        JOIN suppliers s ON s.supplier_id=po.supplier_id
        JOIN materials m ON m.material_id=po.material_id
        ORDER BY po.po_id DESC
    """), use_container_width=True, hide_index=True)

elif page == "Goods Receipts":
    st.subheader("Record goods receipt")
    orders = query("""
        SELECT po.po_id, po.po_number, m.material_name, po.quantity,
               COALESCE(SUM(gr.quantity_received),0) AS already_received
        FROM purchase_orders po
        JOIN materials m ON m.material_id=po.material_id
        LEFT JOIN goods_receipts gr ON gr.po_id=po.po_id
        GROUP BY po.po_id
        HAVING already_received < po.quantity
        ORDER BY po.po_number
    """)
    if orders.empty:
        st.info("No purchase orders have outstanding quantities.")
    else:
        with st.form("gr_form"):
            labels = {f"{r.po_number} | {r.material_name} | remaining {int(r.quantity-r.already_received)}": int(r.po_id) for r in orders.itertuples()}
            label = st.selectbox("Purchase order", list(labels))
            selected = orders[orders.po_id == labels[label]].iloc[0]
            remaining = int(selected.quantity - selected.already_received)
            received = st.number_input("Quantity received", min_value=1, max_value=remaining, value=min(remaining,1), step=1)
            receipt_date = st.date_input("Receipt date")
            submit = st.form_submit_button("Record goods receipt")
            if submit:
                execute("INSERT INTO goods_receipts(po_id,quantity_received,receipt_date) VALUES(?,?,?)",
                        (int(selected.po_id),int(received),str(receipt_date)))
                st.success("Goods receipt recorded.")
    st.markdown("#### Goods receipt history")
    st.dataframe(query("""
        SELECT gr.receipt_id, po.po_number, m.material_name, gr.quantity_received, gr.receipt_date
        FROM goods_receipts gr JOIN purchase_orders po ON po.po_id=gr.po_id
        JOIN materials m ON m.material_id=po.material_id ORDER BY gr.receipt_id DESC
    """), use_container_width=True, hide_index=True)

elif page == "Invoice Verification":
    st.subheader("Record and verify supplier invoice")
    orders = query("""
        SELECT po.po_id, po.po_number, s.supplier_name, po.quantity, po.unit_price,
               COALESCE(SUM(gr.quantity_received),0) AS received_qty
        FROM purchase_orders po JOIN suppliers s ON s.supplier_id=po.supplier_id
        LEFT JOIN goods_receipts gr ON gr.po_id=po.po_id
        GROUP BY po.po_id ORDER BY po.po_number
    """)
    if orders.empty:
        st.info("Create a purchase order first.")
    else:
        with st.form("invoice_form"):
            labels = {f"{r.po_number} | {r.supplier_name}": int(r.po_id) for r in orders.itertuples()}
            label = st.selectbox("Purchase order", list(labels))
            selected = orders[orders.po_id == labels[label]].iloc[0]
            invoice_no = st.text_input("Supplier invoice number")
            invoiced_qty = st.number_input("Quantity invoiced", min_value=1, value=int(selected.quantity), step=1)
            invoice_amount = st.number_input("Invoice amount (₹)", min_value=0.01,
                                             value=float(selected.quantity*selected.unit_price), step=100.0)
            invoice_date = st.date_input("Invoice date")
            submit = st.form_submit_button("Run three-way match")
            if submit:
                if not invoice_no.strip():
                    st.error("Invoice number is required.")
                else:
                    po_qty = int(selected.quantity)
                    gr_qty = int(selected.received_qty)
                    expected_amount = float(invoiced_qty * selected.unit_price)
                    qty_ok = invoiced_qty <= po_qty and invoiced_qty <= gr_qty
                    amount_ok = abs(float(invoice_amount)-expected_amount) < 0.01
                    status = "APPROVED" if qty_ok and amount_ok else "BLOCKED"
                    try:
                        execute("""INSERT INTO invoices(po_id,invoice_number,quantity_invoiced,amount,invoice_date,status)
                                   VALUES(?,?,?,?,?,?)""",
                                (int(selected.po_id),invoice_no.strip(),int(invoiced_qty),float(invoice_amount),str(invoice_date),status))
                        if status == "APPROVED":
                            st.success("Invoice passed the simulated checks and is APPROVED.")
                        else:
                            st.warning(f"Invoice is BLOCKED. Ordered quantity: {po_qty}; received quantity: {gr_qty}; invoiced quantity: {invoiced_qty}. Expected amount at PO price: {money(expected_amount)}.")
                    except sqlite3.IntegrityError:
                        st.error("That invoice number already exists.")
    st.markdown("#### Invoice register")
    st.dataframe(query("""
        SELECT i.invoice_number, po.po_number, i.quantity_invoiced, i.amount,
               i.invoice_date, i.status
        FROM invoices i JOIN purchase_orders po ON po.po_id=i.po_id
        ORDER BY i.invoice_id DESC
    """), use_container_width=True, hide_index=True)
    st.caption("Simplified educational rule: invoice quantity must not exceed ordered or received quantity, and amount must equal invoiced quantity × PO unit price. Real SAP invoice verification can include tolerances, taxes, freight, delivery costs, and configured blocks.")

elif page == "SQL Explorer":
    st.subheader("SQL learning workspace")
    st.caption("Run read-only SELECT queries against the project database.")
    examples = {
        "Purchase order value by supplier": """SELECT s.supplier_name, SUM(po.quantity*po.unit_price) AS order_value
FROM purchase_orders po JOIN suppliers s ON s.supplier_id=po.supplier_id
GROUP BY s.supplier_name ORDER BY order_value DESC;""",
        "Received quantity by purchase order": """SELECT po.po_number, po.quantity AS ordered,
COALESCE(SUM(gr.quantity_received),0) AS received
FROM purchase_orders po LEFT JOIN goods_receipts gr ON gr.po_id=po.po_id
GROUP BY po.po_id;""",
        "Invoices blocked for review": """SELECT invoice_number, quantity_invoiced, amount, status
FROM invoices WHERE status='BLOCKED';"""
    }
    choice = st.selectbox("Choose an example", list(examples))
    sql = st.text_area("SQL query", value=examples[choice], height=180)
    if st.button("Run SELECT"):
        if not sql.strip().lower().startswith("select"):
            st.error("Only SELECT queries are allowed in this explorer.")
        else:
            try:
                st.dataframe(query(sql), use_container_width=True, hide_index=True)
            except Exception as exc:
                st.error(f"SQL error: {exc}")

st.markdown("---")
st.caption("Designed & Developed by Aruna Arjun | Exploring ERP, Procurement & Business Process Analytics")
