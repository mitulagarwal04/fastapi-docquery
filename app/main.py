from fastapi import FastAPI
from app.api.v1 import auth
import logging
import sys


app = FastAPI(title='AI doc query')

app.include_router(auth.router, prefix="", tags=["Auth"])

@app.get("/")
def root():
    return {"message":'Welcome to AI Document Query API'}