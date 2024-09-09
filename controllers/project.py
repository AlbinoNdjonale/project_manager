from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse

import models
from models import session
from models.connection import db
from serializers import PROJECT

from . import base_controller

from utils import Utils

class Project(base_controller.Controller):
    __model__ = models.Project
    __model_str__ = 'Project'
    __serializer__ = PROJECT
    
    __attr_validate__ = {
        'title': {
            'required': True,
            'type': str
        },
        'description': {
            'required': True,
            'type': str
        },
        'admin_id': {
            'required': True,
            'type': int
        },
        'budget': {
            'type': int | float | None
        },
        'started': {
            'type': str | None
        }
    }

    async def create(self, request: Request, token_id = None):
        data: dict = await request.json()

        is_valid, msg =  Utils.validate(data, Project.__attr_validate__)

        if not is_valid:
            return JSONResponse(msg, 400)
        
        admin: models.User = session.query(models.User).get({'id': data['admin_id']})

        if not admin:
            return JSONResponse({'detail': 'this user not exist'}, 400)
        
        if token_id and (not admin.token_id == token_id):
            return JSONResponse({
                "detail": "Not Authorized"
            }, 401)
        
        data['token_id'] = admin.token_id
        
        if data.get('started'):
            try:
                year, month, day = data['started'].split('-')
                data['started'] = datetime(int(year), int(month), int(day))
            except ValueError:
                return JSONResponse({'detail': 'invalid date'}, 400)
            
        if data.get('budget'):
            data['budget'] = float(data['budget'])

        project = models.Project(**data)

        session.add(project)

        collention = db['details']

        try:
            session.commit()
            collention.insert_one({
                'project_id': project.id,
                'value': {}
            })
        except Exception as e:
            session.rollback()
            return JSONResponse(e.args, 400)
        
        return JSONResponse(
            Utils.serializer(project, PROJECT),
            status_code = 201,
            headers = {'Location': f'{request.url}{project.id}'}
        )
    
    async def update(self, request: Request, project_id, token_id = None):
        data = await request.json()

        attr_validadte = self.__attr_validate__.copy()

        for attr in attr_validadte:
            if 'required' in attr_validadte[attr]:
                del attr_validadte[attr]["required"]

        is_valid, msg =  Utils.validate(data, attr_validadte)

        if not is_valid:
            return JSONResponse(msg, 400)
        
        if data.get('started'):
            year, month, day = data['started'].split('-')
            try:
                data['started'] = datetime(int(year), int(month), int(day))
            except ValueError:
                return JSONResponse({'detail': 'invalid date'}, 400)
            
        if data.get('budget'):
            data['budget'] = float(data['budget'])

        project: models.Project = session.query(models.Project).get({'id': project_id})

        if not project:
            return JSONResponse({"msg": f"Project not found"}, 404)

        if token_id and (not project.token_id == token_id):
            return JSONResponse({
                "detail": "Not Authorized"
            }, 401)

        for attr in data:
            setattr(project, attr, data[attr])

        session.add(project)

        try:
            session.commit()
        except Exception as e:
            return JSONResponse(e.args, 400)

        return Utils.serializer(project, self.__serializer__)
    
    async def delete(self, request: Request, model_id, token_id = None):
        response = super().delete(request, model_id, token_id)

        if isinstance(response, dict):
            collection = db['details']
            collection.delete_one({'project_id': response['id']})

        return response
    
    async def invite(self, request: Request, link):
        link = session.query(models.Link).filter_by(value = link).first()

        if not link:
            return JSONResponse({"msg": "Link not found"}, 404)

        if (not link.write) and (not request.method == 'GET'):
            return JSONResponse({"msg": "Fobidden"}, 403)

        if request.method == 'PUT':
            return await self.update(request, link.project_id)
        
        return self.get(request, link.project_id)