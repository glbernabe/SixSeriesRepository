from fastapi import FastAPI

from app.routers import users, subscriptions, profiles, payments

app = FastAPI(debug=True)
app.include_router(users.router)
app.include_router(subscriptions.router)
app.include_router(profiles.router)
app.include_router(payments.router)

@app.get("/")
async def root():
    return {"message": "Prueba"}


