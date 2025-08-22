import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from extractionData.extraction import salesPerCategory
from extractionData.extraction import revenuesChannel
from extractionData.extraction import newCustomers
from extractionData.extraction import salesByRegion
from extractionData.extraction import lowRotationProducts
from extractionData.extraction import revenueGrowth


DB_NAME = 'sales.db'  
df_sales_cat = salesPerCategory(DB_NAME)
df_revenues = revenuesChannel(DB_NAME)
df_new_customers = newCustomers(DB_NAME)
df_sales_ByRegion = salesByRegion(DB_NAME)
df_low_rotation = lowRotationProducts(DB_NAME)
df_revenue_growth = revenueGrowth(DB_NAME)

# Calcular porcentaje para Ventas por categoría-
df_sales_cat['percentage'] = df_sales_cat['total_units'] / df_sales_cat['total_units'].sum() * 100

# Ingresos por canal de venta (físico vs online) y su variación en el tiempo.
df_revenues_channel = df_revenues.groupby(['month','channel'])['revenue'].sum().reset_index()

#Por region

pivot_df = df_sales_ByRegion.pivot_table(index="country", columns="city", values="total_sales", fill_value=0)



#---pestaña tkinter ---

root = tk.Tk()
root.title("KPIs Technology Store")
root.geometry("900x700")

tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)
tab6 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Ventas por categoría')
tabControl.add(tab2, text='Ingresos por canal')
tabControl.add(tab3, text='Ventas por región')
tabControl.add(tab4, text='Clientes Nuevos por Mes/Año')
tabControl.add(tab5, text='Productos Baja Rotación')
tabControl.add(tab6, text='Crecimiento de ingresos')
tabControl.pack(expand=1, fill="both")

#1. Ventas por categoría --------

plt.figure(figsize=(8, 8))

fig1, ax1 = plt.subplots()
ax1.pie(df_sales_cat['percentage'], labels=df_sales_cat['category'], autopct='%1.1f%%', startangle=90)

plt.title('Ventas por categoría', fontsize=16)
plt.axis('equal')

canvas1 = FigureCanvasTkAgg(fig1, master=tab1)
canvas1.draw()
canvas1.get_tk_widget().pack(expand=True, fill='both')

#2. Ventas por canal ------------
plt.figure(figsize=(8,5))

fig2, ax2 = plt.subplots(figsize=(8,5))
for channel in df_revenues_channel['channel'].unique():
    df_plot = df_revenues_channel[df_revenues_channel['channel'] == channel]
    ax2.plot(df_plot['month'], df_plot['revenue'], marker='o', label=channel)

ax2.set_title("Ingresos por Canal de Venta")
ax2.set_xlabel("Mes")
ax2.set_ylabel("Ingresos")
ax2.legend()
ax2.grid(True)

canvas2 = FigureCanvasTkAgg(fig2, master=tab2)
canvas2.draw()
canvas2.get_tk_widget().pack(expand=True, fill='both')


# 3.Ventas por region geografica ----------

fig3, ax3 = plt.subplots(figsize=(7, 5))
pivot_df.plot(kind="bar", stacked=True, ax=ax3)

ax3.set_title("Ventas por Región (País / Ciudad)")
ax3.set_ylabel("Total Ventas")
ax3.set_xlabel("País")

canvas3 = FigureCanvasTkAgg(fig3, master=tab3)
canvas3.draw()
canvas3.get_tk_widget().pack(expand=True, fill='both')

#4.clientes mes año ----------------------


fig4, ax4 = plt.subplots(figsize=(7, 5))
ax4.fill_between(df_new_customers["month"], df_new_customers["new_customers"], color="skyblue", alpha=0.5)
ax4.plot(df_new_customers["month"], df_new_customers["new_customers"], color="black", marker="o")

ax4.set_title("Clientes Nuevos por Mes (2025)")
ax4.set_xlabel("Mes")
ax4.set_ylabel("Nuevos Clientes")
ax4.set_xticks(df_new_customers["month"])

canvas4 = FigureCanvasTkAgg(fig4, master=tab4)
canvas4.draw()
canvas4.get_tk_widget().pack(expand=True, fill='both')



#5.crecimiento de ingresos --------------


fig6, (ax6_1, ax6_2) = plt.subplots(2, 1, figsize=(8, 8), sharex=True)

# Línea de ingresos totales por mes
ax6_1.plot(df_revenue_growth["month"], df_revenue_growth["total_revenue"], color="blue", marker="o", linewidth=2)
ax6_1.set_title("Ingresos Totales por Mes")
ax6_1.set_ylabel("Ingresos")
ax6_1.grid(True, linestyle="--", alpha=0.5)

# Barra de crecimiento porcentual
ax6_2.bar(
    df_revenue_growth["month"],
    df_revenue_growth["growth_pct"],
    color=["green" if x > 0 else "red" for x in df_revenue_growth["growth_pct"]]
)
ax6_2.axhline(0, color="black", linestyle="--", linewidth=0.8)
ax6_2.set_title("Crecimiento % vs Mes Anterior")
ax6_2.set_xlabel("Mes")
ax6_2.set_ylabel("Crecimiento (%)")
ax6_2.grid(True, linestyle="--", alpha=0.5)

fig6.tight_layout()


canvas6 = FigureCanvasTkAgg(fig6, master=tab6)
canvas6.draw()
canvas6.get_tk_widget().pack(expand=True, fill='both')


# 6. Productos de baja rotación -------------


fig5, ax5 = plt.subplots(figsize=(8, 5))
df_sorted = df_low_rotation.sort_values("total_units_sold", ascending=True).head(5)
ax5.barh(df_sorted["product"], df_sorted["total_units_sold"], color="orange", edgecolor="black")
ax5.set_title("Top 5 Productos con Menor Rotación")
ax5.set_xlabel("Unidades Vendidas")
ax5.set_ylabel("Producto")
ax5.grid(True, linestyle="--", alpha=0.5)
fig5.tight_layout()

canvas5 = FigureCanvasTkAgg(fig5, master=tab5)
canvas5.draw()
canvas5.get_tk_widget().pack(expand=True, fill='both')


root.mainloop()
