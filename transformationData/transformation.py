import pandas as pd

#Transformacion
def dataTransformation(df):

    products = df[['product_id', 'product_name', 'category', 'brand', 'unit_price', 'unit_cost']].drop_duplicates()

    customers = df[['customer_id', 'customer_name', 'city', 'country', 'age']].drop_duplicates()

    channels = df[['channel_id', 'channel']].drop_duplicates()

    df['date'] = pd.to_datetime(df['date'])
    date = df[['date']].drop_duplicates()
    date['date_id'] = range(1, len(date)+1)
    date['year'] = date['date'].dt.year
    date['month'] = date['date'].dt.month
    date['weekday'] = date['date'].dt.day_name()

    sales = df.merge(date[['date', 'date_id']], on='date')[['sale_id', 'date_id', 'product_id', 'customer_id', 'channel_id', 'quantity', 'unit_price_sale']]
    
    return [
        ("products", products),
        ("customers", customers),
        ("channels", channels),
        ("date", date),
        ("sales", sales)
    ]