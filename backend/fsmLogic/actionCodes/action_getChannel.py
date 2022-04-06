from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class GetChannel(Action):
    guildID = -1
    group = "Values"
    templID = 57
    inputs = [
        ValueInput("channel ID", ValueType.Number)
    ]
    outputs = [
        ValueOutput("channel", ValueType.Structure, "'id' (Number), 'created at' (Datetime), 'name' (Text), 'mention' (Text), 'category ID' (Number)")
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
        from Bot.utils import formatChannel
        import datetime
        ch = guild.get_channel(values[0])
        if not ch:
            client.errMsg[guild.id] = "[GetChannel - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Could not find channel"
            return super().sendEvent(1)
        super().setValue(formatChannel(ch), 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
