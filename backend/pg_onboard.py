from fastapi import FastAPI,APIRouter
from models import *
from mongo_db import *

router = APIRouter(prefix='/pgonboard')


@router.post('/pg_onboard',tags=['On Board'])
async def pg_onboard(request : Pg_Master):
    if not isinstance(request,dict):
        data = request.dict()
    data_base = await connect_collection("Pg_master","pg_master")
    record = data_base.find_one({"pg_code":data.get("pg_code")})
    print("record====>",record)
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    if not record:
        db_data = {
            "email" : data.get("email"),
            "pg_name" : data.get("pg_name"),
            "pg_code" : data.get("pg_code"),
            "state" : data.get("state"),
            "city" : data.get("city"),
            "pincode": data.get("pincode"),
            "area" : data.get("area"),
            "total_no_of_rooms" : data.get("total_no_of_rooms"),
            "no_of_floors" : data.get("no_of_floors"),
            "no_of_5sharing_rooms":data.get("no_of_5sharing_rooms"),
            "no_of_4sharing_rooms" : data.get("no_of_4sharing_rooms"),
            "no_of_3sharing_rooms" : data.get("no_of_3sharing_rooms"),
            "no_of_2sharing_rooms" : data.get("no_of_2sharing_rooms"),
            "no_of_single_sharing_rooms" : data.get("no_of_single_sharing_rooms"),
            "morethan_5sharing_rooms": data.get("morethan_5sharing_rooms"),
            "cost_of_5sharing" : data.get("cost_of_5sharing"),
            "cost_of_4sharing" : data.get("cost_of_4sharing"),
            "cost_of_3sharing" : data.get("cost_of_3sharing"),
            "cost_of_2sharing" : data.get("cost_of_2sharing"),
            "cost_of_single_sharing" : data.get("cost_of_single_sharing"),
            "cost_for_morethan_5sharing" : data.get("cost_for_morethan_5sharing"),
            "cost_of_5sharing_wof" : data.get("cost_of_5sharing_wof"),
            "cost_of_4sharing_wof" : data.get("cost_of_4sharing_wof"),
            "cost_of_3sharing_wof" : data.get("cost_of_3sharing_wof"),
            "cost_of_2sharing_wof" : data.get("cost_of_2sharing_wof"),
            "cost_of_single_sharing_wof" : data.get("cost_of_single_sharing_wof"),
            "cost_for_morethan_5sharing_wof" : data.get("cost_for_morethan_5sharing_wof"),
        }
        db_data["advance"] = data.get("advance")
        db_data["maintenance_charge"] = data.get("maintenance_charge")
        db_data["negotiable"] = data.get("negotiable")
        db_data["on_boarded_time"] = formatted_datetime

        db_update_data = data_base.insert_one(db_data)
        return {"msg" : "On Borded Successfully"}
    else:
        filter = {"_id":record.get("_id")}
        db_data = {
            "email" : data.get("email"),
            "pg_name" : data.get("pg_name"),
            "pg_code" : data.get("pg_code"),
            "state" : data.get("state"),
            "city" : data.get("city"),
            "pincode": data.get("pincode"),
            "area" : data.get("area"),
            "total_no_of_rooms" : data.get("total_no_of_rooms"),
            "no_of_floors" : data.get("no_of_floors"),
            "no_of_5sharing_rooms":data.get("no_of_5sharing_rooms"),
            "no_of_4sharing_rooms" : data.get("no_of_4sharing_rooms"),
            "no_of_3sharing_rooms" : data.get("no_of_3sharing_rooms"),
            "no_of_2sharing_rooms" : data.get("no_of_2sharing_rooms"),
            "no_of_single_sharing_rooms" : data.get("no_of_single_sharing_rooms"),
            "morethan_5sharing_rooms": data.get("morethan_5sharing_rooms"),
            "cost_of_5sharing" : data.get("cost_of_5sharing"),
            "cost_of_4sharing" : data.get("cost_of_4sharing"),
            "cost_of_3sharing" : data.get("cost_of_3sharing"),
            "cost_of_2sharing" : data.get("cost_of_2sharing"),
            "cost_of_single_sharing" : data.get("cost_of_single_sharing"),
            "cost_for_morethan_5sharing" : data.get("cost_for_morethan_5sharing"),
            "cost_of_5sharing_wof" : data.get("cost_of_5sharing_wof"),
            "cost_of_4sharing_wof" : data.get("cost_of_4sharing_wof"),
            "cost_of_3sharing_wof" : data.get("cost_of_3sharing_wof"),
            "cost_of_2sharing_wof" : data.get("cost_of_2sharing_wof"),
            "cost_of_single_sharing_wof" : data.get("cost_of_single_sharing_wof"),
            "cost_for_morethan_5sharing_wof" : data.get("cost_for_morethan_5sharing_wof"),
            
        }
        db_data["advance"] = data.get("advance")
        db_data["maintenance_charge"] = data.get("maintenance_charge")
        db_data["negotiable"] = data.get("negotiable") 
        db_data["updated_time"] = formatted_datetime
        db_data["total_vacant"] = data.get("total_vacancy")
        db_update = data_base.update_one(filter, {'$set': db_data})
        return {"msg":"updated"}



    
