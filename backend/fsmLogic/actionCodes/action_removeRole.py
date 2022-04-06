import disnake

from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class RemoveRole(Action):
    guildID = -1
    group = "Interaction"
    templID = 67
    inputs = [
        ValueInput("user ID", ValueType.Number),
        ValueInput("role ID", ValueType.Number)
    ]
    outputs = []
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
        from http.client import HTTPException
        usr = await guild.getch_member(values[0])
        if not usr:
            client.errMsg[guild.id] = "[RemoveRole - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Could not find user"
            return super().sendEvent(1)
        rl = guild.get_role(values[1])
        if not rl:
            client.errMsg[guild.id] = "[RemoveRole - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Could not find role"
            return super().sendEvent(1)
        try:
            await usr.remove_roles(rl)
        except HTTPException:
            client.errMsg[guild.id] = "[RemoveRole - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Discord could not add the role"
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
