
# import random
# import asyncio
# import logging
# import traceback
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# import uvicorn
# from starlette.websockets import WebSocketDisconnect as StarletteWebSocketDisconnect

# # Configuration de l'enregistrement des erreurs dans les logs
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Création d'une instance FastAPI
# app = FastAPI()

# # Liste pour stocker les connexions websocket
# websocket_connections = set()

# # Fonction asynchrone pour générer aléatoirement des erreurs HTTP 500
# async def generate_random_error():
#     while True:
#         await asyncio.sleep(random.randint(1, 3))  # Attendre un délai aléatoire entre 1 et 3 secondes
#         if random.random() < 0.5:  # Probabilité de 50% de générer une erreur
#             try:
#                 raise Exception("Erreur interne du serveur")
#             except Exception as e:
#                 error_msg = f"Erreur générée: {str(e)}\n{traceback.format_exc()}"
#                 logger.error(error_msg)
#                 # Envoyer le message d'erreur aux clients connectés via websocket
#                 await send_to_clients(str(error_msg))  # Convertir en chaîne avec str()

# # Fonction pour envoyer des données aux clients websocket
# async def send_to_clients(message):
#     for connection in websocket_connections:
#         await connection.send_text(message)  # Utiliser send_text() pour envoyer une chaîne de caractères

# # Gestionnaire pour les connexions websocket
# @app.websocket("/ws")
# async def websocket_handler(websocket: WebSocket):
#     await websocket.accept()
#     # Ajouter la connexion au groupe
#     websocket_connections.add(websocket)
#     try:
#         # Attendre les messages des clients (ceci est optionnel, vous pouvez gérer les connexions sans attendre les messages)
#         while True:
#             data = await websocket.receive_text()
#             print(f"Message reçu du client: {data}")
#     except (WebSocketDisconnect, StarletteWebSocketDisconnect):
#         pass
#     finally:
#         # Supprimer la connexion du groupe lorsque le client se déconnecte
#         websocket_connections.remove(websocket)

# # Démarrage de la tâche asynchrone pour générer des erreurs
# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(generate_random_error())


# # Lancer l'application FastAPI
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="localhost", port=8000)


import random
import asyncio
import logging
import traceback
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

websocket_connections = set()

exception_types = [ValueError, PermissionError, FileNotFoundError, RuntimeError]

async def generate_random_error():
    while True:
        await asyncio.sleep(3)  # Générer une erreur toutes les 3 secondes
        try:
            # Choisir un type d'exception aléatoire
            exception_type = random.choice(exception_types)
            # Générer l'erreur
            raise exception_type("Erreur aléatoire du serveur")
        except Exception as e:
            error_msg = f"Erreur générée: {traceback.format_exc()}"
            logger.error(error_msg)
            # Envoyer le message d'erreur aux clients connectés via websocket
            await send_to_clients(str(error_msg))  # Convertir en chaîne avec str()

# Fonction pour envoyer des données aux clients websocket
async def send_to_clients(message):
    for connection in websocket_connections:
        await connection.send_text(message)

# Gestionnaire pour les connexions websocket
@app.websocket("/ws")
async def websocket_handler(websocket: WebSocket):
    await websocket.accept()
    # Ajouter la connexion au groupe
    websocket_connections.add(websocket)
    try:
        # Attendre les messages des clients (ceci est optionnel, vous pouvez gérer les connexions sans attendre les messages)
        while True:
            data = await websocket.receive_text()
            print(f"Message reçu du client: {data}")
    except WebSocketDisconnect:
        pass
    finally:
        # Supprimer la connexion du groupe lorsque le client se déconnecte
        websocket_connections.remove(websocket)

# Démarrage de la tâche asynchrone pour générer des erreurs
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(generate_random_error())

# Lancer l'application FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8081)



