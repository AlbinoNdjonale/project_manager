from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, JSONResponse

web = APIRouter()

@web.route('/{path:path}', ['GET', 'POST', 'DELETE', 'PUT'])
def home(path):
    return FileResponse('./static/dist/index.html', 200, media_type = 'text/html')

def options(_: Request):
    return JSONResponse(
        {},
        200,
        {'Access-Control-Allow-Methods': 'DELETE,PUT'}
    )

web.add_route('/{path:path}', options, methods = ['OPTIONS'])
