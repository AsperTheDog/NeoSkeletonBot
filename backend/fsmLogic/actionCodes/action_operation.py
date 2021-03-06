from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class Operation(Action):
    guildID = -1
    group = "Math"
    templID = 12
    inputs = [
        ValueInput("First value", ValueType.Number),
        ValueInput("Second value", ValueType.Number),
        ValueInput("Operator", ValueType.Combo, "add", [
            "add",
            "substract",
            "multiply",
            "divide",
            "modulus",
            "power"
        ])
    ]
    outputs = [
        ValueOutput("result", ValueType.Number)
    ]
    outEvents = [
        EventOutput("completed")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)
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

