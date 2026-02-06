from fastapi import FastAPI

from app.routers import users, subscriptions, profiles, payments, content, genre, favorites

app = FastAPI(debug=True)
app.include_router(users.router)
app.include_router(subscriptions.router)
app.include_router(profiles.router)
app.include_router(payments.router)
app.include_router(content.router)
app.include_router(genre.router)
app.include_router(favorites.router)
@app.get("/")
async def root():
    return {"message": "Prueba"}


