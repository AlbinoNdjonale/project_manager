from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse

import models
from models import session
from serializers import USER

from hashlib import sha256

from utils import Utils

from . import base_controller

class User(base_controller.Controller):
    __model__ = models.User
    __model_str__ = 'User'
    __serializer__ = USER

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
        'password': {
            'required': True,
            'type': str
        },
        'is_admin': {
            'required': True,
            'type': bool
        },
        'is_active': {
            'required': False,
            'type': bool | None
        }
    }

    async def create(self, request: Request):
        data = await request.json()

        is_valid, msg =  Utils.validate(data, User.__attr_validate__)

        if not is_valid:
            return JSONResponse(msg, 400)
        
        token = models.Token(value = Utils.generate_token(data['email']))
        session.add(token)
        session.commit()

        date = datetime.now()

        data['last_login']  = date
        data['date_joined'] = date
        data['password']    = sha256(data['password'].encode()).hexdigest()
        data['token_id']    = token.id

        user = models.User(**data)

        session.add(user)

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            session.delete(token)
            session.commit()
            return JSONResponse(e.args, 400)

        return JSONResponse(
            Utils.serializer(user, USER),
            status_code = 201,
            headers = {'Location': f'{request.url}{user.id}'}
        )
    
    def delete(self, request: Request, model_id, token_id = None):
        user: models.User = session.query(models.User).get({'id': model_id})

        if not user:
            return JSONResponse({"msg": f"User not found"}, 404)

        if token_id and (not user.token_id == token_id):
            return JSONResponse({
                "detail": "Not Authorized"
            }, 401)
        
        response = Utils.serializer(user, self.__serializer__)

        session.delete(user.token)
        session.commit()

        return response
