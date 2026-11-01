PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name TEXT NOT NULL,
    city TEXT,
    email TEXT
);

CREATE TABLE IF NOT EXISTS materials (
    material_id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_code TEXT NOT NULL UNIQUE,
    material_name TEXT NOT NULL,
    unit TEXT NOT NULL DEFAULT 'EA'
);

CREATE TABLE IF NOT EXISTS purchase_orders (
    po_id INTEGER PRIMARY KEY AUTOINCREMENT,
    po_number TEXT NOT NULL UNIQUE,
    supplier_id INTEGER NOT NULL,
    material_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price REAL NOT NULL CHECK(unit_price >= 0),
    order_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'OPEN',
    FOREIGN KEY(supplier_id) REFERENCES suppliers(supplier_id),
    FOREIGN KEY(material_id) REFERENCES materials(material_id)
);

CREATE TABLE IF NOT EXISTS goods_receipts (
    receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
    po_id INTEGER NOT NULL,
    quantity_received INTEGER NOT NULL CHECK(quantity_received > 0),
    receipt_date TEXT NOT NULL,
    FOREIGN KEY(po_id) REFERENCES purchase_orders(po_id)
);

CREATE TABLE IF NOT EXISTS invoices (
    invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
    po_id INTEGER NOT NULL,
    invoice_number TEXT NOT NULL UNIQUE,
    quantity_invoiced INTEGER NOT NULL CHECK(quantity_invoiced > 0),
    amount REAL NOT NULL CHECK(amount >= 0),
    invoice_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'PENDING',
    FOREIGN KEY(po_id) REFERENCES purchase_orders(po_id)
);
