import os

from fsmLogic import actionParser
import json

from quart import jsonify

from fsmLogic.actionManager import ActionManager


def loadBoards(guild):
    if not os.path.isdir("fsmLogic/dataFiles/front/" + guild):
        os.mkdir("fsmLogic/dataFiles/front/" + guild)
    paths = os.listdir("fsmLogic/dataFiles/front/" + guild)
    boards = []
    if "Main.json" not in paths:
        with open("fsmLogic/dataFiles/front/" + guild + "/Main.json", "w") as main:
            json.dump({
                "guild": guild,
                "name": "Main",
                "actions": [],
                "varInstances": [],
                "variables": [],
                "transitions": [],
                "globalEvents": [],
                "pipelines": []
            }, main, indent=4)

    with open("fsmLogic/dataFiles/front/" + guild + "/Main.json", "r") as board:
        boards.append(json.load(board))

    if "ActionBoards" not in paths:
        os.mkdir("fsmLogic/dataFiles/front/" + guild + "/ActionBoards")
    else:
        paths = os.listdir("fsmLogic/dataFiles/front/" + guild + "/ActionBoards")
        for fl in paths:
            with open("fsmLogic/dataFiles/front/" + guild + "/ActionBoards/" + fl, "r") as board:
                boards.append(json.load(board))

    return jsonify(boards)


def saveBoard(data):
    guild = data['guild']
    if data['name'] == "Main":
        path = "fsmLogic/dataFiles/front/" + guild + "/Main.json"
    else:
        path = "fsmLogic/dataFiles/front/" + guild + "/ActionBoards/" + data['name'] + ".json"
    with open(path, "w") as file:
        json.dump(data, file, indent=4)
    if data['name'] == 'Main':
        actionParser.compileMain(data, guild)
        return
    actionParser.compileAction(data, guild)
    return ActionManager.getAction(data['name'], guild).getTemplate()