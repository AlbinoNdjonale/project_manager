from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from utils import Utils

Utils.up_env()

import middlewares
from routes import routes

app = FastAPI()

app.mount(
    '/assets',
    StaticFiles(directory='static/dist/assets'),
    'static'
)

app.add_middleware(middlewares.UpdateCsrfToken)
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
    expose_headers    = ["WWW-Authenticate"]
)

app.include_router(routes)