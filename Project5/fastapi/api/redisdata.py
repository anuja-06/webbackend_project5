import json
import redis
from pprint import pprint

r = redis.Redis()

fileobj = open('var/less10.json')

userdatadict =json.load(fileobj)


(r.set("track_user", json.dumps(userdatadict)))

usersbytes = r.get("track_user")
userstr = usersbytes.decode("utf-8")
userdict = json.loads(userstr)


#SET the data in redis
r.set("track_user", json.dumps(userdict))


#Retrive data from redis
usersbytes = r.get("track_user")
userstr = usersbytes.decode("utf-8")
userdict = json.loads(userstr)



