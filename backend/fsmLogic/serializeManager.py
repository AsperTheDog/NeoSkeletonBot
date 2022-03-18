import os

from fsmLogic import actionParser
import json

from flask import jsonify

from fsmLogic.actionManager import ActionManager


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
            return
        path = "fsmLogic/dataFiles/front/" + guild + "/Main.json"
        if not os.path.isdir("fsmLogic/dataFiles/front/" + guild):
            os.mkdir("fsmLogic/dataFiles/front/" + guild)
    else:
        if not os.path.isdir("fsmLogic/dataFiles/front/" + guild + "/ActionBoards"):
            os.makedirs("fsmLogic/dataFiles/front/" + guild + "/ActionBoards")
        path = "fsmLogic/dataFiles/front/" + guild + "/ActionBoards/" + data['name'] + ".json"
    with open(path, "w") as file:
        json.dump(data, file, indent=4)
    if data['name'] == 'Main':
        actionParser.compileMain(data, guild)
        return
    actionParser.compileAction(data, guild)
    return ActionManager.getAction(data['name'], guild).getTemplate()


def deleteFiles(guild, board):
    os.remove("fsmLogic/dataFiles/front/" + guild + "/ActionBoards/" + board + ".json")
    if len(os.listdir("fsmLogic/dataFiles/front/" + guild + "/ActionBoards")) == 0:
        os.rmdir("fsmLogic/dataFiles/front/" + guild + "/ActionBoards")
        if len(os.listdir("fsmLogic/dataFiles/front/" + guild)) == 0:
            os.rmdir("fsmLogic/dataFiles/front/" + guild)
    os.remove("fsmLogic/actionCodes/custom/" + actionParser.hashGuildID(guild) + "/action_" + board + ".py")
    if len(os.listdir("fsmLogic/actionCodes/custom/" + actionParser.hashGuildID(guild))) == 0:
        os.rmdir("fsmLogic/actionCodes/custom/" + actionParser.hashGuildID(guild))
