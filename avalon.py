from db import DB
class Avalon:
    def __init__(self):
        self.player_number = {
            "5":{"good":3,"evil":2},
            "6":{"good":4,"evil":2},
            "7":{"good":4,"evil":3},
            "8":{"good":5,"evil":3},
            "9":{"good":6,"evil":3},
            "10":{"good":6,"evil":4},
        }
        self.characters = {
            "merlin":{"name":"merlin","alignment":"good","knownby":"percival"},
            "mordred":{"name":"mordred","alignment":"evil","knownby":"none"},
            "percival":{"name":"percival","alignment":"good","knownby":"none"},
            "oberon":{"name":"oberon","alignment":"evil","knownby":"mordred"},
            "morgana":{"name":"morgana","alignment":"evil","knownby":"percival"},
            "minion":{"name":"minion","alignment":"evil","knownby":"wizards"},
            "knight":{"name":"knight","alignment":"good","knownby":"none"}
        }
    # def addPlayer2Game(self, game_id, player_name):
    #     p = {
    #         "game_id": game_id,
    #         "game_title": "Avalon",
    #         "character_title": "", 
    #         "character_data":"",
    #         "player_number":0,
    #         "player_name" : player_name,
    #         "is_active" : 1
    #     }
    #     db.create(p)
    def getCharacters(self, num):
        character_list = [];
        if num == 5:
            character_list = ["merlin","knight","knight","mordred","minion"];
        if num == 6:
            character_list = ["merlin","knight","knight","knight","mordred","minion"];
        if num == 7:
            character_list = ["merlin","knight","knight","knight","mordred","minion","minion"];
        if num == 8:
            character_list = ["merlin","percival","knight","knight","knight","mordred","minion","minion"];
        if num == 9:
            character_list = ["merlin","percival","knight","knight","knight","knight","mordred","morgana","minion"];
        if num == 10:
            character_list = ["merlin","percival","knight","knight","knight","knight","mordred","morgana","minion","minion"];
        return character_list