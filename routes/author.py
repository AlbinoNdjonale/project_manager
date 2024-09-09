from fastapi import APIRouter, Request
from controllers import Author

from utils.auth import Auth

author = APIRouter()
controller = Author()

@author.post('/')
async def insert_author(request: Request):
    return await Auth.relationship(controller.create, request)

@author.get('/{author_id}')
async def get_author(request: Request, author_id):
    return await Auth.relationship(controller.get, request, author_id)

@author.delete('/{author_id}')
async def delete_author(request: Request, author_id: str):
    return await Auth.relationship(controller.delete, request, author_id)

@author.post('/invite/{link}')
@author.delete('/invite/{link}/{author_id}')
async def invite_author(request: Request, link, author_id: str = None):
    return await controller.invite(request, link, author_id)
