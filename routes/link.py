from fastapi import APIRouter, Request
from controllers import Link

from utils.auth import Auth

link = APIRouter()
controller = Link()

@link.post('/')
async def insert_link(request: Request):
    return await Auth.relationship(controller.create, request)

@link.get('/{link_id}')
async def get_link(request: Request, link_id):
    return await Auth.relationship(controller.get, request, link_id)

@link.delete('/{link_id}')
async def delete_link(request: Request, link_id: str):
    return await Auth.relationship(controller.delete, request, link_id)

@link.put('/{link_id}')
async def update_link(request: Request, link_id: str):
    return await Auth.relationship(controller.update, request, link_id)
