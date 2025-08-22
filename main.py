import pandas as pd
from extractionData.extraction import (
    salesPerCategory,
    revenuesChannel,
    newCustomers,
    salesByRegion,
    lowRotationProducts,
    revenueGrowth
)

DB_NAME = "sales.db"

def main():
    # KPI 1: Ventas por categoría
    df_sales_cat = salesPerCategory(DB_NAME)
    print("\n Ventas por categoría:")
    print(df_sales_cat)

    # KPI 2: Ingresos por canal y variación mensual
    df_revenues = revenuesChannel(DB_NAME)
    print("\n Ingresos por cana(DataFrame):")
    print(df_revenues)

    # KPI 3: Clientes nuevos por mes/año
    df_new_customers = newCustomers(DB_NAME)
    print("\n Clientes nuevos por mes/año:")
    print(df_new_customers)

    # KPI 4: Ventas por región geográfica
    df_sales_region = salesByRegion(DB_NAME)
    print("\n Ventas por región geográfica:")
    print(df_sales_region)

    # KPI 5: Productos con menor rotación
    df_low_rotation = lowRotationProducts(DB_NAME)
    print("\n Productos con menor rotación:")
    print(df_low_rotation)

    # KPI 6: Crecimiento de ingresos
    df_revenue_growth = revenueGrowth(DB_NAME)
    print("\n Crecimiento de ingresos mensual:")
    print(df_revenue_growth.to_string(index=False))

if __name__ == "__main__":
    main()
