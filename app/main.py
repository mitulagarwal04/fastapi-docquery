from fastapi import FastAPI
from fastapi.security import HTTPBearer
from app.api.v1 import auth
import logging
import sys
from app.core.database import init_db

oauth2_scheme = HTTPBearer()
app = FastAPI(title='AI doc query')

app.include_router(auth.router, prefix="", tags=["Auth"])

@app.get("/")
def root():
    return {"message":'Welcome to AI Document Query API'}

@app.on_event("startup")
async def on_startup():
    await init_db()

