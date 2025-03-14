from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")

            # print(f"get token: {credentials.credentials}")
            payload = self.verify_jwt(credentials.credentials)
            if payload == None:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")

            uid = payload.get('user_id')
            # print(f"user varified: {uid}")
            if uid == None:
                raise HTTPException(
                    status_code=403, detail="user id not found in token.")
            return uid
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            return decodeJWT(jwtoken)
        except:
            return None
