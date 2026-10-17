
from business_agent.tools import calcular_promocion

resultado = calcular_promocion()

for indicador, valor in resultado.items():
    print(f"{indicador}: {valor}")
