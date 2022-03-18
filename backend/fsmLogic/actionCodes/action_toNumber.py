from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from Bot.bot import client
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class ToNumber(Action):
    guildID = -1
    templID = 6
    inputs = [
        ValueInput(0, "value", ValueType.Text, None),
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
        super().setValue(int(values[0]), 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

