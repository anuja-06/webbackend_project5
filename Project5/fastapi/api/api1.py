# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 12:17:29 2022

@author: shind
"""

import sqlite3
import datetime
import enchant
from profanity_check import predict, predict_prob
import warnings
warnings.filterwarnings("ignore")
from fastapi import FastAPI


app = FastAPI()

@app.post("/checkvalidword")
def checkvalidword(word : str):
   # word.lower()
    d = enchant.Dict("en_US")
    checkvalid = d.check(word)
    if not checkvalid:
        return {'status' : 'Not a valid word'}
    
    elif checkvalid:         
        conn = sqlite3.connect("./var/wordsall.db")
        cur = conn.execute("SELECT word FROM words WHERE word = ? LIMIT 1", [word])
        out = cur.fetchall()
        if len(out) == 0:
                checkoffensive = predict([word])
                if checkoffensive == 0:   
                    maxid = conn.execute("SELECT max(id) FROM words")
                    maxid = maxid.fetchall()[0][0] + 1
                    cur = conn.cursor()
                    cur.execute('INSERT INTO words VALUES (?,?)', (maxid,word))
                    conn.commit()
                    conn.close()
                    return {'status' : 'Inserted into the database successfully'}
                else:
                	#print("the word is offensive")
                	return {'status' : 'Offensive word'}
        else:
            checkoffensive = predict([out][0][0])
            if checkoffensive == 1:  
                cur = conn.cursor()
                cur.execute('DELETE FROM words WHERE word=?', [word])
                conn.commit()
                conn.close()
                print("Word removed")
                return {'status' : 'Removed sucessfully from Database'}
            else:
                return {'status' : 'Word already present in the database'}

