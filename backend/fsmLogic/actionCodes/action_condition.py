from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from Bot.bot import client
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class Condition(Action):
    guildID = -1
    templID = 0
    inputs = [
        ValueInput(0, "First value", ValueType.Number, None),
        ValueInput(0, "Second value", ValueType.Number, None)
    ]
    outputs = []
    outEvents = [
        EventOutput(0, "larger"),
        EventOutput(0, "equal"),
        EventOutput(0, "smaller")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client):
        values = super().getValues()
        if values[0] > values[1]:
            return super().sendEvent(0)
        if values[0] == values[1]:
            return super().sendEvent(1)
        else:
            return super().sendEvent(2)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

