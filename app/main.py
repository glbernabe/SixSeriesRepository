from fastapi import FastAPI

from app.routers import users, clients, profiles

app = FastAPI(debug=True)
app.include_router(users.router)
app.include_router(clients.router)
app.include_router(profiles.router)

@app.get("/")
async def root():
    return {"message": "Prueba"}


