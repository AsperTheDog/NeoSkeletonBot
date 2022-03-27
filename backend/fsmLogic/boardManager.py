import json


class BoardManager:
    globalEvents = []
    customActionEvents = []
    valueTypes = {}
    _mains = {}

    @staticmethod
    def updateGEvents():
        with open("fsmLogic/dataFiles/tracking/gevents.json", "r") as file:
            gEvents = json.load(file)
        BoardManager.globalEvents = gEvents['events']
        BoardManager.customActionEvents = gEvents['customAction']

    @staticmethod
    def updateValueTypes():
        with open("fsmLogic/dataFiles/tracking/types.json", "r") as file:
            BoardManager.valueTypes = json.load(file)

    @staticmethod
    def mainClass(cls):
        print("Added board", cls.__name__)
        BoardManager._mains[cls.guildID] = cls

    @staticmethod
    def sendGlobalEvent(client, event, value, guild):
        print("broadcasting event", event, "for guild", guild)
        if guild not in BoardManager._mains:
            return
        if guild not in client.errCh:
            client.errCh[guild] = client.get_guild(int(guild)).system_channel
        BoardManager._mains[guild].processEvent(client, event, value, guild)

