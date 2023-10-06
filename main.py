from fastapi import FastAPI

from src.translate_routes import translate_router

app = FastAPI(
    title="Word Translate Api",
    description="Created by Zoltán Pallai",
    version="2.5.0")

app.include_router(translate_router, prefix="/v1")

import init_db
