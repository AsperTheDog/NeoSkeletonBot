import os

from actionManager import ActionManager

paths = os.listdir("fsmLogic/actionCodes/custom")
for pth in paths:
    exec("from actionCodes.custom." + pth + " import *")

print(ActionManager._actions)