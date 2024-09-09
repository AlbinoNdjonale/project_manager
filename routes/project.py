from fastapi import APIRouter, Request
from controllers import Project

from utils.auth import Auth

project = APIRouter()
controller = Project()

@project.post('/')
async def insert_project(request: Request):
    return await Auth.relationship(controller.create, request)

@project.get('/{project_id}')
async def get_project(request: Request, project_id):
    return await Auth.relationship(controller.get, request, project_id)

@project.delete('/{project_id}')
async def delete_project(request: Request, project_id: str):
    return await Auth.relationship(controller.delete, request, project_id)

@project.put('/{project_id}')
async def update_project(request: Request, project_id):
    return await Auth.relationship(controller.update, request, project_id)

@project.api_route('/invite/{link}', methods = ['GET', 'PUT'])
async def invite_project(request: Request, link = None):
    return await controller.invite(request, link)