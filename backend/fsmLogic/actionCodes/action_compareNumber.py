from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class CompareNumber(Action):
    guildID = -1
    group = "Math"
    templID = 2
    inputs = [
        ValueInput("First value", ValueType.Number),
        ValueInput("Second value", ValueType.Number)
    ]
    outputs = []
    outEvents = [
        EventOutput("larger"),
        EventOutput("equal"),
        EventOutput("smaller")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)
        if values[0] > values[1]:
            return super().sendEvent(0)
        if values[0] == values[1]:
            return super().sendEvent(1)
        else:
            return super().sendEvent(2)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

