import fastapi
import glob
import os
import importlib
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()



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
async def authMiddleware(request : fastapi.Request , call_next):
    response = fastapi.Response(None, 403)
    cookie = request.cookies.get(cookie_name, None)
    print(cookie_name)
    print("cookie",cookie)
