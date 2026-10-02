import os
import csv
import sqlite3

# Define the output directory
OUTPUT_DIR = os.path.join("part1_sql", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Connect to your SQLite database (Replace with your actual .db file path)
DB_PATH = "data/meesho_reseller.db" 
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def save_to_csv(filename, headers, rows):
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Saved: {filepath} ({len(rows)} rows)")

# =====================================================================
# Q1: Monthly revenue by category
# =====================================================================
q1_query = """
SELECT 
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category;
"""
cursor.execute(q1_query)
save_to_csv("monthly_category_revenue.csv", ["month", "category", "revenue", "n_orders"], cursor.fetchall())

# =====================================================================
# Q2: Region-wise total revenue and order count
# =====================================================================
q2_query = """
SELECT 
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
    COUNT(*) AS order_count
FROM orders o
JOIN resellers r ON o.reseller_id = r.reseller_id
GROUP BY r.region;
"""
cursor.execute(q2_query)
save_to_csv("region_revenue.csv", ["region", "total_revenue", "order_count"], cursor.fetchall())

# =====================================================================
# Q3: Top resellers by total spend
# =====================================================================
q3_query = """
SELECT 
    reseller_id,
    ROUND(SUM(quantity * unit_price), 2) AS total_spend
FROM orders
GROUP BY reseller_id
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;
"""
cursor.execute(q3_query)
save_to_csv("top_resellers.csv", ["reseller_id", "total_spend"], cursor.fetchall())

# =====================================================================
# Q4: Resellers who have never placed an order (Part A & B)
# =====================================================================
# Part A: Identify resellers with zero matching orders
q4_a_query = """
SELECT r.reseller_id, r.reseller_name
FROM resellers r
LEFT JOIN orders o ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;
"""
cursor.execute(q4_a_query)
unmatched_resellers = cursor.fetchall()
save_to_csv(
    "inactive_resellers.csv",
    ["reseller_id", "reseller_name"],
    unmatched_resellers
)

# Part B: Demonstration of COUNT(*) vs COUNT(order_id)
# We will run this specifically for one of the unmatched reseller IDs found above (if any exist)
if unmatched_resellers:
    demo_reseller_id = unmatched_resellers[0][0]
    q4_b_query = f"""
    SELECT 
        r.reseller_id,
        COUNT(*) AS count_all,
        COUNT(o.order_id) AS count_order_id
    FROM resellers r
    LEFT JOIN orders o ON r.reseller_id = o.reseller_id
    WHERE r.reseller_id = '{demo_reseller_id}'
    GROUP BY r.reseller_id;
    """
    cursor.execute(q4_b_query)
    save_to_csv("count_demonstration.csv", ["reseller_id", "count_all", "count_order_id"], cursor.fetchall())
else:
    print("No unmatched resellers found; count_demonstration.csv skipped.")

# =====================================================================
# Q5: Average Order Value (AOV) for June, Delivered orders only
# =====================================================================
q5_query = """
SELECT ROUND(SUM(quantity * unit_price) / COUNT(*), 2) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
"""
cursor.execute(q5_query)
save_to_csv("june_delivered_aov.csv", ["june_delivered_aov"], cursor.fetchall())

# Close database connection
conn.close()
print("All tasks completed successfully!")
