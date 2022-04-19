from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class GetEvent(Action):
    guildID = -1
    group = "Values"
    templID = 61
    inputs = [
        ValueInput("event ID", ValueType.Number)
    ]
    outputs = [
        ValueOutput("event", ValueType.Structure, "channel ID (Number)\ncreator ID (Number)\ndescription (Text)\nid (Number)\nname (Text)\nuser count (Number)")
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
        from Bot.utils import formatGuildEvent
        import datetime
        ev = guild.get_scheduled_event(values[0])
        if not ev:
            client.errMsg[guild.id] = "[GetRole - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Could not find role"
            return super().sendEvent(1)
        super().setValue(formatGuildEvent(ev), 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
