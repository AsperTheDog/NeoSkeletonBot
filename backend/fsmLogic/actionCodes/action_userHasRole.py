import disnake

from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class UserHasRole(Action):
    guildID = -1
    group = "Values"
    templID = 65
    inputs = [
        ValueInput("user ID", ValueType.Number),
        ValueInput("role ID", ValueType.Number)
    ]
    outputs = []
    outEvents = [
        EventOutput("yes"),
        EventOutput("no"),
        EventOutput("error")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)
        import datetime
        usr = await guild.getch_member(values[0])
        if not usr:
            client.errMsg[guild.id] = "[UserHasRole - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Could not find user"
            return super().sendEvent(2)
        rl = usr.get_role(values[1])
        if not rl:
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
