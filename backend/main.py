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


app = FastAPI()

app.include_router(register_app)
app.include_router(pg_onboard_app)
app.include_router(user_update_app)


# send otp to mail id 
@app.post("/send_otp", tags=["Authentication"])
async def send_otp(request: str):
    print("send_mail_data",request)
    otp_generated = random.randint(10000,99999)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    s.login("akhileswarreddymp@gmail.com", "xodgydwslhywjare")
    message = EmailMessage()
    message["Subject"] = "Verificaion code to change password"
    # message to be sent
    message = f"Your verification cod is {otp_generated}"
    s.subject = "Verification code"
    # sending the mail
    s.sendmail("akhileswarreddymp@gmail.com",request, message)
    print("akhileswarreddymp@gmail.com", request, message)
    print("Mail sent sucessfully")
    # terminating the session
    s.quit()
    store = await redis_store(otp_generated)
    return None


# store otp in redis 
async def redis_store(otp):
    redis_client = redisclient()
    key = 'otp'
    value = otp
    ttl = 3000
    redis_client.redis_client.setex(key, ttl, value)
    print("opt saved==>",redis_client.redis_client.get(key))






    

