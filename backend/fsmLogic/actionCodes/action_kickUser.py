import disnake

from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class KickUser(Action):
    guildID = -1
    group = "Interaction"
    templID = 63
    inputs = [
        ValueInput("user ID", ValueType.Number),
        ValueInput("reason", ValueType.Text)
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
        from http.client import HTTPException
        import datetime
        reason = values[1] if values[1] != "" else None
        try:
            await guild.kick(values[0], reason=reason)
        except HTTPException:
            client.errMsg[guild.id] = "[KickUser - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Discord could not kick this user"
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
