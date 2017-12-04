import os
import psycopg2
import psycopg2.extras
import urllib.parse
import base64
import sqlite3
import random
from GVM import SessionStore
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx];
    return d 

class DB:
    
    def __init__(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.cursor = self.connection.cursor()



    def __del__(self):
        self.connection.close()
    # CREATE TABLE session (id text, user_id integer);
    # 
    # CREATE TABLE games (id integer primary key, title varchar(20), is_active integer);
    # 
    # CREATE TABLE users (id integer primary key, email varchar(20), encr_pass text, first_name varchar(30), last_name varchar(30),  age integer);
    # 
    # CREATE TABLE players (id integer primary key, game_id integer, game_title varchar(20), character_title varchar(20), character_data text, player_number integer, player_name varchar(20));

    def createSessionsTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sessions (id TEXT, user_id SERIAL)")
        self.connection.commit()
        
    def createGamesTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS games (id SERIAL PRIMARY KEY, title VARCHAR(255), is_active SERIAL)")
        self.connection.commit()
    
    def createUsersTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, email VARCHAR(255), encr_pass TEXT, first_name VARCHAR(255), last_name VARCHAR(255), age SERIAL)")
        self.connection.commit()
    
    def createPlayersTable(self):
        self.cursor.execute("DROP TABLE players;")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS players (id SERIAL PRIMARY KEY, game_id SERIAL, game_title VARCHAR(255), character_title VARCHAR(255), character_data TEXT, player_number SERIAL, player_name VARCHAR(255), is_active SERIAL)")
        self.connection.commit()
        
    def createUser(self, data):
        # CREATE TABLE users (id integer primary key, email varchar(20), encr_pass text, first_name varchar(30), last_name varchar(30),  age integer);
        sql = '''
                INSERT INTO users
                (email, encr_pass, first_name, last_name ,age)
                values (%s,%s,%s,%s,%s)
              '''
        attributes = (
            data['email'], data['encr_pass'], data['first_name'], 
            data['last_name'], data['age']
        )
        
        self.cursor.execute(sql, attributes)
        self.connection.commit()
        return self.cursor.lastrowid
    
    def create(self, data):
        sql = '''
                INSERT INTO players
                (game_id, game_title, character_title, character_data ,player_number, player_name, is_active)
                values (%s,%s,%s,%s,%s,%s,%s)
              '''
        attributes = (
            data['game_id'], data['game_title'], data['character_title'], 
            data['character_data'], data['player_number'], data['player_name'],
            data['is_active']
        )
        
        self.cursor.execute(sql, attributes)
        self.connection.commit()
        return self.cursor.lastrowid
    
    # def sqlHelper(self,table):
    #     sql = '''
    #             SELECT * FROM %s LIMIT 1;
    #           '''
    #     attributes = (table)
    #     self.cursor.execute(sql, attributes)
    #     rows = self.cursor.fetchall()
    #     return rows[0]
    #     # self.connection.commit()
    # def setHelper(self,data):
    #     sqlString = ""
    #     for k, v in data.items():
    #         sqlString += k + " = %s, "
    #      sqlString = sqlString[:-1] + "WHERE id = %s;"
    
    def createSession(self, id, uid):
        sql = '''
        INSERT INTO sessions
            (id, user_id)
            values (%s,%s)
        '''
        # s = SessionStore()
        # rnum = os.urandom(32)
        # rstr = base64.b64encode(rnum).decode('utf-8')
        # return rstr
        attributes = (
            id ,uid
        )
        
        self.cursor.execute(sql, attributes)
        self.connection.commit()
        return True
    
    def updatePlus(self, data, table):
        sql = " UPDATE  " +table+ " SET" + setHelper(sqlHelper(table));
        for k, v in data.items():
         attributes = (
             data['game_id'], data['game_title'], 
             data['character_title'], data['character_data'],
             data['player_number'], data['player_name'], 
             data['is_active'], data['id']
         )
    def update(self, data):
        sql = '''
                UPDATE players
                SET game_id = %s, game_title = %s, character_title = %s, character_data = %s, player_number = %s, player_name = %s, is_active =%s
                WHERE id = %s;
              '''
        # print(sql)
        attributes = (
            data['game_id'], data['game_title'], 
            data['character_title'], data['character_data'],
            data['player_number'], data['player_name'], 
            data['is_active'], data['id']
        )
        self.cursor.execute(sql, attributes)
        self.connection.commit()
    
    def delete(self, data):
        sql = 'DELETE FROM players WHERE id = '+data['id']+';'
        # attributes = (
        #      data['id']
        # )
        print(sql)
        self.cursor.execute(sql)
        # self.cursor.execute(sql, attributes)
        self.connection.commit()
        
    def getActiveGames(self):
        sql = 'SELECT game_id FROM players WHERE is_active = 1 GROUP BY game_id;'
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    def getNewGameId(self):
        sql = 'SELECT game_id FROM players GROUP BY game_id ORDER BY game_id DESC LIMIT 1;'
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        # print(rows)
        return rows[0].get('game_id') + 1
    
    def sqlGetSimple(self, sql):
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
        
    def get(self, id=0, game = False):
        sql = 'SELECT * FROM players'
        if id and not game:
            sql +=  ' WHERE id = '+str(id)+';'
        elif id and game:   
            sql +=  ' WHERE game_id = '+str(id)+';'
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows