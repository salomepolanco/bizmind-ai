
from business_agent.rag import indexar_documentos, buscar_conocimiento

cantidad = indexar_documentos()
print(f"Documentos indexados: {cantidad}")

pregunta = "¿Qué promoción ayuda a vender más sándwiches?"
print("\nInformación recuperada:")
print(buscar_conocimiento(pregunta))
