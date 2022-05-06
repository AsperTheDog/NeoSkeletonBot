from copy import deepcopy
from disnake.ext.commands import Bot
from disnake import Guild

from fsmLogic.nodeClasses.inputs import EventInput


class Action:
    guildID = -1
    group = "Values"
    templID = 6

    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.outEvents = []

    def execute(self, client: Bot, guild: Guild):
        raise NotImplementedError("Please override function execute() in your action")

    def getValues(self):
        pass

    def setValue(self, value, out):
        pass

    def checkValues(self, vrs):
        pass

    def addConnections(self, inputs, outputs, outEvents):
        self.inputs = deepcopy(inputs)
        self.outputs = deepcopy(outputs)
        self.outEvents = deepcopy(outEvents)

    @staticmethod
    def getTemplate(obj):
        try:
            with open("fsmLogic/actionCodes/descriptions/" + obj.__name__ + ".html", "r") as file:
                descr = file.read()
        except FileNotFoundError:
            descr = "<h2>" + obj.__name__ + "</h2><br>This action is either custom or is missing a description"
        return {
            "type": obj.__name__,
            "id": obj.templID,
            "description": descr,
            "group": obj.group,
            "position": {
                "x": 0,
                "y": 0
            },
            "cdkPos": {
                "x": 0,
                "y": 0
            },
            "inputs": [iv.getTemplate() for iv in obj.inputs],
            "outputs": [ov.getTemplate() for ov in obj.outputs],
            "events": [oe.getTemplate() for oe in obj.outEvents],
            "inputEvent": EventInput.getTemplate()
        }

    def sendEvent(self, event):
        pass
