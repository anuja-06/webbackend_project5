import sqlite3
import redis
import json
import redis
from pprint import pprint
from collections import defaultdict

r = redis.Redis()


#Connecting to shards 1,2,3
conn1 = sqlite3.connect("var/shard1.db")

conn2 = sqlite3.connect("var/shard2.db")

conn3 = sqlite3.connect("var/shard3.db")

#Retriving records top 10 records from each shard
cur1 = conn1.execute("SELECT * FROM wins LIMIT 10")
cur2 = conn2.execute("SELECT * FROM wins LIMIT 10")
cur3 = conn3.execute("SELECT * FROM wins LIMIT 10")

cur4 = conn1.execute("SELECT * FROM streaks LIMIT 10")
cur5 = conn2.execute("SELECT * FROM streaks LIMIT 10")
cur6 = conn3.execute("SELECT * FROM streaks LIMIT 10")

out1=cur1.fetchall()
out2=cur2.fetchall()
out3=cur3.fetchall()

out4=cur4.fetchall()
out5=cur5.fetchall()
out6=cur6.fetchall()


#Creating Dict for 30 entries of user wins
wins1=dict(out1)
wins2=dict(out2)
wins3=dict(out3)

WINS={}
WINS.update(wins1)
WINS.update(wins2)
WINS.update(wins3)


#Adding userid to Sorted Set of Redis
r.zadd("Win_Sorrted_Set", WINS)



streak= []
streak.extend(out4)
streak.extend(out5)
streak.extend(out6)
#dictionary of user id -streaks-start-end date
d = {}

#dict for only streaks
strx = {}

for userid,streaks,max_start_date,max_end_date in streak:
    if userid not in d:
        d[userid] = []
        strx[userid] = []
    d[userid].append((streaks ,max_start_date , max_end_date ))
    strx[userid].append(streaks)
    
mdict= {}
i = 1
for k,v in d.items():
    for val in v:
        tdict = {'streaks': val[0], 'start-date' : val[1], 'end-date' : val[2]}
        mdict[i] = tdict
        i += 1

stx = {}
for key, val in d.items():
    strx[key] = max(strx[key])

r.zadd("STREAK_Sorted_Set", strx)







