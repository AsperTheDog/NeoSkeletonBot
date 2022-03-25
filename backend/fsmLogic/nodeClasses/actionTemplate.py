from copy import deepcopy

from fsmLogic.boardManager import BoardManager
from fsmLogic.nodeClasses.inputs import EventInput, ValueInput, ValueOutput, EventOutput
from fsmLogic.nodeClasses.variable import Variable


class Action:
    guildID = -1
    group = "Values"
    templID = 6

    def __init__(self):
        self.inputs = []
        self.outputs = []
        self.outEvents = []

    def execute(self, client, guild):
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
        return {
            "type": obj.__name__,
            "id": obj.templID,
            "group": obj.group,
            "position": {
                "x": 0,
                "y": 0
            },
            "cdkPos": {
                "x": 0,
                "y": 0
            },
            "inputs": [ValueInput.getTemplate(iv.name, iv.valType, iv.combo) for iv in obj.inputs],
            "outputs": [ValueOutput.getTemplate(ov.name, ov.valType) for ov in obj.outputs],
            "events": [EventOutput.getTemplate(oe.name) for oe in obj.outEvents],
            "inputEvent": EventInput.getTemplate()
        }

    def sendEvent(self, event):
        pass
