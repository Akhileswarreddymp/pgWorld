from fastapi import APIRouter,HTTPException
from models import *
from mongo_db import *
import hashlib
from Authentication import *


router = APIRouter()



#step 1 in registering 
@router.post("/user_register", tags=['Users'])
async def register(data: register_params,request : user_register):
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
    
# pydantic model for saving login details
class only_otp(pydantic.BaseModel):
    otp : str

# Registering the user after verifying Otp
@router.post('/verify_user_otp',tags=['Users'])
async def verify_otp(request : only_otp):
    print(type(request))
    request = dict(request)
    redis_client = redisclient()
    print("reg_otp",redis_client.redis_client.get('otp').decode())
    print("reg_send_otp",request)
    if str(request["otp"]) == str(redis_client.redis_client.get('otp').decode()):
        print("?????")
        # client = pymongo.MongoClient("mongodb://localhost:27017/")
        # db = client["Users"] 
        # collection = db["users"]
        collection = await connect_collection("Users","users")
        data = {
            "name" : redis_client.redis_client.get('name').decode(),
            "email" : redis_client.redis_client.get('temp_mail').decode(),
            "contact_number" : redis_client.redis_client.get('contact_number').decode(),
            "password" : redis_client.redis_client.get('temp_password').decode(),
            "created_time" : datetime.datetime.now()
        }
        storing_into_mongo = collection.insert_one(data)

    #     mail = redis_client.redis_client.setex("email", 30000, redis_client.redis_client.get("temp_mail"))
    #     password = redis_client.redis_client.setex("password", 3000, redis_client.redis_client.get("temp_password"))
        return {"msg":"Registred Successfully"}
    else:
        raise HTTPException(status_code=401, detail="Wrong Credentials received")
    

class user_id(pydantic.BaseModel):
    email : str 


@router.post('/update_user',tags=['Users'])
async def update_user(data1 : user_id,request : user_register):
    data = request.dict()
    collection = await connect_collection("Users","users")
    result = collection.find_one({"email": data1.email})
    filter = {"_id":result.get("_id")}
    result = collection.find_one(filter)
    print("updated_result--->",result)
    if result:
        updated_data = {
            "name" : data.get("name"),
            "contact_number" : data.get("contact_number"),
            "updated_time" : datetime.datetime.now()
        }
        db_update = collection.update_one(filter, {'$set': updated_data})
        return {"msg" : "updated Successfully"}
    else:
        raise HTTPException(status_code=403, detail="Wrong Credentials received")