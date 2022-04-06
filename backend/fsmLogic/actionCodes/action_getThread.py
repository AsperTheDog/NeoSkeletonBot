from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class GetThread(Action):
    guildID = -1
    group = "Values"
    templID = 62
    inputs = [
        ValueInput("thread ID", ValueType.Number)
    ]
    outputs = [
        ValueOutput("thread", ValueType.Structure, "'id' (Number), 'archived' (Boolean), 'archive duration' (Number), 'created at' (Datetime), 'locked' (Boolean), 'mention' (Text), 'category ID' (Number), 'owner ID' (Number), 'parent ID' (Number)")
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
        from Bot.utils import formatThread
        import datetime
        th = guild.get_thread(values[0])
        if not th:
            client.errMsg[guild.id] = "[GetRole - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Could not find role"
            return super().sendEvent(1)
        super().setValue(formatThread(th), 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
