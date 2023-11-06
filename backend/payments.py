from fastapi import APIRouter, HTTPException
from models import *
from mongo_db import *
import httpx
from typing import Optional
import time
import secrets
import razorpay
import jinja2
import json


router = APIRouter()

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
    
    amount = 10000
    client = razorpay.Client(auth=(key_id,key_secret))
    order = {
        "amount": amount*100,
        "currency": "INR",
        "receipt": "Pg World",
        "partial_payment":False,
        "notes": {
            "payment_for": "Registeration",
            "name": "Akhil"
        }
    }
    order_created = client.order.create(order)
    print("order Created--->",order_created)
    tpl_data=order_created.get("id")
    return {"request": tpl_data}

@router.post("/verify_payment", tags=['Payments'])
async def verify_payment():
    key_id = "rzp_test_7OEfNThHSPE7Nb"
    key_secret = "TNDKO5lng1XtQ65sDlt0nqw0"
    client = razorpay.Client(auth=(key_id,key_secret))
    data1 = {"razorpay_payment_id": 'pay_Mv3vZbp0N5wvqF', 'razorpay_order_id': 'order_Mv3th6YugCQpXd', "razorpay_signature": '620d1e407e48f6d533559a74714c1b4155d3142203ffb4f03b223feb56b08c0e'}
    payment_verify = client.utility.verify_payment_signature({
        'razorpay_order_id': data1.get('razorpay_order_id'),
        'razorpay_payment_id': data1.get('razorpay_payment_id'),
        'razorpay_signature': data1.get('razorpay_signature')
    })
    print("payment_verify",payment_verify)
    if payment_verify == True:
        return {"msg" : "Payment Successful"}
    else:
        return {"msg" : "Payment Failed"}