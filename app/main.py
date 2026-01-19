from fastapi import FastAPI

from app.routers import users, clients

app = FastAPI(debug=True)
app.include_router(users.router)
app.include_router(clients.router)

@app.get("/")
async def root():
    return {"message": "Prueba"}


