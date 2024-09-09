from fastapi import APIRouter, Request
from controllers import User

from utils.auth import Auth

user = APIRouter()
controller = User()

@user.post('/')
async def insert_user(request: Request):
    return await Auth.authcreateuser(controller.create, request)

@user.get('/{user_id}')
async def get_user(request: Request, user_id):
    return await Auth.relationship(controller.get, request, user_id)

@user.delete('/{user_id}')
async def delete_user(request: Request, user_id):
    return await Auth.relationship(controller.delete, request, user_id)

@user.put('/{user_id}')
async def update_user(request: Request, user_id):
    return await Auth.relationship(controller.update, request, user_id)