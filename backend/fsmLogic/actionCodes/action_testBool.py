import disnake

from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class TestBool(Action):
    guildID = -1
    group = "Math"
    templID = 20
    inputs = [
        ValueInput("Bool", ValueType.Boolean)
    ]
    outputs = []
    outEvents = [
        EventOutput("True"),
        EventOutput("False")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)
        if bool(values[0]):
            return super().sendEvent(0)
        return super().sendEvent(1)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
