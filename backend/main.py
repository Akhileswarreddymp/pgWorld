from fastapi import FastAPI,HTTPException
import smtplib
import random
from email.message import EmailMessage
import redis
import asyncio
import hashlib
from models import *
import pydantic



app = FastAPI()

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
async def register(data: register_params):
    redis_client = redisclient()
    temp_mail = redis_client.redis_client.setex("temp_mail", 3000, data.username)
    hash_temp_password = hashlib.md5(data.password.encode('utf-8')).hexdigest()
    temp_passwor = redis_client.redis_client.setex("temp_password", 3000, hash_temp_password)
    re_temp_password = hashlib.md5(data.re_password.encode('utf-8')).hexdigest()
    temp_passwor = redis_client.redis_client.setex("re_temp_password", 3000, re_temp_password)
    print("email===>", redis_client.redis_client.get("temp_mail").decode())
    print("passwor===>",redis_client.redis_client.get("temp_password").decode())
    if redis_client.redis_client.get("temp_password") == redis_client.redis_client.get("re_temp_password"):
        await send_otp(redis_client.redis_client.get("temp_mail").decode())
        print("Succesfully registred")
        return {"msg" : "Otp sent Successfully"}
    else:
        return {"msg" : "Passwords are not matching"}
    

# login
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

# pydantic model for saving login details
class only_otp(pydantic.BaseModel):
    otp : str


#send otp to registering mail id after clicking on submit  
@app.post('/reg_otp',tags=['Authentication'])
async def save_login(request : only_otp):
    print(type(request))
    request = dict(request)
    redis_client = redisclient()
    print("reg_otp",redis_client.redis_client.get('otp').decode())
    print("reg_send_otp",request)
    if str(request["otp"]) == str(redis_client.redis_client.get('otp').decode()):
        print("?????")
        mail = redis_client.redis_client.setex("email", 30000, redis_client.redis_client.get("temp_mail"))
        password = redis_client.redis_client.setex("password", 3000, redis_client.redis_client.get("temp_password"))
        return {"msg":"Registred Successfully"}
    else:
        return {"msg":"Wrong otp"}
    

