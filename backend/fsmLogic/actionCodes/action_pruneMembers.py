import disnake

from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class PruneMembers(Action):
    guildID = -1
    group = "Interaction"
    templID = 64
    inputs = [
        ValueInput("days", ValueType.Number),
        ValueInput("role", ValueType.Number)
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
        role = guild.get_role(values[1])
        if not role:
            role = None
        try:
            await guild.prune_members(days=max(0, values[0]), roles=[role] if role else [], compute_prune_count=False)
        except HTTPException:
            client.errMsg[guild.id] = "[KickUser - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Discord could not kick this user"
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
