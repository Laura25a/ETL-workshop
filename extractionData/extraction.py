import pandas as pd
import sqlite3



# KPI 1
def salesPerCategory(dbName):
    conn = sqlite3.connect(dbName)
    query = '''
        SELECT p.category AS category,
               SUM(s.quantity) AS total_units
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.category
        ORDER BY total_units DESC;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# KPI 2 
def revenuesChannel(dbName): 
    conn = sqlite3.connect(dbName)
    query = '''
        SELECT d.month AS month,
               c.channel AS channel,
               SUM(s.quantity * s.unit_price_sale) AS revenue
        FROM sales s
        JOIN channels c ON s.channel_id = c.channel_id
        JOIN date d ON s.date_id = d.date_id
        GROUP BY d.month, c.channel
        ORDER BY d.month;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# KPI 3
def newCustomers(dbName):
    conn = sqlite3.connect(dbName)
    query = '''
        SELECT d.year AS year,
               d.month AS month,
               COUNT(DISTINCT s.customer_id) AS new_customers
        FROM sales s
        JOIN date d ON s.date_id = d.date_id
        GROUP BY d.year, d.month
        ORDER BY d.year, d.month;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# KPI 4

def salesByRegion(dbName):
    conn = sqlite3.connect(dbName)
    query = '''
        SELECT c.country AS country,
               c.city AS city,
               SUM(s.quantity * s.unit_price_sale) AS total_sales
        FROM sales s
        JOIN customers c ON s.customer_id = c.customer_id
        GROUP BY c.country, c.city
        ORDER BY total_sales DESC;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# KPI 5

def lowRotationProducts(dbName):
    conn = sqlite3.connect(dbName)
    query = '''
        SELECT p.product_id,
               p.category AS product,
               SUM(s.quantity) AS total_units_sold
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.product_id, p.category
        ORDER BY total_units_sold ASC
        LIMIT 5;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# KPI 6

def revenueGrowth(dbName):
    conn = sqlite3.connect(dbName)
    query = '''
        SELECT d.year AS year,
               d.month AS month,
               SUM(s.quantity * s.unit_price_sale) AS total_revenue
        FROM sales s
        JOIN date d ON s.date_id = d.date_id
        GROUP BY d.year, d.month
        ORDER BY d.year, d.month;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()


    df = df.drop_duplicates()

    
    df["growth_pct"] = df["total_revenue"].pct_change().round(2) * 100

    return df
