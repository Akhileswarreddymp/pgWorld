from fastapi import FastAPI,HTTPException
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
async def register(data: verify_params):
    redis_client = redisclient()
    mail = redis_client.redis_client.setex("email", 300, data.username)
    hash_temp_password = hashlib.md5(data.password.encode('utf-8')).hexdigest()
    passwor = redis_client.redis_client.setex("password", 300, hash_temp_password)
    print("email===>", redis_client.redis_client.get("email").decode())
    print("passwor===>",redis_client.redis_client.get("password").decode())
    print("Succesfully registred")


@app.post("/login", tags=['Authentication'])
def verification(request: verify_params):
    redis_client = redisclient()
    print("verification email==>",request.username)
    print("verification password===>",verification)
    passwo = hashlib.md5(request.password.encode('utf-8')).hexdigest()
    if redis_client.redis_client.get("email").decode() == request.username and redis_client.redis_client.get("password").decode() == passwo:
        return {"msg" : "Successfully Logged in "}
    else:
        raise HTTPException(status_code=401, detail="Wrong Credentials received")

