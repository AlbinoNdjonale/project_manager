from fastapi import APIRouter
from fastapi.responses import FileResponse

web = APIRouter()

@web.route('/{path:path}', ['GET', 'POST', 'DELETE', 'PUT'])
def home(path):
    return FileResponse('./static/dist/index.html', 200, media_type = 'text/html')