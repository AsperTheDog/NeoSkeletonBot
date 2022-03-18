from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from Bot.bot import client
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class extractValue(Action):
    guildID = -1
    templID = 1
    inputs = [
        ValueInput(0, "Extract tag", ValueType.Text, None),
        ValueInput(0, "Structure", ValueType.Structure, None)
    ]
    outputs = [
        ValueOutput(0, "result", ValueType.Any, None)
    ]
    outEvents = [
        EventOutput(0, "Completed")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client):
        values = super().getValues()
        super().setValue(values[1][values[0]], 0)
        super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

