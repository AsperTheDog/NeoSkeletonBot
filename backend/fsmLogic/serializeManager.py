import os
from copy import deepcopy

from fsmLogic import actionParser
import json

from flask import jsonify

from fsmLogic.boardManager import BoardManager


def loadBoards(guild):
    mainTempl = {
        "guild": guild,
        "name": "Main",
        "actions": [],
        "varInstances": [],
        "variables": [],
        "transitions": [],
        "globalEvents": [],
        "pipelines": []
    }
    if not os.path.isdir("fsmLogic/dataFiles/front/" + guild):
        return jsonify([mainTempl])
    paths = os.listdir("fsmLogic/dataFiles/front/" + guild)
    boards = []
    if "Main.json" not in paths:
        boards.append(mainTempl)
    else:
        with open("fsmLogic/dataFiles/front/" + guild + "/Main.json", "r") as board:
            boards.append(json.load(board))

    if "ActionBoards" in paths:
        paths = os.listdir("fsmLogic/dataFiles/front/" + guild + "/ActionBoards")
        for fl in paths:
            with open("fsmLogic/dataFiles/front/" + guild + "/ActionBoards/" + fl, "r") as board:
                boards.append(json.load(board))

    return jsonify(boards)


def removeMain(guild):
    BoardManager.removeMain(int(guild))
    if os.path.isfile("fsmLogic/mains/mainBoard_" + guild + ".py"):
        os.remove("fsmLogic/mains/mainBoard_" + guild + ".py")
    if os.path.isfile("fsmLogic/dataFiles/front/" + guild + "/Main.json"):
        os.remove("fsmLogic/dataFiles/front/" + guild + "/Main.json")
        if len(os.listdir("fsmLogic/dataFiles/front/" + guild)) == 0:
            os.rmdir("fsmLogic/dataFiles/front/" + guild)


def saveBoard(data):
    guild = data['guild']
    if data['name'] == "Main":
        if len(data['actions']) + len(data['varInstances']) + len(data['globalEvents']) == 0:
            removeMain(guild)
            return True
        path = "fsmLogic/dataFiles/front/" + guild + "/Main.json"
        if not os.path.isdir("fsmLogic/dataFiles/front/" + guild):
            os.mkdir("fsmLogic/dataFiles/front/" + guild)
    else:
        if not os.path.isdir("fsmLogic/dataFiles/front/" + guild + "/ActionBoards"):
            os.makedirs("fsmLogic/dataFiles/front/" + guild + "/ActionBoards")
        path = "fsmLogic/dataFiles/front/" + guild + "/ActionBoards/" + data['name'] + ".json"
        if not os.path.isfile(path):
            with open(path, "w") as file:
                json.dump(data, file, indent=4)
    unchanged = deepcopy(data)
    if data['name'] == 'Main':
        ret = actionParser.compileMain(data, guild)
    else:
        ret = actionParser.compileAction(data, guild)
    if ret:
        with open(path, "w") as file:
            json.dump(unchanged, file, indent=4)
    return ret


def deleteFiles(guild, board):
    if os.path.isfile("fsmLogic/dataFiles/front/" + guild + "/ActionBoards/" + board + ".json"):
        os.remove("fsmLogic/dataFiles/front/" + guild + "/ActionBoards/" + board + ".json")
        if len(os.listdir("fsmLogic/dataFiles/front/" + guild + "/ActionBoards")) == 0:
            os.rmdir("fsmLogic/dataFiles/front/" + guild + "/ActionBoards")
            if len(os.listdir("fsmLogic/dataFiles/front/" + guild)) == 0:
                os.rmdir("fsmLogic/dataFiles/front/" + guild)
    if os.path.isfile("fsmLogic/actionCodes/custom/" + actionParser.hashGuildID(guild) + "/action_" + board + ".py"):
        os.remove("fsmLogic/actionCodes/custom/" + actionParser.hashGuildID(guild) + "/action_" + board + ".py")
        if len(os.listdir("fsmLogic/actionCodes/custom/" + actionParser.hashGuildID(guild))) == 1:
            os.remove("fsmLogic/actionCodes/custom/" + actionParser.hashGuildID(guild) + "/__init__.py")
            os.rmdir("fsmLogic/actionCodes/custom/" + actionParser.hashGuildID(guild))


def getBoard(guild, name):
    if not os.path.isdir("fsmLogic/dataFiles/front/" + guild) or \
       not os.path.isdir("fsmLogic/dataFiles/front/" + guild + "/ActionBoards") or \
       not os.path.isfile("fsmLogic/dataFiles/front/" + guild + "/ActionBoards/" + name + ".json"):
        return
    with open("fsmLogic/dataFiles/front/" + guild + "/ActionBoards/" + name + ".json", "r") as board:
        return jsonify(json.load(board))
