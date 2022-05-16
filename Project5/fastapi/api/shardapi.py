# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 20:44:25 2022

@author: CSUFTitan
"""

import sqlite3
import uuid
import functools
import pandas as pd
from fastapi import FastAPI
from datetime import date
from pydantic import BaseModel


class ustats(BaseModel):
    user_id : int 
    game_id : int  
    finished : date = None
    guesses : int
    won : int
    

class username(BaseModel):
      username : str
app = FastAPI()


@app.post("/newgame")
def newgame(un : username):
	u=dict(un)
	usrname = u["username"]
	conn = sqlite3.connect("var/shard4.db")
	ret = conn.execute('''SELECT user_id from users
		                    WHERE username = ?''', (usrname,))
	uid = ret.fetchall()[0][0]
	conn.close()
	userid = {}
	userid['userid']=uid
	return userid
		
@app.get("/Getuserstats")
def checkstats(userid : int):
    
    conn = sqlite3.connect("var/stats.db")
    ret = conn.execute('''SELECT uuid from users
                            WHERE user_id = ?''', (userid,))
    uuid = ret.fetchall()[0][0]
    conn.close()
    
    shard = (int(uuid, 16) % 3) + 1
    name = 'var/shard' + str(shard) + '.db'
    
    conn = sqlite3.connect(name)
    ret = conn.execute('''SELECT * from games
                            WHERE user_id = ?''', (userid,))
    
    cur = conn.execute("SELECT count(*) FROM games WHERE user_id = ? LIMIT 1", [userid])
    cur1 = conn.execute("SELECT won FROM games WHERE user_id = ? ORDER BY finished" , [userid])
    #cur2 = conn.execute("SELECT streak FROM streaks WHERE user_id = ?" , [userid])  
    cur3 = conn.execute("SELECT Count(won) FROM games WHERE user_id = ? and won=1"  , [userid]) 
    cur4 = conn.execute("SELECT ROUND(AVG(guesses),2) FROM games WHERE user_id = ?"  , [userid]) 
    cur5 = conn.execute("select '1' , count(game_id) from games where won=1 and guesses=1 and user_id=? union select '2' , count(game_id) from games where won=1 and guesses=2 and user_id = ? union select '3' , count(game_id) from games where won=1 and guesses=3 and user_id=? union select '4' , count(game_id) from games where won=1 and guesses=4 and user_id=? union select '5' , count(game_id) from games where won=1 and guesses=5 and user_id=? union select '6' , count(game_id) from games where won=1 and guesses=6 and user_id=? union select 'fail' , count(*) from games where won=0 and  user_id=?" 
                        , (userid,userid,userid,userid,userid,userid,userid))
    out = cur.fetchall()
    out1= cur1.fetchall()
    #out2= cur2.fetchall()
    out3= cur3.fetchall()
    out4= cur4.fetchall()
    out5= cur5.fetchall()
    
 
    won=[out1[i][0] for i in range(len(out1))]
    #print(won)
    won.reverse()
    zeroFirstInd = won.index(0) if 0 in won else len(won)
    currentstreak = functools.reduce(lambda a,b: a+b, won[:zeroFirstInd])
    #print('##############')
    #print(won)
    def maxstreak():
        
        sum1=0
        maxsum=0

        for i in won:
            #print(i, sum1, maxsum)
   
            if i==1:
                sum1=sum1+i
        
            elif i==0:
                if maxsum<=sum1:
                    maxsum=sum1
                sum1=0
        if maxsum<=sum1:
            maxsum=sum1
        return (maxsum)  
    

    maxs=maxstreak()
    guesses=dict(out5)
    games_played=out[0][0]
    games_won = out3[0][0]
    avgguesses = out4[0][0]
    winpercentage = round((games_won/games_played)*100,2)

    userstats = {}
    userstats["currentStreak"]=currentstreak
    userstats["maxs"]=maxs
    userstats["guesses"]=guesses
    userstats["winpercentage"]=winpercentage
    userstats["games_played"]=games_played
    userstats["games_won"]=games_won
    userstats["avgguesses"]=avgguesses
    
    conn.close()
    
    return userstats
    


@app.get("/gettopusers")
def gettopusers():
    conn1 = sqlite3.connect("var/shard1.db")
    cur = conn1.execute("""select uuid, count(WON) AS WINS 
                          from games 
                          where won=1 
                          group by uuid 
                          ORDER BY WINS 
                          DESC LIMIT 10""")
    out1 = cur.fetchall()
    conn1.close()
    
    conn2 = sqlite3.connect("var/shard2.db")
    cur = conn2.execute("""select uuid, count(WON) AS WINS 
                          from games 
                          where won=1 
                          group by uuid 
                          ORDER BY WINS 
                          DESC LIMIT 10""")
    out2 = cur.fetchall()
    conn2.close()
    
    conn3 = sqlite3.connect("var/shard3.db")
    cur = conn3.execute("""select uuid, count(WON) AS WINS 
                          from games 
                          where won=1 
                          group by uuid 
                          ORDER BY WINS 
                          DESC LIMIT 10""")
    out3 = cur.fetchall()
    conn3.close()
    
    top30 = list(out1)
    top30.extend(out2)
    top30.extend(out3)
    top30.sort(key = lambda x: x[-1], reverse = True)
    top10 = top30[:10]
    top10_withnm = {}
    conn = sqlite3.connect("var/stats.db")
    
    for uid,val in top10:
        ret = conn.execute('''SELECT username from users
                            WHERE uuid = ?''', (uid,))
        name = ret.fetchall()[0][0]
        top10_withnm[name] = val
        
    conn.close()
    return top10_withnm
    
    
@app.get("/getlongeststreak")
def getlongeststreak():
    
    conn1 = sqlite3.connect("var/shard1.db")
    cur = conn1.execute("""WITH ranks AS (
            SELECT DISTINCT
                uuid,
                finished,
                RANK() OVER(PARTITION BY user_id ORDER BY finished) AS rank
            FROM
                games
            WHERE
                won = TRUE
            ORDER BY
                uuid,
                finished
        ),
        groups AS (
            SELECT
                uuid,
                finished,
                rank,
                DATE(finished, '-' || rank || ' DAYS') AS base_date
            FROM
                ranks
        )
        SELECT
            uuid,
            COUNT(*) AS streak,
            MIN(finished) AS beginning,
            MAX(finished) AS ending
        FROM
            groups
        GROUP BY
            uuid, base_date
        HAVING
            streak > 1
        ORDER BY
            uuid,
            finished;""")
    out1 = cur.fetchall()
    conn1.close()
    
    conn2 = sqlite3.connect("var/shard2.db")
    cur = conn2.execute("""WITH ranks AS (
            SELECT DISTINCT
                uuid,
                finished,
                RANK() OVER(PARTITION BY user_id ORDER BY finished) AS rank
            FROM
                games
            WHERE
                won = TRUE
            ORDER BY
                uuid,
                finished
        ),
        groups AS (
            SELECT
                uuid,
                finished,
                rank,
                DATE(finished, '-' || rank || ' DAYS') AS base_date
            FROM
                ranks
        )
        SELECT
            uuid,
            COUNT(*) AS streak,
            MIN(finished) AS beginning,
            MAX(finished) AS ending
        FROM
            groups
        GROUP BY
            uuid, base_date
        HAVING
            streak > 1
        ORDER BY
            uuid,
            finished;""")
    out2 = cur.fetchall()
    conn2.close()
    
    conn3 = sqlite3.connect("var/shard3.db")
    cur = conn3.execute("""WITH ranks AS (
            SELECT DISTINCT
                uuid,
                finished,
                RANK() OVER(PARTITION BY user_id ORDER BY finished) AS rank
            FROM
                games
            WHERE
                won = TRUE
            ORDER BY
                uuid,
                finished
        ),
        groups AS (
            SELECT
                uuid,
                finished,
                rank,
                DATE(finished, '-' || rank || ' DAYS') AS base_date
            FROM
                ranks
        )
        SELECT
            uuid,
            COUNT(*) AS streak,
            MIN(finished) AS beginning,
            MAX(finished) AS ending
        FROM
            groups
        GROUP BY
            uuid, base_date
        HAVING
            streak > 1
        ORDER BY
            uuid,
            finished;""")
    out3 = cur.fetchall()
    conn3.close()
    
    streakall = list(out1)
    streakall.extend(out2)
    streakall.extend(out3)
    
    streak_df = pd.DataFrame(streakall, columns = ['UUID', 'STREAK', \
                                                   'BEGINNING', 'ENDING'])
    
    
    top10_df = pd.DataFrame(streak_df.groupby(['UUID'])['STREAK'].max().reset_index(),\
                            columns = ['UUID', 'STREAK'])

    top10_df.sort_values(by = 'STREAK', ascending = False, inplace = True, ignore_index = True)
    top10_df = top10_df.loc[0:9]
    top10_uuid = top10_df['UUID'].to_list()
    
    conn = sqlite3.connect("var/stats.db")
    names = []
    for uid in top10_uuid:
        cur = conn.execute('''SELECT username from users
                            WHERE uuid = ?''', (uid,))
        out=cur.fetchall()
        names.append(out[0][0])
    conn.close()
    
    top10_df['USER NAME'] = names
    top10_df.drop(columns = ['UUID'], axis = 1, inplace = True)
    
    top10Dict = {}
    
    for i in top10_df.index.values.tolist():
        top10Dict[top10_df.loc[i, 'USER NAME']] = int(top10_df.loc[i, 'STREAK'])

    return top10Dict
    
@app.post("/winloss")
def winloss(ustat : ustats):
        
    s = dict(ustat)
    
    
    uid = s["user_id"]
    conn = sqlite3.connect("var/shard4.db")
    cur = conn.cursor()
    cur.execute(
            '''SELECT uuid from users
                                    WHERE user_id = ?''', (uid,))
    out=cur.fetchall()
    uuid=out[0][0]
    
    shard = (int(uuid, 16) % 3) + 1
    
    name = 'var/shard' + str(shard) + '.db'
    
    s['uuid'] = uuid
    
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    conn.execute("""INSERT INTO games(user_id, game_id, finished, guesses, won, uuid)
            VALUES(:user_id, :game_id, :finished, :guesses , :won, :uuid)
            """, s)
    
    conn.commit()
    conn.close()
    return s
             


