from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class SendError(Action):
    guildID = -1
    group = "Interaction"
    templID = 17
    inputs = [
        ValueInput("Channel", ValueType.Number)
    ]
    outputs = [
        ValueOutput("Message", ValueType.Number)
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
        import datetime
        import disnake
        if values[0] == 0:
            ch = client.get_channel(guild.system_channel)
        else:
            ch = client.get_channel(values[0])
        if not ch:
            client.errMsg[guild.id] = "[SendError - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Could not find channel"
            return super().sendEvent(1)
        embed = disnake.Embed(title=client.errMsg[guild.id], colour=disnake.Colour.red())
        await ch.send(embed=embed)


    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

