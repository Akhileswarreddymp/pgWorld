from fastapi import APIRouter, HTTPException, Depends
from models import *
from mongo_db import *
import httpx
from typing import Optional
import time
import secrets
import razorpay
import jinja2
import json
from jwt_authorize import *


router = APIRouter(prefix='/payment')

class PaymentRequest(pydantic.BaseModel):
    type_of_service: str

# async def generate_receipt_id():
#     time1 = time.strftime("%Y%m%d%H%M%S")
#     unique_id = secrets.token_hex(4)
#     receipt_id = f"ORD-{time1}-{unique_id}"
#     print("receipt_id ===>", receipt_id)
#     return receipt_id

@router.get('/create_payment', tags=['Payments'])
async def create_payment():
    key_id = "rzp_test_7OEfNThHSPE7Nb"
    key_secret = "TNDKO5lng1XtQ65sDlt0nqw0"
    redis_client = redisclient()
    name  =  redis_client.redis_client.get('name').decode()
    amount = 10
    client = razorpay.Client(auth=(key_id,key_secret))
    order = {
        "amount": amount*100,
        "currency": "INR",
        "receipt": "Pg World",
        "partial_payment":False,
        "notes": {
            "payment_for": "Registeration",
            "name": redis_client.redis_client.get('name').decode()
        }
    }
    order_created = client.order.create(order)
    print("order Created--->",order_created)
    tpl_data=order_created.get("id")
    print(tpl_data)
    return {"request": tpl_data,"name" : name}

class verify_request(pydantic.BaseModel):
    razorpay_order_id : str
    razorpay_payment_id : str
    razorpay_signature : str

@router.post("/verify_payment", tags=['Payments'])
async def verify_payment(request : verify_request):
    if not isinstance(request,dict):
        data1 = request.dict()
    key_id = "rzp_test_7OEfNThHSPE7Nb"
    key_secret = "TNDKO5lng1XtQ65sDlt0nqw0"
    client = razorpay.Client(auth=(key_id,key_secret))
    payment_verify = client.utility.verify_payment_signature({
        'razorpay_order_id': data1.get('razorpay_order_id'),
        'razorpay_payment_id': data1.get('razorpay_payment_id'),
        'razorpay_signature': data1.get('razorpay_signature')
    })
    print("payment_verify",payment_verify)
    if payment_verify == True:
        redis_client = redisclient()
        collection = await connect_collection("Users","users")
        data = {
            "name" : redis_client.redis_client.get('name').decode(),
            "email" : redis_client.redis_client.get('temp_mail').decode(),
            "contact_number" : redis_client.redis_client.get('contact_number').decode(),
            "password" : redis_client.redis_client.get('temp_password').decode(),
            "role" : redis_client.redis_client.get('role').decode(),
            "created_time" : datetime.datetime.now()
        }
        storing_into_mongo = collection.insert_one(data)
        print("registred Successfully")
        return {
                "msg" : "Payment Successful",
                "token" : signJWT(redis_client.redis_client.get("temp_mail"))
            }
    else:
        raise HTTPException(status_code=4010, detail="Wrong Credentials received")