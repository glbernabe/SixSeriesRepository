from fastapi import FastAPI

from app.routers import users, content


app = FastAPI(debug=True)
app.include_router(users.router)
app.include_router(content.router)

@app.get("/")
async def root():
    return {"message": "Prueba"}


