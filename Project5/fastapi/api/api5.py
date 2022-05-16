from pydantic import BaseModel
import json
import redis
from fastapi import FastAPI
from pprint import pprint



app = FastAPI()

r = redis.Redis()

@app.get("/gettopusers_redis")
def gettopusers():
	top10user_bywins = r.zrevrange("Win_Sorrted_Set", 0, 9)
	return top10user_bywins





@app.get("/gettopusersbystreaks_redis")
def gettopusersbystreaks():
	top10user_bywins = r.zrevrange("STREAK_Sorted_Set", 0, 9)
	return top10user_bywins

