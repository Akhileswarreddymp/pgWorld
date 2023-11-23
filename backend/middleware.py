import fastapi
import glob
import json
import os
import importlib
from fastapi.middleware.cors import CORSMiddleware
from models import *
import base64
app = fastapi.FastAPI()

cookie_name = "Akhil"

#api routing
@app.on_event("startup")
def onStart():
    for filename in glob.glob("**/*.py", recursive=True):
        if filename.startswith("."):
            continue
        #get all the file in the directory
        modname = os.path.splitext(filename)[0].replace(os.sep, '.')
        #get file path using importlib
        mod = importlib.import_module(modname)
        # to get attr named router 
        symbol = getattr(mod, 'router', None)
        if isinstance(symbol, fastapi.APIRouter):
            app.include_router(symbol, prefix="/api")
        else:
            for attr in dir(mod):
                if not attr.startswith("_"):
                    symbol = getattr(mod, attr)
                    if isinstance(symbol, fastapi.APIRouter):
                        app.include_router(symbol, prefix="/api")


onStart()

origins = [
    "http://localhost",
    "http://localhost:8001",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5501"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.middleware('http')
async def authMiddleware(request: fastapi.Request, call_next):
    payload_data = request.json()
    print("payload_data====>",payload_data)
    print(request.method)
    response = fastapi.Response(None, status_code=403)
    allowed_paths = [
        '/api/login',
        '/api/user/verify_user_otp',
        '/api/user/user_register',
        '/api/payment/create_payment',
        '/api/payment/verify_payment',
        '/api/send_otp',
        "/docs",
        "/openapi.json",
        
    ]
    if request.method == "OPTIONS":
        return await call_next(request)
    if request.url.path in allowed_paths:
        return await call_next(request)
    
    cookie_value = request.cookies.get(cookie_name)
    print("request_headers=",request.headers)
    print(f"Cookie Name: {cookie_name}")
    print(f"Cookie Value: {cookie_value}")

    if not cookie_value:
        redirect_url = f"https://{request.base_url.hostname}/login"
        print("redirect_url",redirect_url)
        # response: fastapi.responses.Response = await call_next(request)
        response = fastapi.responses.JSONResponse({'url': redirect_url}, status_code=401)

    return response



# @app.middleware('http')
# async def contextMiddleware(request: fastapi.Request, call_next):
#     print("request=======----->",request)
#     data = {}
#     data["domain"] = request.base_url
#     data["tenant"] = "PG WORLD"
#     data['oauth_redirect'] = f'{request.base_url}api/login'
#     print("data====>",data)
#     print("request.cookies====>",request.cookies)
#     cookie_id = request.cookies.get(cookie_name, None)
#     print("cookie_id", cookie_id)

#     if cookie_id:
#         redis_client = redisclient()
#         cookie = redis_client.redis_client.hget("CookieStore", cookie_id)
#         if cookie:
#             if isinstance(cookie, bytes):
#                 cookie = cookie.decode()
#             data["rpt"] = json.loads(base64.urlsafe_b64decode(cookie.split('.')[1] + '=====').decode())

#     respo = None

#     try:
#         respo = await call_next(request)
#     except Exception as error:
#         import traceback
#         traceback.print_exc()
#         print("error=====>", error)

#     return respo or fastapi.responses.PlainTextResponse("Internal Server Error", status_code=500)


