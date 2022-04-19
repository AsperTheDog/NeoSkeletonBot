from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class GetRoleByName(Action):
    guildID = -1
    group = "Values"
    templID = 60
    inputs = [
        ValueInput("role name", ValueType.Text)
    ]
    outputs = [
        ValueOutput("role", ValueType.Structure, "id (Number)\ncreated at (Datetime)\nmention (Text)\nname (Text)\nis admin (Boolean)")
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
        roles = guild.roles
        for role in roles:
            if role.name == values[0]:
                super().setValue(formatRole(role), 0)
                return super().sendEvent(0)
        client.errMsg[guild.id] = "[GetRole - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Could not find role"
        return super().sendEvent(1)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
