import disnake

from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class CreateRole(Action):
    guildID = -1
    group = "Interaction"
    templID = 48
    inputs = [
        ValueInput("name", ValueType.Text),
        ValueInput("color", ValueType.Structure),
        ValueInput("hoist", ValueType.Boolean),
        ValueInput("mentionable", ValueType.Boolean),
        ValueInput("reason", ValueType.Text)
    ]
    outputs = [
        ValueOutput("roleID", ValueType.Number)
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
        from http.client import HTTPException
        from disnake import InvalidArgument
        if ["r", "g", "b"] != list(values[1].keys()):
            client.errMsg[guild.id] = "[CreateRole - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Invalid color format"
            return super().sendEvent(1)
        color = disnake.Color.from_rgb(values[1]["r"], values[1]["g"], values[1]["b"])
        try:
            rl = await guild.create_role(name=values[0], colour=color, hoist=values[2], mentionable=values[3], reason=values[4] if values[4] != "" else None)
        except (HTTPException, InvalidArgument):
            client.errMsg[guild.id] = "[CreateRole - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Discord could not create the role"
            return super().sendEvent(1)
        super().setValue(rl.id, 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
