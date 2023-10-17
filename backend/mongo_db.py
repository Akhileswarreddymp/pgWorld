from pymongo import MongoClient
import pydantic

mongo_client = None

async def connect_to_mongodb():
    global mongo_client

    if mongo_client is None:
        try:
            mongo_client = MongoClient('mongodb://localhost:27017/')
            print("Connected to MongoDB")
        except Exception as e:
            print(f"Error connecting to MongoDB: {str(e)}")

def get_db(db_name):
    if mongo_client is not None:
        return mongo_client[db_name]
    else:
        raise Exception("MongoDB not connected. Call connect_to_mongodb() first.")

# class db_collection(pydantic.BaseModel):
#     database_name : str
#     collection_name : str

async def connect_collection(database_name,collection_name):
    await connect_to_mongodb()
    try:
        database = get_db(database_name)
        collection = database[collection_name]
        return collection
    except Exception as e:
        print(f"Database error: {str(e)}")