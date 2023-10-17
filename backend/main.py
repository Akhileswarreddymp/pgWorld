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
from register_user import router as register_app
from mongo_db import *


app = FastAPI()

app.include_router(register_app)


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


#step 1 in registering 
@app.post("/register", tags=['Authentication'])
async def register(data: register_params,request : register):
    redis_client = redisclient()
    temp_mail = redis_client.redis_client.setex("temp_mail", 3000, data.username)
    hash_temp_password = hashlib.md5(data.password.encode('utf-8')).hexdigest()
    temp_passwor = redis_client.redis_client.setex("temp_password", 3000, hash_temp_password)
    re_temp_password = hashlib.md5(data.re_password.encode('utf-8')).hexdigest()
    temp_passwor = redis_client.redis_client.setex("re_temp_password", 3000, re_temp_password)
    print("email===>", redis_client.redis_client.get("temp_mail").decode())
    # client = pymongo.MongoClient("mongodb://localhost:27017/")
    # collection = client.get_database("Users").get_collection("users")
    collection = await connect_collection("Users","users")
    result = collection.find_one({"email": data.username})
    print("result_register====>",result)
    if result:
        return {
            "msg":"user already exist"
        }
    print("passwor===>",redis_client.redis_client.get("temp_password").decode())
    if redis_client.redis_client.get("temp_password") == redis_client.redis_client.get("re_temp_password"):
        await send_otp(redis_client.redis_client.get("temp_mail").decode())
        name = redis_client.redis_client.setex("name",300,request.name)
        contact_number = redis_client.redis_client.setex("contact_number",300,request.contact_number)
        print("Succesfully registred")
        return {"msg" : "Otp sent Successfully"}
    else:
        return {"msg" : "Passwords are not matching"}
    




    

