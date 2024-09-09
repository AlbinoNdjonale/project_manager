from fastapi import Request
from fastapi.responses import JSONResponse

from models import User, Token, session

from typing import Coroutine

from utils import Env

env = Env()

class Auth:
    @staticmethod
    def get_user(request: Request):
        if not request.headers.get('WWW-Authenticate'):
            return None

        token = session.query(Token).filter_by(value = request.headers['WWW-Authenticate']).first()

        if not token:
            return None

        user = session.query(User).filter_by(token_id = token.id).first()

        return user
    
    @staticmethod
    async def only_admin(view, request: Request, *args, **kwargs):
        if env.TEST == 'true':
            response = view(request, *args, **kwargs)
            if isinstance(response, Coroutine):
                return await response
            return response
        
        user = Auth.get_user(request)

        if not user:
            return JSONResponse({
                "detail": "Fobidden",
            }, 403)
    
        if not user.is_active:
            return JSONResponse({
                "detail": "Authentication Required",
            }, 407)
        
        if not user.is_admin:
            return JSONResponse({
                "detail": "Not Authorized",
            }, 401)

        response = view(request, *args, **kwargs)
        if isinstance(response, Coroutine):
            return await response
        
        return response
    
    @staticmethod
    async def only_user(view, request: Request, *args, **kwargs):
        if env.TEST == 'true':
            response = view(request, *args, **kwargs)
            if isinstance(response, Coroutine):
                return await response
            return response
        
        user = Auth.get_user(request)

        if not user:
            return JSONResponse({
                "detail": "Fobidden",
            }, 403)
    
        if not user.is_active:
            return JSONResponse({
                "detail": "Authentication Required",
            }, 407)

        response = view(request, *args, **kwargs)
        if isinstance(response, Coroutine):
            return await response
        
        return response
    
    async def authcreateuser(view, request: Request, *args, **kwargs):
        if env.TEST == 'true':
            response = view(request, *args, **kwargs)
            if isinstance(response, Coroutine):
                return await response
            return response
        
        user = Auth.get_user(request)

        data: dict = await request.json()

        if (data.get('is_admin') is not None) and (data.get('is_admin')):
            if (not user):
                return JSONResponse({
                    "detail": "Fobidden",
                }, 403)
    
            if not user.is_active:
                return JSONResponse({
                    "detail": "Authentication Required",
                }, 407)

            if (not user.is_admin):
                if not user.is_admin:
                    return JSONResponse({
                        "detail": "Not Authorized",
                    }, 401)
                
        return await view(request, *args, **kwargs)

    @staticmethod
    async def relationship(view, request: Request, *args, **kwargs):
        if env.TEST == 'true':
            response = view(request, *args, **kwargs)
            if isinstance(response, Coroutine):
                return await response
            return response
        
        user = Auth.get_user(request)
        
        if not user:
            return JSONResponse({
                "detail": "Fobidden",
            }, 403)
    
        if not user.is_active:
            return JSONResponse({
                "detail": "Authentication Required",
            }, 407)
        
        if user.is_admin:
            response = view(request, *args, **kwargs)
            if isinstance(response, Coroutine):
                return await response
            
            return response

        kwargs['token_id'] = user.token_id
        
        response = view(request, *args, **kwargs)
        if isinstance(response, Coroutine):
            return await response
        
        return response