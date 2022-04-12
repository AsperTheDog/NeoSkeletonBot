from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class DeleteMessages(Action):
    guildID = -1
    group = "Interaction"
    templID = 69
    inputs = [
        ValueInput("channel ID", ValueType.Number),
        ValueInput("maximum seconds old", ValueType.Number),
        ValueInput("limit", ValueType.Number),
        ValueInput("author ID", ValueType.Number)
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

        def check(msg):
            return values[3] == 0 or msg.author.id == values[3]

        ch = guild.get_channel(values[0])
        if not ch:
            client.errMsg[guild.id] = "[DeleteMessages - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Could not find channel"
            return super().sendEvent(1)
        dt = datetime.datetime.now() - datetime.timedelta(seconds=values[1])
        try:
            await ch.purge(limit=values[2], oldest_first=True, after=dt, check=check)
        except HTTPException:
            client.errMsg[guild.id] = "[DeleteMessages - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Discord servers returned an error"
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

