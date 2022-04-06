from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class GetRole(Action):
    guildID = -1
    group = "Values"
    templID = 59
    inputs = [
        ValueInput("role ID", ValueType.Number)
    ]
    outputs = [
        ValueOutput("role", ValueType.Structure, "'id' (Number), 'created at' (Datetime), 'mention' (Text), 'name' (Text), 'is admin' (Boolean)")
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
        from Bot.utils import formatRole
        import datetime
        rl = guild.get_role(values[0])
        if not rl:
            client.errMsg[guild.id] = "[GetRole - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Could not find role"
            return super().sendEvent(1)
        super().setValue(formatRole(rl), 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
