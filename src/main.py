'''
Archivo Orquestador del Sistema Multi-Agente
'''


import argparse
from .logger_configuration import logger
from .call_api import call_api

def go():
    parser = argparse.ArgumentParser(description="Sistema Multi-Agente")
    parser.add_argument("--query", type=str, required=True, help="Consulta del usuario")
    args = parser.parse_args()

    system_prompt = Orquestador.md
    user_prompt = args.query

    response = call_api(system_prompt, user_prompt, json_mode=True)
    logger.info(response)   


if __name__ == "__main__":
    go()


## Instrucciones 
# REplica adaptada al caso de uso 
#=============================================================
#            Main Controller (Orquestador)      
#=============================================================

# def main(topic):
#     # 1. El Router decide el camino
#     ruta_seleccionada = agente_router(topic)
#     logger.info(f"Router decidió: {ruta_seleccionada}")
    
#     resultado = ""
    
#     # 2. Switch Case (Lógica de Enrutamiento)
#     if ruta_seleccionada == "RECONCILIACION":
#         resultado = flujo_reconciliacion(topic)
        
#     elif ruta_seleccionada == "ROMANTICO":
#         resultado = flujo_romantico(topic)
        
#     elif ruta_seleccionada == "CASUAL":
#         resultado = flujo_casual(topic)
        
#     else:
#         # Fallback
#         logger.warning("Ruta desconocida, ejecutando flujo casual.")
#         resultado = flujo_casual(topic)
        
#     return {
#         "ruta": ruta_seleccionada,
#         "mensaje": resultado
#     }
