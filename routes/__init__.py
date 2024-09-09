from fastapi import APIRouter

from .api import api
from .web import web

routes = APIRouter()

routes.include_router(api, prefix = '/api')
routes.include_router(web)