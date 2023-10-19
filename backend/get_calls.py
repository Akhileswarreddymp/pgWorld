from fastapi import APIRouter, HTTPException
from bson import json_util
import json
import asyncio
from mongo_db import *
import pydantic
from typing import List


router = APIRouter()

class query(pydantic.BaseModel):
    query : list[dict]

@router.get('/get_details', tags=['On Board'])
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



