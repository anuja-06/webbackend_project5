import httpx
from pydantic import BaseModel
from fastapi import FastAPI
import json

app = FastAPI()



class users(BaseModel):
   username : str
    
   
@app.post('/game/new')
def finduserid(ug: users):
	game={}
	sdata = {}
	u=dict(ug)
	data = json.dumps(u)
	
	#this api call will return the userid.
	ruserid = httpx.post("http://127.0.0.1:5000/newgame", data=data)
	
	#this api call will return the game which has to be played.
	rgameid = httpx.get("http://127.0.0.1:5100/choosegame")
	
	userval=ruserid.json()["userid"]
	usergame=rgameid.json()["gameid"]
	
	sdata["user_id"]=userval
	sdata["game_id"]=usergame
	udata = json.dumps(sdata)
	
	#this api will return the state of the game.
	rstatus = httpx.post("http://127.0.0.1:5200/stateofgame", data=udata)
	
		
	guesslist=[]	
	status=rstatus.json()
	print(status)
		
	
	if status==None:
		game["status"]="new"
		game["user_id"]=userval
		game["game_id"]=usergame
		
		rnewgame = httpx.post("http://127.0.0.1:5200/create", data=udata)
		return game
	else:
		game["status"]="inprogress"
		game["user_id"]=userval
		game["game_id"]=usergame
		
		remaining = rstatus.json()["Remaining"]
		
		game["remaining"]= remaining
		
		for i in range(6-remaining):
		
			guesslist.append(rstatus.json()[str(i+1)])
	
		game["guesses"] = guesslist
		
		
		
		
		
		for i in guesslist:
		
			word={}
			word["word"]=i
			word_dict = json.dumps(word)
			correct=[]
			present=[]
				
			rword=httpx.post("http://127.0.0.1:5100/checkGuessAgainstWord", data=word_dict)
			letters=rword.json()["status"]
				
			for l in letters:
				s=l.split(":")[1].strip()
							
				if s == "IN THE WORD IN CORRECT POSITION":
					correct.append(l.split(":")[0])
				elif s == "IN THE WORD BUT IN INCORRECT POSITION":
					present.append(l.split(":")[0])
		game["letters"]={"correct": correct, "present": present}
				
	
	
	return game
	
