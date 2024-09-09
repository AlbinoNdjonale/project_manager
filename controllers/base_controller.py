from fastapi import Request
from fastapi.responses import JSONResponse

from models import session

from utils import Utils

class Controller:
    async def create(self, request: Request):
        data = await request.json()

        is_valid, msg =  Utils.validate(data, self.attr_validadte)

        if not is_valid:
            return JSONResponse(msg, 400)
        
        model = self.__model__(**data)

        session.add(model)

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            return JSONResponse(e.args, 400)
        
        return JSONResponse(
            Utils.serializer(model, self.__serializer__),
            status_code = 201,
            headers = {'Location': f'{request.url}{model.id}'}
        )
    
    def get(self, request: Request, model_id, token_id = None):
        model = session.query(self.__model__).get({'id': model_id})

        if not model:
            return JSONResponse({"msg": f"{self.__model_str__} not found"}, 404)
        
        if token_id and (not model.token_id == token_id):
            return JSONResponse({
                "detail": "Not Authorized"
            }, 401)
        
        return Utils.serializer(model, self.__serializer__)
    
    def delete(self, request: Request, model_id, token_id = None):
        model = session.query(self.__model__).get({'id': model_id})

        if not model:
            return JSONResponse({"msg": f"{self.__model_str__} not found"}, 404)

        if token_id and (not model.token_id == token_id):
            return JSONResponse({
                "detail": "Not Authorized"
            }, 401)
        
        response = Utils.serializer(model, self.__serializer__)

        session.delete(model)
        session.commit()

        return response
    
    async def update(self, request: Request, model_id, token_id = None):
        model = session.query(self.__model__).get({'id': model_id})

        if not model:
            return JSONResponse({"msg": f"{self.__model_str__} not found"}, 404)
        
        if token_id and (not model.token_id == token_id):
            return JSONResponse({
                "detail": "Not Authorized"
            }, 401)
        
        data: dict = await request.json()

        attr_validadte = self.__attr_validate__.copy()

        for attr in attr_validadte:
            if 'required' in attr_validadte[attr]:
                del attr_validadte[attr]["required"]

        is_valid, msg =  Utils.validate(data, attr_validadte)

        if not is_valid:
            return JSONResponse(msg, 400)

        for attr in data:
            setattr(model, attr, data[attr])

        session.add(model)
        
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            return JSONResponse(e.args, 400)

        return Utils.serializer(model, self.__serializer__)
    