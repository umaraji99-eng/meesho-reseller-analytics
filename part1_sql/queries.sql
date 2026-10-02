-- Part 1: Monthly revenue by category
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY month, category;


-- Part 1: Regional revenue and order count
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
    COUNT(*) AS order_count
FROM orders o
JOIN resellers r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;


-- Part 1: Top 5 resellers by total spend
SELECT
    reseller_id,
    ROUND(SUM(quantity * unit_price), 2) AS total_spend
FROM orders
GROUP BY reseller_id
ORDER BY total_spend DESC
LIMIT 5;


-- Part 1: Resellers with zero orders
SELECT
    r.reseller_id,
    r.reseller_name
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;


-- Part 1: COUNT(*) versus COUNT(order_id)
SELECT
    r.reseller_id,
    COUNT(*) AS count_all,
    COUNT(o.order_id) AS count_order_id
FROM resellers r
LEFT JOIN orders o
    ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY r.reseller_id;


-- Part 1: June Delivered Average Order Value
SELECT
    ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
