# In router.py
from fastapi import APIRouter
from .endpoints import credentials, schema

api_router = APIRouter()
api_router.include_router(credentials.router, tags=["credentials"])
api_router.include_router(schema.router, tags=["schema"])
