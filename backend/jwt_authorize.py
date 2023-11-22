from typing import Optional
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jwt_auth import * 

class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error :bool = True):
        super(jwtBearer,self).__init__(auto_error=auto_Error)


    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials : HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403,detail="Invalid or Expired Token!!")
            return credentials.credentials
        else:
           raise HTTPException(status_code=403,detail="Invalid or Expired Token!!")
        
    def verify_jwt(self,jwtoken : str):
        isTokenValid : bool = False
        payload = decodeJWT(jwtoken)
        if payload:
            isTokenValid = True
        return isTokenValid

         