from fastapi import APIRouter, HTTPException,Depends
from bson import json_util
import json
import asyncio
from mongo_db import *
import pydantic
from typing import List
from jwt_authorize import *
from bson import ObjectId


router = APIRouter() 

class query(pydantic.BaseModel):
    query : list[dict]

@router.get('/get_room_details', tags=['On Board'])
async def get_room_details(request : query):
    query1 = {'$and': request}
    collection = await connect_collection("Room_master","room_master")
    cursor = collection.find(query1)
    results = []

    for document in cursor:
        results.append(document)
    if not results:
        raise HTTPException(status_code=404, detail="No documents found")
    serialized_results = json_util.dumps(results)
    data = json.loads(serialized_results)
    print("data--->",data)
    return data 


@router.get('/get_pg_details', tags=['On Board'])
async def get_pg_details(request : query):
    query1 = {'$and': request}
    collection = await connect_collection("Pg_master","pg_master")
    cursor = collection.find(query1)
    results = []

    for document in cursor:
        results.append(document)
    if not results:
        raise HTTPException(status_code=404, detail="No documents found")
    serialized_results = json_util.dumps(results)
    data = json.loads(serialized_results)
    print("data--->",data)
    return data

@router.get('/get_users',tags=['Users'],dependencies=[Depends(jwtBearer())])
async def get_users():
    collection = await connect_collection("Users","users")
    data = collection.find()
    if data:
        results = []
        for document in data:
            results.append(document)
    else:
        raise HTTPException(status_code=404, detail="No documents found")
    if not results:
        raise HTTPException(status_code=404, detail="No documents found")
    serialized_results = json_util.dumps(results)
    data = json.loads(serialized_results)
    print("data--->",data)
    return data

@router.get('/get_users/{user_id}',tags=['Users'],dependencies=[Depends(jwtBearer())])
async def get_users(userId : str):
    try:
        id_string = userId.decode()
    except:
        id_string = userId

    collection = await connect_collection("Users","users")
    print("userId",userId,type(userId))
    start_index = id_string.find('"') + 1
    end_index = id_string.rfind('"')
    actual_id = id_string[start_index:end_index]
    object_id = ObjectId(actual_id)

    filter = {"_id":object_id}
    print(filter)
    data = collection.find(filter)
    if data:
        results = []
        for document in data:
            results.append(document)
    else:
        raise HTTPException(status_code=404, detail="No documents found")
    if not results:
        raise HTTPException(status_code=404, detail="No documents found")
    serialized_results = json_util.dumps(results)
    data = json.loads(serialized_results)
    print("data--->",data)
    return data


    

