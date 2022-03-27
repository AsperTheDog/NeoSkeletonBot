from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class SendMessage(Action):
    guildID = -1
    group = "Interaction"
    templID = 5
    inputs = [
        ValueInput("Content", ValueType.Any),
        ValueInput("Channel", ValueType.Number)
    ]
    outputs = [
        ValueOutput("Message", ValueType.Number)
    ]
    outEvents = [
        EventOutput("completed"),
        EventOutput("error")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)
        import datetime
        ch = client.get_channel(values[1])
        if not ch:
            client.errMsg[guild] = "[SendMessage - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Could not find channel"
            return super().sendEvent(1)
        msg = await ch.send(str(values[0]))
        super().setValue(msg.id, 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

