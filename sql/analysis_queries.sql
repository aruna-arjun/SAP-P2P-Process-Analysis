-- 1. Purchase order value by supplier
SELECT s.supplier_name, SUM(po.quantity * po.unit_price) AS order_value
FROM purchase_orders po
JOIN suppliers s ON s.supplier_id = po.supplier_id
GROUP BY s.supplier_name
ORDER BY order_value DESC;

-- 2. Ordered versus received quantity
SELECT po.po_number, m.material_name, po.quantity AS ordered_quantity,
       COALESCE(SUM(gr.quantity_received), 0) AS received_quantity
FROM purchase_orders po
JOIN materials m ON m.material_id = po.material_id
LEFT JOIN goods_receipts gr ON gr.po_id = po.po_id
GROUP BY po.po_id;

-- 3. Invoice status register
SELECT invoice_number, quantity_invoiced, amount, status
FROM invoices
ORDER BY invoice_date;

-- 4. Outstanding quantities
SELECT po.po_number, po.quantity - COALESCE(SUM(gr.quantity_received),0) AS outstanding_quantity
FROM purchase_orders po
LEFT JOIN goods_receipts gr ON gr.po_id = po.po_id
GROUP BY po.po_id
HAVING outstanding_quantity > 0;
