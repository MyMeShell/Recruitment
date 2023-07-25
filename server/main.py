import asyncio
import random
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.post("/")
async def main_route():
  
  error_codes = ["Bad Request", "Unauthorized", "Forbidden", "Not Found", "Internal Server Error !"]    
  #liste des différents code d'erreurs

  while True:
        
    random_number = random.randint(0, 4)
         
    await asyncio.sleep(3)

    if __name__ == "__main__":
      
      uvicorn.run(app, host="127.0.0.1", port=8000)

    return {"message": error_codes[random_number]}
    #réponse aléatoire d'un message d'erreur
  

