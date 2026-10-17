
import pandas as pd

ventas = pd.read_csv("data/ventas.csv")

print("Primeras filas:")
print(ventas.head())

print("\nTotal de registros:", len(ventas))
print("Columnas:", list(ventas.columns))
