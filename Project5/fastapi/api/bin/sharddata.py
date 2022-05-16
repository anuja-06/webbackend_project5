import sqlite3
import uuid

def updateUsers():
    conn = sqlite3.connect("./var/stats.db")
    cur = conn.execute("SELECT COUNT(*) FROM users")
    records = cur.fetchall()[0][0]
    cur = conn.execute("ALTER TABLE users ADD uuid VARCHAR(32);")
    
    uuidLst = [uuid.uuid4().hex for i in range(records)]

    for i,val in enumerate(uuidLst):
        cur.execute('''UPDATE users
                 SET uuid = ?
                 WHERE user_id = ?''', (val, i+1))

    conn.commit()
    conn.close()                 


def updateGames():
    conn = sqlite3.connect("./var/stats.db")
    cur = conn.execute("ALTER TABLE games ADD uuid VARCHAR(32);")
    cur = conn.execute("SELECT COUNT(*) FROM users")
    records = cur.fetchall()[0][0]

    for i in range(records):
        uuid_val = conn.execute('''SELECT uuid from users
                                WHERE user_id = ?''', (i+1,))
        uuidV = uuid_val.fetchall()[0][0]
        conn.execute('''UPDATE games
                 SET uuid = ?
                 WHERE user_id = ?''', (uuidV, i+1))

    conn.commit()
    conn.close() 


def sharding():
    
    newShards = ["./var/shard1.db", "./var/shard2.db", "./var/shard3.db"]
    
    conn = sqlite3.connect("./var/stats.db")
    
    cur = conn.execute("SELECT COUNT(*) FROM users")
    records = cur.fetchall()[0][0]
    
    for i in range(records):
        rows = conn.execute('''SELECT * from games
                                WHERE user_id = ?''', (i+1,))
        r = rows.fetchall()
        if  r == []:
            continue
        uuidV = r[0][-1]
        shardnum = int(uuidV, 16) % 3
        
        connT = sqlite3.connect(newShards[shardnum])
        
        isempty = connT.execute('''SELECT * FROM sqlite_master
        WHERE type = 'table' AND name = "games"''')
        isempty = isempty.fetchall()
        if isempty == []:
                   
            connT.execute('''CREATE TABLE games(
                      user_id INTEGER NOT NULL,
                      game_id INTEGER NOT NULL,
                      finished DATE DEFAULT CURRENT_TIMESTAMP,
                      guesses INTEGER,
                      won BOOLEAN,
                      uuid VARCHAR(32),
                      PRIMARY KEY(uuid, game_id),
                      FOREIGN KEY(user_id) REFERENCES users(user_id))''')
        for row in r:
            connT.execute('INSERT INTO games VALUES(?,?,?,?,?,?)', row)
            
            
        connT.commit()
        connT.close()

def sharding4():
    
    conn = sqlite3.connect("./var/stats.db")
    
    cur = conn.execute("SELECT COUNT(*) FROM users")
    records = cur.fetchall()[0][0]
    
    connT = sqlite3.connect("./var/shard4.db")
               
    connT.execute('''CREATE TABLE users(
           user_id INTEGER NOT NULL,
           username VARCHAR(50),
           uuid VARCHAR(32),
           PRIMARY KEY(user_id,uuid))''')
    
    for i in range(records):
        rows = conn.execute('''SELECT * from users
                                WHERE user_id = ?''', (i+1,))
        r = rows.fetchall()
        
        for row in r:
            connT.execute('INSERT INTO  users VALUES(?,?,?)', row)
            
            
    connT.commit()
    connT.close()
    conn.close()

updateUsers()
updateGames()
sharding()
sharding4()
