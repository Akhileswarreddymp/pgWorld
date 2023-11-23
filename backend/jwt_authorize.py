from typing import Optional
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jwt_auth import * 

class jwtBearer(HTTPBearer):
    def __init__(self, auto_Error :bool = True):
        super(jwtBearer,self).__init__(auto_error=auto_Error)


    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials.scheme == "Bearer":
            print("credentials.scheme", credentials.scheme)
            raise HTTPException(status_code=403, detail="Invalid or Expired Token!!")
        print("credentials.credentials",credentials.credentials)
        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid Token")

        return credentials.credentials
        
    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decodeJWT(jwtoken)
            return True
        except HTTPException:
            return False 