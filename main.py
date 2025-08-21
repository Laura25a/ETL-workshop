import pandas as pd

from extractionData.extraction import *
from loadData.load import *
from transformationData.transformation import *

def main():

    '''
    CAMBIAN POR LA DIRECCION DE USTEDES DONDE SE ENCUENTRE EL DF EN MI CASO ES AQUI.
    BUENO, PRUEBEN SI LES CARGA, BIEN :)
    '''
    df = pd.read_csv('dataSales/ETL_store_sales_200.csv').sort_values(by=['product_id'])

    trasnformeData = dataTransformation(df)

    loadToDB = load(trasnformeData, 'sales.db')
    salesCategory = salesPerCategory('sales.db')
    topSalesChannel = revenuesChannel('sales.db')

if __name__ == "__main__":
    main()