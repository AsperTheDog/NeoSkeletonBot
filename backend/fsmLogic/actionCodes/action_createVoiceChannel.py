from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class CreateVoiceChannel(Action):
    guildID = -1
    group = "Interaction"
    templID = 54
    inputs = [
        ValueInput("name", ValueType.Text),
        ValueInput("user limit", ValueType.Number),
        ValueInput("categoryID", ValueType.Number),
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
        import disnake
        from http.client import HTTPException
        cat = guild.get_channel(values[2])
        if not cat:
            client.errMsg[guild.id] = "[CreateTextChannel - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Category not found"
            return super().sendEvent(1)
        try:
            await guild.create_voice_channel(values[0], user_limit=max(0, values[1]), category=cat)
        except (HTTPException | disnake.InvalidArgument):
            client.errMsg[guild.id] = "[CreateTextChannel - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Discord could not create the channel"
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

