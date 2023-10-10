from fastapi import FastAPI
import smtplib
import random
from email.message import EmailMessage
import redis
import asyncio
import hashlib
from models import *



app = FastAPI()


@app.get("/send_otp", tags=["Authentication"])
async def send_otp():
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
    s.sendmail("akhileswarreddymp@gmail.com", "mpakhileswarreddy@gmail.com", message)
    print("Mail sent sucessfully")
    # terminating the session
    s.quit()
    store = await redis_store(otp_generated)



async def redis_store(otp):
    redis_client = redisclient()
    key = 'otp'
    value = otp
    ttl = 300
    redis_client.redis_client.setex(key, ttl, value)
    print("opt saved==>",redis_client.redis_client.get(key))



@app.post("/register", tags=['Authentication'])
def register(username,password):
    redis_client = redisclient()
    mail = redis_client.redis_client.setex("email", 300, username)
    passwor = redis_client.redis_client.setex("password", 300, password)
    print("email===>", redis_client.redis_client.get("email").decode())
    print("passwor===>",redis_client.redis_client.get("password").decode())
    print("Succesfully registred")


@app.post("/login", tags=['Authentication'])
def verification(username,password):
    redis_client = redisclient()
    print("verification email==>",username)
    print("verification password===>",verification)
    if redis_client.redis_client.get("email").decode() == username and redis_client.redis_client.get("password").decode() == password:
        return {"msg" : "Successfully Logged in "}
    else:
        return {"msg" : "Wrong Credentials received"}

