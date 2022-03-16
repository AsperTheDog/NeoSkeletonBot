import json


class Board:
    globalEvents = {}

    @staticmethod
    def updateGEvents():
        with open("fsmLogic/dataFiles/tracking/gevents.json", "r") as file:
            Board.globalEvents = json.load(file)
