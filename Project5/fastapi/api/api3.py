# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 12:03:29 2022

@author: shind
"""


import sqlite3
import datetime
from fastapi import FastAPI
from pydantic import BaseModel

class ustats(BaseModel):
    user_id : int 
    game_id : int  
    finished : datetime.date = None
    guesses : int
    won : int

class user(BaseModel):
    name : str
    
app = FastAPI()

@app.post("/finduserid")
def finduserid(usr : user):
	
	

@app.get("/getuserstats")
def checkstats(userid : int):
    userstats={}
    conn = sqlite3.connect("var/stats_original.db")
    cur = conn.execute("SELECT count(*) FROM games WHERE user_id = ? LIMIT 1", [userid])
    cur1 = conn.execute("SELECT won FROM games WHERE user_id = ? ORDER BY finished" , [userid])
    cur2 = conn.execute("SELECT streak FROM streaks WHERE user_id = ?" , [userid])  
    cur3 = conn.execute("SELECT Count(won) FROM games WHERE user_id = ? and won=1"  , [userid]) 
    cur4 = conn.execute("SELECT ROUND(AVG(guesses),2) FROM games WHERE user_id = ?"  , [userid]) 
    cur5 = conn.execute("select '1' , count(game_id) from games where won=1 and guesses=1 and user_id=? union select '2' , count(game_id) from games where won=1 and guesses=2 and user_id = ? union select '3' , count(game_id) from games where won=1 and guesses=3 and user_id=? union select '4' , count(game_id) from games where won=1 and guesses=4 and user_id=? union select '5' , count(game_id) from games where won=1 and guesses=5 and user_id=? union select '6' , count(game_id) from games where won=1 and guesses=6 and user_id=? union select 'fail' , count(*) from games where won=0 and  user_id=?" 
                        , (userid,userid,userid,userid,userid,userid,userid))
    out = cur.fetchall()
    out1= cur1.fetchall()
    out2= cur2.fetchall()
    out3= cur3.fetchall()
    out4= cur4.fetchall()
    out5= cur5.fetchall()
    
 
    won=[out1[i][0] for i in range(len(out1))]
    def maxstreak():
        
        sum1=0
        maxsum=0

        for i in won:
   
            if i==1:
                sum1=sum1+i
        
            elif i==0:
                if maxsum<=sum1:
                    maxsum=sum1
                sum1=0
        return(maxsum)  
    
    currentstreak = out2[0][0]
    maxs=maxstreak()
    guesses=dict(out5)
    games_played=out[0][0]
    games_won = out3[0][0]
    avgguesses = out4[0][0]
    winpercentage = round((games_won/games_played)*100,2)

    userstats["currentStreak"]=currentstreak
    userstats["maxs"]=maxs
    userstats["guesses"]=guesses
    userstats["winpercentage"]=winpercentage
    userstats["games_played"]=games_played
    userstats["games_won"]=games_won
    userstats["avgguesses"]=avgguesses
    
    return userstats

@app.get("/gettopusers")
def gettopusers():
    conn = sqlite3.connect("var/stats_original.db")
    cur = conn.execute("select user_id,count(WON) AS WINS from games where won=1 group by user_id ORDER BY WINS DESC LIMIT 10")
    out=cur.fetchall()
    top10=dict(out)
    
    return top10

@app.get("/getlongeststreak")
def getlongeststreak():
    conn = sqlite3.connect("var/stats_original.db")
    cur = conn.execute("select user_id,max(streak) AS streak from streaks group by user_id ORDER BY streak DESC LIMIT 10")
    out=cur.fetchall()
    top10=dict(out)
    
    return top10
    
@app.post("/winloss")
def checkvalidword(ustat : ustats):
        
    s=dict(ustat)
    conn = sqlite3.connect("var/stats_original.db")
    cur = conn.cursor()
    cur.execute("""
            INSERT INTO games(user_id, game_id, finished, guesses, won)
            VALUES(:user_id, :game_id, :finished, :guesses , :won)
            """,
            s)
    conn.commit()
    conn.close()
    return s
            

    
