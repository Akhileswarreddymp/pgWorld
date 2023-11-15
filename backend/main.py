from fastapi import FastAPI,HTTPException
import smtplib
import random
from email.message import EmailMessage
import redis
import asyncio
import hashlib
from models import *
import pydantic
import pymongo
from Authentication import router as register_app
from mongo_db import *
from pg_onboard import router as pg_onboard_app
from update_user import router as user_update_app
from pg_rooms_vacancy import router as pg_room_vacancy_app
from get_calls import router as get_calls_app
from add_attachments import router as add_attachments_app
from fastapi.middleware.cors import CORSMiddleware
from payments import router as payments_app
from video_calls import router as video_call_app

app = FastAPI()

app.include_router(register_app)
app.include_router(pg_onboard_app)
app.include_router(user_update_app)
app.include_router(pg_room_vacancy_app)
app.include_router(get_calls_app)
app.include_router(add_attachments_app)
app.include_router(payments_app)
app.include_router(video_call_app)

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



    

