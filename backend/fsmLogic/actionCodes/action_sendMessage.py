from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class SendMessage(Action):
    guildID = -1
    templID = 5
    inputs = [
        ValueInput(0, "Text", ValueType.Any, None),
        ValueInput(0, "Channel", ValueType.Number, None)
    ]
    outputs = []
    outEvents = [
        EventOutput(0, "completed")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client):
        values = super().getValues()
        await client.get_channel(values[1]).send(str(values[0]))
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

