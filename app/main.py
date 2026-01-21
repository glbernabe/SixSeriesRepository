from fastapi import FastAPI

from app.routers import users, content, genre


app = FastAPI(debug=True)
app.include_router(users.router)
app.include_router(content.router)
app.include_router(genre.router)

@app.get("/")
async def root():
    return {"message": "Prueba"}


