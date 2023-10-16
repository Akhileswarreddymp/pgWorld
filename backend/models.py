import redis 
import pydantic
import typing
import datetime

class redisclient():
    def __init__(self) -> None:
        self.redis_host = 'localhost'
        self.redis_port = 6379
        self.redis_db = 0
        self.redis_client = redis.Redis(host=self.redis_host, port=self.redis_port, db=self.redis_db)

class register_params(pydantic.BaseModel):
    username : str
    password : str
    re_password : str

class verify_params(pydantic.BaseModel):
    username : str
    password : str


class ratings_internal_model(pydantic.BaseModel):
    food_rating : typing.Optional[float]
    cleaning : typing.Optional[float]
    maintenance : typing.Optional[float]
    water_facility : typing.Optional[float]
    freedom : typing.Optional[float]
    worth_for_money : typing.Optional[float]
    over_all_rating : typing.Optional[float]


class review_internalmodel(pydantic.BaseModel):
    review : typing.List[str]

class occupancy_vacancy(pydantic.BaseModel):
    occupied : int
    vacant : int


class Pg_Master(pydantic.BaseModel):
    pg_name : str = pydantic.Field("",**{})
    pg_code : str = pydantic.Field("",**{})
    state : str = pydantic.Field("", **{})
    city : str = pydantic.Field("", **{})
    pincode : int = pydantic.Field(0, **{})
    area : str = pydantic.Field("", **{})
    total_no_of_rooms : int = pydantic.Field(0, **{})
    no_of_floors : int = pydantic.Field(0, **{})
    no_of_5sharing_rooms : int = pydantic.Field(0, **{})
    no_of_4sharing_rooms : int = pydantic.Field(0, **{})
    no_of_3sharing_rooms : int = pydantic.Field(0, **{})
    no_of_2sharing_rooms : int = pydantic.Field(0, **{})
    no_of_single_sharing_rooms : int = pydantic.Field(0, **{})
    morethan_5sharing_rooms : typing.Optional[int] = pydantic.Field("", **{})
    cost_of_5sharing : float = pydantic.Field(0.0, **{})
    cost_of_3sharing : float = pydantic.Field(0.0, **{})
    cost_of_2sharing : float = pydantic.Field(0.0, **{})
    cost_of_single_sharing : float = pydantic.Field(0.0, **{})
    cost_for_morethan_5sharing : typing.Optional[float] = pydantic.Field(0.0, **{})
    cost_of_5sharing_wof : float = pydantic.Field(0.0, **{})
    cost_of_4sharing_wof : float = pydantic.Field(0.0, **{})
    cost_of_3sharing_wof : float = pydantic.Field(0.0, **{})
    cost_of_2sharing_wof : float = pydantic.Field(0.0, **{})
    cost_of_single_sharing_wof : float = pydantic.Field(0.0, **{})
    cost_for_morethan_5sharing_wof : typing.Optional[float] = pydantic.Field(0.0, **{})
    overall_rating : typing.Optional[ratings_internal_model]
    reviews : typing.Optional[review_internalmodel]
    advance : typing.Optional[float] = pydantic.Field(0.0, **{})
    maintenance_charge : typing.Optional[float] = pydantic.Field(0.0, **{})
    negotiable : typing.Optional[bool] = pydantic.Field(False, )

class status_internal_model(pydantic.BaseModel):
    available : bool = pydantic.Field(False, ) 
    unavailabe : bool = pydantic.Field(False, )

class room_master(pydantic.BaseModel):
    pg_name : str = pydantic.Field("",**{})
    pg_code : str
    room_number : str = pydantic.Field("",**{})
    no_of_sharing : int = pydantic.Field(0,**{})
    no_of_occupied_beds : int = pydantic.Field(0,**{})
    no_of_vacent_beds : int = pydantic.Field(0,**{})
    description : typing.List[str]
    status : status_internal_model



class register(pydantic.BaseModel):
    name : str = pydantic.Field("",**{})
    contact_number : int = pydantic.Field(0,**{})
    role : str = typing.Optional[str]
    created_time : typing.Optional[datetime.datetime] = pydantic.Field()
    updated_time : typing.Optional[datetime.datetime] = pydantic.Field()
    profile_pic : typing.Optional[str] = pydantic.Field("",**{})


    
    