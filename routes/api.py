from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from .author import author
from .detail import detail
from .project import project
from .user import user
from .link import link

from .auth import auth

def options(_: Request):
    return JSONResponse(
        {},
        200,
        {'Access-Control-Allow-Methods': 'DELETE,PUT'}
    )

project.add_route('/{id}', options, methods = ['OPTIONS'])
user.add_route('/{id}', options, methods = ['OPTIONS'])
author.add_route('/{id}', options, methods = ['OPTIONS'])
detail.add_route('/{id}', options, methods = ['OPTIONS'])
link.add_route('/{id}', options, methods = ['OPTIONS'])

api = APIRouter()

v1 = APIRouter()

v1.include_router(user, prefix = "/users")
v1.include_router(project, prefix = "/projects")
v1.include_router(author, prefix = '/authors')
v1.include_router(auth, prefix = '/auth')
v1.include_router(detail, prefix = '/details')
v1.include_router(link, prefix = '/links')

api.include_router(v1, prefix = "/v1")

@api.route('/{path:path}', ['GET', 'POST', 'DELETE', 'PUT'])
def notfound(path):
    return JSONResponse({'detail': 'Not Found'}, 404)