from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class Operation(Action):
    guildID = -1
    group = "Math"
    templID = 3
    inputs = [
        ValueInput("First value", ValueType.Number),
        ValueInput("Second value", ValueType.Number),
        ValueInput("Operator", ValueType.Combo, [
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
        if values[2]['value'] == "add":
            super().setValue(values[0]['value'] + values[1]['value'], 0)
        elif values[2]['value'] == "substract":
            super().setValue(values[0]['value'] - values[1]['value'], 0)
        elif values[2]['value'] == "multiply":
            super().setValue(values[0]['value'] * values[1]['value'], 0)
        elif values[2]['value'] == "divide":
            super().setValue(values[0]['value'] / values[1]['value'], 0)
        elif values[2]['value'] == "modulus":
            super().setValue(values[0]['value'] % values[1]['value'], 0)
        elif values[2]['value'] == "power":
            super().setValue(values[0]['value'] ** values[1]['value'], 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

