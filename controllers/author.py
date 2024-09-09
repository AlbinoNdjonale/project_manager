from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse

import models
from models import session
from serializers import AUTHOR

from utils import Utils

from . import base_controller

class Author(base_controller.Controller):
    __model__ = models.Author
    __model_str__ = 'Author'
    __serializer__ = AUTHOR

    __attr_validate__ = {
        'name': {
            'required': True,
            'type': str
        },
        'email': {
            'required': True,
            're': Utils.RE_EMAIL,
            'type': str
        },
        'birth': {
            'required': True,
            'type': str
        },
        'gender': {
            'required': True,
            'type': str,
            'values': ['M', 'F']
        },
        'project_id': {
            'required': True,
            'type': int
        }
    }

    async def create(self, request: Request, token_id = None):
        data = await request.json()

        is_valid, msg =  Utils.validate(data, Author.__attr_validate__)

        project: models.Project = session.query(models.Project).get({'id': data['project_id']})

        if not project:
            return JSONResponse({'detail': 'this project not exist'}, 400)

        if token_id and (not project.token_id == token_id):
            return JSONResponse({
                "detail": "Not Authorized"
            }, 401)

        data['token_id'] = project.token_id
        
        if not is_valid:
            return JSONResponse(msg, 400)
        
        try:
            year, month, day = data['birth'].split('-')
            data['birth'] = datetime(int(year), int(month), int(day))
        except ValueError:
            return JSONResponse({'detail': 'invalid date'}, 400)
        
        author = models.Author(**data)

        session.add(author)

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            return JSONResponse(e.args, 400)
        
        return JSONResponse(
            Utils.serializer(author, AUTHOR),
            status_code = 201,
            headers = {'Location': f'{request.url}{author.id}'}
        )
    
    async def invite(self, request: Request, link, author_id):
        link = session.query(models.Link).filter_by(value = link).first()

        if not link:
            return JSONResponse({"msg": "Link not found"}, 404)
            
        if ((not link.write) and (not request.method == 'GET')) or\
        (author_id and (author_id not in [str(author.id) for author in link.project.authors])):
            return JSONResponse({"msg": "Fobidden"}, 403)
        
        if request.method == 'DELETE':
            return self.delete(request, author_id)
            
        return await self.create(request)