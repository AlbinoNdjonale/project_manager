from controllers import Detail
from fastapi import APIRouter, Request

from utils.auth import Auth

detail = APIRouter()

@detail.get('/{project_id}')
async def get_detail(request: Request, project_id):
    return await Auth.relationship(Detail.get, request, project_id)

@detail.put('/{project_id}')
async def update_detail(request: Request, project_id):
    return await Auth.relationship(Detail.update, request, project_id)

@detail.api_route('/invite/{link}/{project_id}', methods = ['GET', 'PUT'])
async def invite_detail(request: Request, link, project_id):
    return await Detail.invite(request, link, project_id)