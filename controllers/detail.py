from fastapi import Request
from fastapi.responses import JSONResponse

import models
from models.connection import db
from models import session, Project

class Detail:
    def get(request: Request, project_id, token_id = None):
        collection = db['details']

        project: Project = session.query(Project).get({'id': project_id})

        if not project:
            return JSONResponse({'detail': 'Project not found'}, 404)

        if token_id and (not project.token_id == token_id):
            return JSONResponse({
                "detail": "Not Authorized"
            }, 401)
        
        details: dict = collection.find_one({'project_id': int(project_id)})
        
        if details:
            return details['value']
        
        return None
    
    async def update(request: Request, project_id, token_id = None):
        collection = db['details']

        project: Project = session.query(Project).get({'id': project_id})

        if not project:
            return JSONResponse({'detail': 'Project not found'}, 404)

        if token_id and (not project.token_id == token_id):
            return JSONResponse({
                "detail": "Not Authorized"
            }, 401)
        
        data = await request.json()
        
        collection.update_one(
            {"project_id": int(project_id)},
            {
                "$set": {"value": data}
            }
        )

        details: dict = collection.find_one({'project_id': int(project_id)})
        
        if details:
            return details['value']
        
        return None
    
    async def invite(request: Request, link, project_id):
        link = session.query(models.Link).filter_by(value = link).first()

        if not link:
            return JSONResponse({"msg": "Link not found"}, 404)
        
        if (not link.write) and (not request.method == 'GET') or\
        (not project_id == str(link.project_id)):
            return JSONResponse({"msg": "Fobidden"}, 403)
        
        if request.method == 'PUT':
            return await Detail.update(request, link.project_id)
        
        return Detail.get(request, link.project_id)