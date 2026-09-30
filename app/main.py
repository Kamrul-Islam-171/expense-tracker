from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers.auth import router as auth_router
from app.routers.transactions import router as transaction_router

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth_router)
app.include_router(transaction_router)

@app.get("/")
def root():
    return {"message": "Expense Tracker API"}