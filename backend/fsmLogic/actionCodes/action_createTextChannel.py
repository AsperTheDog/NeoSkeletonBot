from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class CreateTextChannel(Action):
    guildID = -1
    group = "Interaction"
    templID = 53
    inputs = [
        ValueInput("name", ValueType.Text),
        ValueInput("topic", ValueType.Text),
        ValueInput("categoryID", ValueType.Number),
        ValueInput("nsfw", ValueType.Boolean),
        ValueInput("slowmode seconds", ValueType.Number)
    ]
    outputs = [
        ValueOutput("channelID", ValueType.Number)
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
        from http.client import HTTPException
        cat = guild.get_channel(values[2])
        if not cat:
            client.errMsg[guild.id] = "[CreateTextChannel - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Category not found"
            return super().sendEvent(1)
        try:
            ch = await guild.create_text_channel(values[0], topic=values[1], category=cat, nsfw=values[3], slowmode_delay=max(0, min(21600, values[4])))
        except (HTTPException | disnake.InvalidArgument):
            client.errMsg[guild.id] = "[CreateTextChannel - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Discord could not create the channel"
            return super().sendEvent(1)
        super().setValue(ch.id, 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

