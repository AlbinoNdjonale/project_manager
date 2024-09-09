from starlette.middleware.base import BaseHTTPMiddleware

from utils.auth import Auth
from utils import Utils

from models import Token, session

class UpdateCsrfToken(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        if request.method == 'OPTIONS' or response.status_code in [307, 302]:
            return response

        user = Auth.get_user(request)

        if user:
            newtoken = Utils.generate_token(user.email)

            token: Token = session.query(Token).get({'id': user.token_id})

            token.value = newtoken

            session.add(token)
            session.commit()

            response.headers['WWW-Authenticate'] = newtoken

        return response