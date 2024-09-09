from datetime import datetime
from fastapi import Request
from fastapi.responses import JSONResponse

import models
from models import session
from serializers import USER

from hashlib import sha256

from utils import Utils

class Auth:
    model = models.User

    async def login(self, request: Request):
        data = await request.json()

        is_valid, msg =  Utils.validate(data, {
            'email': {
                'required': True,
                're': Utils.RE_EMAIL,
                'type': str
            },
            'password': {
                'required': True,
                'type': str
            }
        })

        if not is_valid:
            return JSONResponse(msg, 400)

        data['password'] = sha256(data['password'].encode()).hexdigest()
        
        user: Auth.model = session.query(Auth.model).filter_by(**data).first()

        if not user:
            return JSONResponse({'detail': 'user not found'}, 403)
        
        newtoken = Utils.generate_token(user.email)

        token: models.Token = session.query(models.Token).get({'id': user.token_id})
        token.value = newtoken
        session.add(token)

        user.is_active  = True
        user.last_login = datetime.now()

        session.add(user)

        session.commit()

        return JSONResponse(Utils.serializer(user, USER), headers = {'WWW-Authenticate': newtoken})
    
    def logout(self, request: Request, user_id, token_id = None):
        user: Auth.model = session.query(Auth.model).get({'id': user_id})

        if not user:
            return JSONResponse({"msg": "User not found"}, 404)
        
        if token_id and (not user.token_id == token_id):
            return JSONResponse({
                "detail": "Not Authorized"
            }, 401)
        
        user.is_active = False

        session.add(user)
        session.commit()

        return Utils.serializer(user, USER)