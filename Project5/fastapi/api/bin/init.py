# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 12:06:25 2022

@author: shind
"""

import json
import nltk
import sqlite3
import datetime
from nltk.corpus import words

nltk.download('words')


def createsubset():
    word_lst = json.load(open('./share/answers.json'))
    conn = sqlite3.connect("wordlelist.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE words(id int PRIMARY KEY, dtWord date, word text)''')
    dtInit = datetime.date(2022, 4, 5)
    for i,item in enumerate(word_lst):
        #dtStr = datetime.datetime.strftime(dtInit, '%Y/%m/%d')
        cur.execute('INSERT INTO words VALUES (?,?,?)', (i,dtInit,item))
        dtInit = dtInit + datetime.timedelta(days = 1)
    conn.commit()
    conn.close()



def createwords():
    all5 = [word for word in words.words() if len(word) == 5]
    conn = sqlite3.connect("wordsall.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE words(id int PRIMARY KEY, word text)''')
    for i,item in enumerate(all5):
        cur.execute('INSERT INTO words VALUES (?,?)', (i,item))
    conn.commit()
    conn.close()

def check(name):
    conn = sqlite3.connect(name)
    cur = conn.cursor()
    for row in cur.execute('SELECT * FROM words'):
        print(row)
    

createsubset()
createwords()

