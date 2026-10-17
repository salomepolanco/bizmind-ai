
import pandas as pd


def analizar_ventas() -> dict:
    """Analiza las ventas de la cafetería y calcula sus principales indicadores."""

    ventas = pd.read_csv("data/ventas.csv")

    ventas["ingresos"] = ventas["cantidad"] * ventas["precio"]
    ventas["costo_total"] = ventas["cantidad"] * ventas["costo"]
    ventas["ganancia_bruta"] = ventas["ingresos"] - ventas["costo_total"]

    productos = (
        ventas.groupby("producto")["cantidad"]
        .sum()
        .sort_values(ascending=False)
    )

    return {
        "ingresos_totales": round(ventas["ingresos"].sum(), 2),
        "costos_totales": round(ventas["costo_total"].sum(), 2),
        "ganancia_bruta": round(ventas["ganancia_bruta"].sum(), 2),
        "productos_mas_vendidos": productos.head(3).to_dict(),
    }




def calcular_promocion(
    precio_cafe: float = 2.00,
    costo_cafe: float = 0.70,
    precio_sandwich: float = 3.50,
    costo_sandwich: float = 1.80,
    descuento_porcentaje: float = 10.0,
) -> dict:
    """
    Calcula la rentabilidad de un combo de café y sándwich.
    Compara el precio habitual con el precio promocional.
    Devuelve ingresos, costos, ganancias y el incremento de
    volumen necesario para compensar la reducción de ganancia.
    """

    # Validar los valores de entrada
    if precio_cafe < 0 or costo_cafe < 0:
        raise ValueError("Los precios y costos no pueden ser negativos.")

    if precio_sandwich < 0 or costo_sandwich < 0:
        raise ValueError("Los precios y costos no pueden ser negativos.")

    if costo_cafe > precio_cafe or costo_sandwich > precio_sandwich:
        raise ValueError("El costo de un producto supera su precio de venta.")

    if not 0 <= descuento_porcentaje < 100:
        raise ValueError("El descuento debe ser mayor o igual a 0 y menor a 100.")

    # Precio y ganancia a precio habitual
    precio_habitual = precio_cafe + precio_sandwich
    costo_total = costo_cafe + costo_sandwich
    ganancia_habitual = precio_habitual - costo_total

    # Precio y ganancia con descuento
    precio_promocional = precio_habitual * (
        1 - descuento_porcentaje / 100
    )
    ganancia_promocional = precio_promocional - costo_total

    # Márgenes brutos
    margen_habitual = (
        ganancia_habitual / precio_habitual * 100
        if precio_habitual > 0 else 0
    )
    margen_promocional = (
        ganancia_promocional / precio_promocional * 100
        if precio_promocional > 0 else 0
    )

    # Incremento de unidades para igualar la ganancia habitual
    if ganancia_promocional > 0:
        incremento_necesario = (
            ganancia_habitual / ganancia_promocional - 1
        ) * 100
    else:
        incremento_necesario = None

    return {
        "precio_habitual": round(precio_habitual, 2),
        "precio_promocional": round(precio_promocional, 2),
        "descuento_porcentaje": descuento_porcentaje,
        "costo_total_por_combo": round(costo_total, 2),
        "ganancia_bruta_habitual": round(ganancia_habitual, 2),
        "ganancia_bruta_promocional": round(ganancia_promocional, 2),
        "margen_bruto_habitual_porcentaje": round(margen_habitual, 2),
        "margen_bruto_promocional_porcentaje": round(margen_promocional, 2),
        "reduccion_ganancia_por_combo": round(
            ganancia_habitual - ganancia_promocional, 2
        ),
        "incremento_unidades_para_igualar_ganancia_porcentual": (
            round(incremento_necesario, 2)
            if incremento_necesario is not None else None
        ),
    }
