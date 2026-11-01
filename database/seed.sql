INSERT INTO suppliers(supplier_name, city, email) VALUES
('ABC Technologies', 'Mumbai', 'orders@abctech.example'),
('Western Office Supplies', 'Pune', 'sales@western.example'),
('Metro IT Solutions', 'Navi Mumbai', 'procurement@metro.example');

INSERT INTO materials(material_code, material_name, unit) VALUES
('LAP-001', 'Business Laptop', 'EA'),
('MON-001', '24-inch Monitor', 'EA'),
('KEY-001', 'Wireless Keyboard', 'EA');

INSERT INTO purchase_orders(po_number,supplier_id,material_id,quantity,unit_price,order_date,status) VALUES
('PO1001',1,1,100,45000,'2026-10-01','OPEN'),
('PO1002',2,2,40,9000,'2026-10-05','OPEN'),
('PO1003',3,3,50,1200,'2026-10-10','OPEN');

INSERT INTO goods_receipts(po_id,quantity_received,receipt_date) VALUES
(1,95,'2026-10-08'),
(2,40,'2026-10-12'),
(3,50,'2026-10-14');

INSERT INTO invoices(po_id,invoice_number,quantity_invoiced,amount,invoice_date,status) VALUES
(1,'INV-ABC-001',100,4500000,'2026-10-09','BLOCKED'),
(2,'INV-WOS-002',40,360000,'2026-10-13','APPROVED'),
(3,'INV-MIT-003',50,60000,'2026-10-15','APPROVED');
