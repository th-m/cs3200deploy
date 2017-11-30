import os, json, re, random
from db import DB
from avalon import Avalon
from GVM import SessionStore

from urllib.request import urlopen
from http import cookies
from http.server import BaseHTTPRequestHandler, HTTPServer
# from collections import namedtuple
from urllib.parse import parse_qs
from passlib.hash import bcrypt
# list, retrieve | no db change and no state change
# create, update, delete | state change, db change
# TODO create resource for sessions
# TODO install passlib 1.7.1 check website
# TODO install bcrypt check website
# NOTE: bcrypt.hash(password)

SessStore = SessionStore()
class MyHandler(BaseHTTPRequestHandler):
    def send_res(self, status, data):
        jsonEncoded = json.dumps(data);
        self.send_response(status) #1
        # self.send_header("Access-Control-Allow-Origin" ,"*")
        self.send_header("Access-Control-Allow-Origin" , self.headers['Origin'])
        self.send_header("Access-Control-Allow-Credentials" , "true")
        self.send_header('Access-Control-Allow-Headers:', 'Content-Type')
        # self.send_header('Access-Control-Allow-Headers:', "Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        self.send_header("Content-Type","application/json")# 2 send header
        self.send_cookie()
        self.end_headers() # 3
        self.wfile.write(bytes(jsonEncoded, "utf-8")) # 4 send body
    
    def requestPrepHelper(self):
        self.routePath = list(filter(None, self.path.split("/"))) 
        self.load_session()
        # self.load_cookie()
        self.db = DB()
    
    def load_session(self):
        self.load_cookie()
        if "sessionId" in self.cookie:
            sessionId = self.cookie["sessionId"].value
            sessionData = SessStore.getSession(sessionId)
            if sessionData is not None:
                pass
                # load session data
                self.session = sessionData 
            else:
                pass
                #self.cookie['sessionId'] = # SET THIs
                sessionId = SessStore.createSession()
                self.cookie["sessionId"] = sessionId
                # create new session_id
                # assing session_id
                # create empty session data in session store
                self.session = SessStore.getSession(sessionId)
        else:
            pass
            sessionId = SessStore.createSession()
            self.cookie["sessionId"] = sessionId
            # create new session_id
            # assing session_id
            # create empty session data in session store
            self.session = SessStore.getSession(sessionId)
    
    def handleSessionCreate(self):
        # do authentication stuff
        # if successful: 
            # self.session['userid'] = session
        pass
    def load_cookie(self):
        # print(self.headers)
        if "Cookie" in self.headers:
            print("yes cookie is in there")
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            print("no cookie is in there")
            self.cookie= cookies.SimpleCookie()
    
    def send_cookie(self):
        for dataMember in self.cookie.values():
            self.send_header("Set-Cookie", dataMember.OutputString())
            
    def do_OPTIONS(self):
        
        self.send_response(200)
        # self.send_header("Access-Control-Allow-Origin" , "*")
        self.send_header("Access-Control-Allow-Origin" , self.headers['Origin'])
        self.send_header("Access-Control-Allow-Credentials" , "true")
        self.send_header("Content-Type","application/json")# 2 send header
        self.send_header('Access-Control-Allow-Headers:', 'Content-Type')
        # self.send_header('Access-Control-Allow-Headers:', "Access-Control-Allow-Headers", "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With")
        # self.send_header("Content-Type","application/x-www-form-urlencoded")# 2 send header
        self.send_header('Access-Control-Allow-Methods:', 'POST, PATCH, PUT, DELETE, OPTIONS')
        self.end_headers() # 3

    def do_PUT(self):
        
        self.requestPrepHelper()
        
        if not self.routePath:
            self.send_res(400,{"response": "failure", "message": "bad path"})
        elif self.routePath[0] == "games" and self.routePath[2] == "players" and len(self.routePath) == 3:            
            # print(self.routePath)
            ava = Avalon()
            gameCharacters = dict(ava.characters)

            players = db.get(self.routePath[1], True) # get players in game
            count = len(players)
            
            character_list = ava.getCharacters(count)
            random.shuffle(character_list)

            for i in range(count):
                players[i]['character_title'] =  gameCharacters[character_list[i]]['name']
                players[i]['knownby'] =  gameCharacters[character_list[i]]['knownby']
            
            for player in players:
                player['character_data'] = ""
            
            for player in players:
                if player['knownby'] == "wizards":
                    merlin = [element for element in players if element['character_title'] == 'merlin']
                    i = players.index(merlin[0])
                    players[i]['character_data'] += str(player['player_name']) + " is a minion \n"
                    
                    mordred = [element for element in players if element['character_title'] == 'mordred']
                    i = players.index(mordred[0])
                    players[i]['character_data'] += str(player['player_name']) + " is a minion \n"
                
                if player['knownby'] == "percival" and count > 7:
                    p = [element for element in players if element['character_title'] == 'percival']
                    i = players.index(p[0])
                    players[i]['character_data'] += str(player['player_name']) +" is merlin \n" 
                
            for player in players:
                player['is_active'] = 0
                db.update(player)
            
            self.send_res(200,players)
        else:
            self.send_res(404,{"response":"bad path"})
    def do_DELETE(self):
        self.requestPrepHelper()
        if not self.routePath:
            self.send_res(400,{"response": "failure", "message": "bad path"})
        elif self.routePath[0] == "players" and len(self.routePath) == 2:
            if not self.db.get(self.routePath[1]):
                self.send_res(400,{"response": "failure", "message": "bad id"})
            else:
                self.db.delete({"id":self.routePath[1]})
                response = {"response": "success", "message": "player deleted"}
                self.send_res(202,response)
        
        else:
            self.send_res(404,{"response": "failure", "message": "bad path"})
    def do_GET(self): 
        self.requestPrepHelper()
        if not self.routePath:
            self.send_res(400,{"response": "failure", "message": "bad path"})
        elif self.routePath[0] == "players" and len(self.routePath) == 1:            
            self.send_res(200,self.db.get())
        elif self.routePath[0] == "players" and len(self.routePath) == 2:
            playerInfo = self.db.get(self.routePath[1])
            if not playerInfo:
                self.send_res(400,{"response": "failure", "message": "bad id"})
            else:
                self.send_res(200,playerInfo)
        elif self.routePath[0] == "games" and len(self.routePath) == 1:
            sql = "SELECT * FROM sessions where id = '"+str(self.cookie["sessionId"].value)+"';"
            userId = self.db.sqlGetSimple(sql)
            print(userId)
            if len(userId) == 0:
                self.send_res(401,{"failure": "unauthenticated"})
            else:
                self.send_res(200,self.db.getActiveGames())
        elif self.routePath[0] == "games" and self.routePath[2] == "players" and len(self.routePath) == 3:
            inGamePlayers = self.db.get(self.routePath[1], True) # second paramerter means query by game id
            if not inGamePlayers:
                self.send_res(400,{"response": "failure", "message": "bad id"})
            else:
                self.send_res(200,inGamePlayers)
        elif self.routePath[0] == "sessions" and len(self.routePath) == 1:
            # print(self.cookie["sessionId"].value)
            sql = "SELECT * FROM sessions where id = '"+str(self.cookie["sessionId"].value)+"';"
            # print(sql)
            userId = self.db.sqlGetSimple(sql)
            print(userId)
            if len(userId) == 0:
                print("you hit this")
                self.send_res(200,{"success": "no data"})
            else:
                userId = userId[0]['user_id']
                sql = "SELECT * FROM users where id = \'"+str(userId)+"\';"
                userData = self.db.sqlGetSimple(sql)
                print(userData)
                self.send_res(200,{"success": userData[0]})
                # self.send_res(200,userData)
        else:
            self.send_res(404,{"response": "failure", "message": "bad path"})
            self.send_response(404) #1            
    def do_POST(self):
        # self.load_session()
        self.requestPrepHelper()
        length = int(self.headers['content-length']) # we must have length to read post 
        body = self.rfile.read(length).decode("utf-8")
        parsed_body = parse_qs(body)
        if not self.routePath:
            self.send_res(400,{"response": "failure", "message": "bad path"})
        elif self.routePath[0] == "players":  
            # print("players path hit")
            
            player_name = parsed_body['player_name'][0]
            game_id = parsed_body['game_id'][0]
            p = {
                "game_id": game_id,
                "game_title": "Avalon",
                "character_title": "", 
                "character_data":"",
                "player_number":0,
                "player_name" : player_name,
                "is_active" : 1
            }
            playerUID = self.db.create(p)
            
            success = {
                "response": "success",
                "message" : "joined game",
                "player_id": playerUID,
                "game_id": game_id
            }
            self.send_res(201,success)
            
        elif self.routePath[0] == "users":
            # print("create user path hit")
            
            # {'email': ['junk@jnk.com'], 'password': ['password'], 'first_name': ['Thom Thom'], 'last_name': ['Valadez'], 'age': ['13']}
            password = parsed_body['password'][0]
            hash = bcrypt.encrypt(password, salt="S06TOS1bdBdyxFpahzvzha")
            email = parsed_body['email'][0]
            sql = "SELECT * FROM users where email = \'"+str(parsed_body['email'][0])+"\';"
            user = self.db.sqlGetSimple(sql)
            if user:
                self.send_res(422,{"failure": "user with that email exists","message": "user with that email exists"})
            else:
                # CREATE TABLE users (id integer primary key, email varchar(20), encr_pass text, first_name varchar(30), last_name varchar(30),  age integer);
                u = {
                    "email": parsed_body['email'][0],
                    "encr_pass": hash, 
                    "first_name":parsed_body['first_name'][0],
                    "last_name":parsed_body['last_name'][0],
                    "age" : parsed_body['age'][0]
                }
                UID = self.db.createUser(u)
                
                success = {
                    "response": "success",
                    "message" : "created user",
                    "first_name":parsed_body['first_name'][0],
                    "last_name":parsed_body['last_name'][0]
                }
                # r = random.randint(1,10001)
                SID = self.db.createSession(self.cookie["sessionId"].value,UID)
                # self.cookie["sessionId"] = SID
                self.send_res(201,success)
        
        elif self.routePath[0] == "sessions":   
            # {'email': ['junk@jnk.com'], 'password': ['tester']}
            sql = "SELECT * FROM users where email = \'"+str(parsed_body['email'][0])+"\';"
            user = self.db.sqlGetSimple(sql)
            # print(user)
            if not user:
                self.send_res(422,{"failure": "unauthenticated"})
            else:
                hash = user[0]['encr_pass']
                password = parsed_body['password'][0]
                if(bcrypt.verify(password, hash)):
                    success = {
                        "response": "success",
                        "message" : "authenticated",
                        "first_name":user[0]['first_name'],
                        "last_name":user[0]['last_name']
                    }
                    # self.cookie["sessionId"].value
                    SID = self.db.createSession(self.cookie["sessionId"].value,user[0]['id'])
                    # self.cookie["sessionId"] = SID
                    self.send_res(201,success)
                else:
                    self.send_res(401,{"failure": "unauthenticated"})

        elif self.routePath[0] == "games": 
            sql = "SELECT * FROM sessions where id = '"+str(self.cookie["sessionId"].value)+"';"
            userId = self.db.sqlGetSimple(sql)
            print(userId)
            if len(userId) == 0:
                self.send_res(401,{"failure": "unauthenticated"})
            else:  
                player_name = parsed_body['player_name'][0]
                new_id = self.db.getNewGameId()
                p = {
                    "game_id": new_id,
                    "game_title": "Avalon",
                    "character_title": "", 
                    "character_data":"",
                    "player_number":0,
                    "player_name" : player_name,
                    "is_active" : 1
                }
                playerUID = self.db.create(p)
                success = {
                    "response": "success",
                    "message" : "game created",
                    "game_id": new_id,
                    "player_id": playerUID
                }
                
                self.send_res(201,success)
        else:
            self.send_res(404,{"failure": "bad path"})

        
def main():
    listen = ("127.0.0.1", 6060) # ip and port
    server = HTTPServer(listen,MyHandler)
    print("Listening ...")
    server.serve_forever()
    
main()