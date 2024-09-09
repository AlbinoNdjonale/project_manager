from fastapi import Request
from fastapi.responses import JSONResponse

import models
from models import session
from serializers import LINK

from . import base_controller

from utils import Utils

class Link(base_controller.Controller):
    __model__ = models.Link
    __model_str__ = 'Link'
    __serializer__ = LINK
    
    __attr_validate__ = {
        'write': {
            'required': True,
            'type': bool
        },
        'project_id': {
            'required': True,
            'type': int
        }
    }

    async def create(self, request: Request, token_id = None):
        data: dict = await request.json()

        is_valid, msg =  Utils.validate(data, Link.__attr_validate__)

        if not is_valid:
            return JSONResponse(msg, 400)
        
        project: models.Project = session.query(models.Project).get({'id': data['project_id']})

        if not project:
            return JSONResponse({'detail': 'this project not exist'}, 400)
        
        if token_id and (not project.token_id == token_id):
            return JSONResponse({
                "detail": "Not Authorized"
            }, 401)
        
        data['token_id'] = project.token_id
        data['value']    = Utils.generate_token('')

        link = models.Link(**data)

        session.add(link)

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            return JSONResponse(e.args, 400)
        
        return JSONResponse(
            Utils.serializer(link, LINK),
            status_code = 201,
            headers = {'Location': f'{request.url}{link.id}'}
        )