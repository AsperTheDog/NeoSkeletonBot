from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from Bot.bot import client
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class Operation(Action):
    guildID = -1
    templID = 3
    inputs = [
        ValueInput(0, "First value", ValueType.Number, None),
        ValueInput(0, "Second value", ValueType.Number, None),
        ValueInput(0, "Operator", ValueType.Combo, None, [
            "add",
            "substract",
            "multiply",
            "divide",
            "modulus",
            "power"
        ])
    ]
    outputs = [
        ValueOutput(0, "result", ValueType.Number, None)
    ]
    outEvents = [
        EventOutput(0, "completed")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client):
        values = super().getValues()
        if values[2] == "add":
            super().setValue(values[0] + values[1], 0)
        elif values[2] == "substract":
            super().setValue(values[0] - values[1], 0)
        elif values[2] == "multiply":
            super().setValue(values[0] * values[1], 0)
        elif values[2] == "divide":
            super().setValue(values[0] / values[1], 0)
        elif values[2] == "modulus":
            super().setValue(values[0] % values[1], 0)
        elif values[2] == "power":
            super().setValue(values[0] ** values[1], 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

