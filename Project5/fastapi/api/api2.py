# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 12:02:41 2022

@author: shind
"""

import sqlite3
import datetime
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class gameword(BaseModel):
   word : str
   
@app.get("/choosegame")
def choosegame():
    game = {}
    conn = sqlite3.connect("./var/wordlelist.db")
    #dtObj = datetime.datetime.strptime('2028/07/30', '%Y/%m/%d')
    #dtF = datetime.date(dtObj.year, dtObj.month, dtObj.day)
    cur = conn.execute("SELECT id,word FROM words WHERE dtWord = ? LIMIT 1", [datetime.date.today()])
    out = cur.fetchall()
    answer = out[0][1]
    gameid = out[0][0]
    
    game["gameid"]=gameid
    game["answer"]=answer
    
    return game
    

@app.post("/checkGuessAgainstWord")
def checkGuessAgainstWord(wrd : gameword):
    w=dict(wrd)
    word=w["word"]
    conn = sqlite3.connect("./var/wordlelist.db")
    #dtObj = datetime.datetime.strptime('2028/07/30', '%Y/%m/%d')
    #dtF = datetime.date(dtObj.year, dtObj.month, dtObj.day)
    cur = conn.execute("SELECT word FROM words WHERE dtWord = ? LIMIT 1", [datetime.date.today()])
    out = cur.fetchall()
    answer = out[0][0]
    conn.close()
    
    #both are same
    if answer == word:
        return {'status' : 'YOU WON!!!','Game_Date' : datetime.date.today()}
        
    
    #common letters
    common = list(set(answer).intersection(set(word)))
    
      #letters not present in the word
    incorrect = list(set(word) - set(answer))
    
    #if nothing is common
    if not len(common):
        retLst = [l + ': NOT IN THE WORD' for l in word]
        
    else:
        retLst = []
        for l in word:
            #first letters not in word of the day
            if l in incorrect:
                retLst.append(l + ': NOT IN THE WORD')
            elif l in common:
                #letters in the word of the day and in correct position
                if answer.index(l) == word.index(l):
                    retLst.append(l + ': IN THE WORD IN CORRECT POSITION')
                #letters in the word of the day but in incorrect position
                else:
                    retLst.append(l + ': IN THE WORD BUT IN INCORRECT POSITION' )
    return {'status' : retLst, 'Game_Date' : datetime.date.today()}

