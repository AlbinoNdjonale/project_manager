from controllers import Auth
from fastapi import APIRouter, Request

from utils.auth import Auth as Auth_

auth = APIRouter()
controller = Auth()

@auth.post('/login')
async def login(request: Request):
    return await controller.login(request)

@auth.post('/logout/{user_id}')
async def loguot(user_id, request: Request):
    return await Auth_.relationship(controller.logout, request, user_id)