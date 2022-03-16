import os

from fsmLogic import actionParser
import json
from manager import Board

Board.updateGEvents()

boards = []

paths = os.listdir("json/front/ActionBoards")
for fl in paths:
    with open("json/front/ActionBoards/" + fl, "r") as board:
        boards.append(json.load(board))

for board in boards:
    actionParser.prepareData(board)

for board in boards:
    actionParser.processConnections(board)

for board in boards:
    actionParser.genCodeAction(board)

    with open("json/back/" + board['name'] + ".json", "w") as file:
        json.dump(board, file, indent=4)

with open("json/front/Main.json", "r") as board:
    main = json.load(board)

actionParser.prepareData(main)
actionParser.processConnections(main)
actionParser.genCodeMain(main)

with open("json/back/Main.json", "w") as file:
    json.dump(main, file, indent=4)