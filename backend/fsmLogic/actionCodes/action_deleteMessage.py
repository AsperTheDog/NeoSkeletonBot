from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class DeleteMessage(Action):
    guildID = -1
    group = "Interaction"
    templID = 68
    inputs = [
        ValueInput("message ID", ValueType.Number)
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
        import disnake
        msg = client.get_message(values[0])
        if not msg:
            client.errMsg[guild.id] = "[DeleteMessage - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Could not find message"
            return super().sendEvent(1)
        try:
            await msg.delete()
        except (HTTPException | disnake.NotFound):
            client.errMsg[guild.id] = "[DeleteMessage - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Discord could not delete the message"
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

