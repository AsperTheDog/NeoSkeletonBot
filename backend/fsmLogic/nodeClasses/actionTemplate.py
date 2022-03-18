from copy import deepcopy

from fsmLogic.boardManager import BoardManager
from fsmLogic.nodeClasses.inputs import EventInput, ValueInput, ValueOutput, EventOutput


class Action:
    def __init__(self):
        self.id = None
        self.inputs = []
        self.outputs = []
        self.outEvents = []

    def __eq__(self, other):
        return self.id is not None and other.id is not None and self.id == other.id

    def execute(self, client):
        raise NotImplementedError("Please override function execute() in your action")

    def getValues(self):
        vals = []
        for inp in self.inputs:
            vals.append(BoardManager.getVar(inp.connection))

    def setValue(self, value, out):
        BoardManager.setVar(self.outputs[out].connection, value)

    def addConnections(self, inputs, outputs, outEvents):
        self.inputs = deepcopy(inputs)
        self.outputs = deepcopy(outputs)
        self.outEvents = deepcopy(outEvents)

    @staticmethod
    def getTemplate(obj):
        return {
            "type": obj.__name__,
            "id": obj.templID,
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
