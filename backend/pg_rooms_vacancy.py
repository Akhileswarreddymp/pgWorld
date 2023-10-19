from fastapi import APIRouter,HTTPException
from models import *
from mongo_db import *
import datetime
import pymongo
from bson import json_util
import json
from get_calls import *

router = APIRouter()

@router.post('/vacant_rooms',tags=['On Board'])
async def no_of_room_vacant(request : room_master):
    if not isinstance(request,dict):
        data = request.dict()
    data_base = await connect_collection("Room_master","room_master")
    record = data_base.find_one({"pg_code":data.get("pg_code")})
    

    d_base = await connect_collection("Pg_master","pg_master")
    record1 = d_base.find_one({"pg_code":data.get("pg_code")})

    print("record====>",record)
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    if record1:
        db_data = {
            "pg_name" : data.get("pg_name"),
            "pg_code" : data.get("pg_code"),
            "room_number" : data.get("room_number"),
            "no_of_sharing" : data.get("no_of_sharing"),
            "no_of_occupied_beds" : data.get("no_of_occupied_beds"),
            "no_of_vacant_beds" : data.get("no_of_vacant_beds")
        }
        db_data["status"] = {
            "available" : False,
            "unavailable" : False
        }
        
        total_vacent = 0
        try:
            db_query = await get_room_details([{"pg_name": data.get("pg_name")},{"pg_code" : data.get("pg_code")}])
            print("db_query===>",db_query)
            if db_query:
                for i in db_query:
                    total_vacent += i["no_of_vacant_beds"]
                    total_vacent +=  data.get("no_of_vacant_beds")
                print("total_in_if====>",total_vacent)
        except Exception as e:
            print("exception_raised===>",e)
            total_vacent = data.get("no_of_vacant_beds")
            print("total_vacant_in_else==>",total_vacent)
        data_base1 = await connect_collection("Pg_master","pg_master")
        result = data_base1.find_one({"pg_code": data.get("pg_code")})
        result["total_vacant"] = total_vacent
        db_update = data_base1.update_one({"pg_code": data.get("pg_code")}, {'$set': result})
        db_update_data = data_base.insert_one(db_data)
        return {"msg" : "room details onboarded Successfully"}
    else:
        filter = {"_id":record.get("_id")}
        db_data = {
            "pg_name" : data.get("pg_name"),
            "pg_code" : data.get("pg_code"),
            "room_number" : data.get("room_number"),
            "no_of_sharing" : data.get("no_of_sharing"),
            "no_of_occupied_beds" : data.get("no_of_occupied_beds"),
            "no_of_vacant_beds" : data.get("no_of_vacant_beds")
        }
        db_data["status"] = {
            "available" : False,
            "unavailable" : False
        }
        total_vacent = 0
        db_data["description"] = data.get("description")
        try:
            db_query = await get_room_details([{"pg_name": data.get("pg_name")},{"pg_code" : data.get("pg_code")}])
            print("db_query===>",db_query)
            if db_query:
                for i in db_query:
                    total_vacent += i["no_of_vacant_beds"]
                    total_vacent +=  data.get("no_of_vacant_beds")
                print("total_in_if====>",total_vacent)
        except Exception as e:
            print("exception_raised===>",e)
            total_vacent = data.get("no_of_vacant_beds")
            print("total_vacant_in_else==>",total_vacent)
        data_base1 = await connect_collection("Pg_master","pg_master")
        result = data_base1.find_one({"pg_code": data.get("pg_code")})
        result["total_vacant"] = total_vacent
        db_update = data_base1.update_one({"pg_code": data.get("pg_code")}, {'$set': result})
        db_update_data = data_base.update_one(filter, {'$set': db_data})
        return {"msg" : "room details updated Successfully"}
    


