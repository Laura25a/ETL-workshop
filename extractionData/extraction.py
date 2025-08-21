import pandas as pd
import sqlite3

def salesPerCategory(dbName):
    try:
        conn = sqlite3.connect(dbName)

        cursor = conn.cursor()

        cursor.execute('''
            SELECT sum(s.quantity) as total, p.product_name as product
            FROM sales s
            JOIN products p
            ON s.product_id = p.product_id
            GROUP BY product
        ''')

        return cursor.fetchall()
    
    except Exception as e:
        return str(e)
    
def revenuesChannel(dbName): 
    try:
        conn = sqlite3.connect(dbName)

        cursor = conn.cursor()

        cursor.execute('''
            SELECT json_group_array(
                    json_object(
                        'month', month,
                        'channel', channel,
                        'revenue', revenue
                    )
                ) AS result
            FROM (
                SELECT
                       d.month AS month,
                       c.channel AS channel,
                       SUM(s.quantity * s.unit_price_sale) AS revenue
                FROM sales s
                JOIN channels c
                    ON s.channel_id = c.channel_id
                JOIN date d 
                    ON s.date_id = d.date_id
                WHERE c.channel = (
                        SELECT c2.channel
                        FROM sales s2
                        JOIN channels c2
                        ON s2.channel_id = c2.channel_id
                        GROUP BY c2.channel
                        ORDER BY SUM(s2.quantity * s2.unit_price_sale) DESC
                        LIMIT 1
                    )
                GROUP BY d.month
                ORDER BY d.month
            );
        ''')

        return cursor.fetchall()
    
    except Exception as e:
        return str(e)