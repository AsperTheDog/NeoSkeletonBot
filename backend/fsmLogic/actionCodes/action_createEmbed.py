from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class CreateEmbed(Action):
    guildID = -1
    group = "Embed"
    templID = 6
    inputs = [
        ValueInput("title", ValueType.Text),
        ValueInput("description", ValueType.Text),
        ValueInput("color", ValueType.Any),
        ValueInput("url", ValueType.Text)
    ]
    outputs = [
        ValueOutput("embed", ValueType.Structure)
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
        import disnake
        import datetime
        if values[2] is not None:
            if isinstance(values[2], dict):
                if ["r", "g", "b"] != list(values[2].keys()):
                    return super().sendEvent(1)
                color = disnake.Color.from_rgb(values[2]["r"], values[2]["g"], values[2]["b"])
            elif isinstance(values[2], str):
                try:
                    color = eval("disnake.Color." + values[2] + "()")
                except AttributeError:
                    client.errMsg[guild.id] = "[CreateEmbed - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Invalid color"
                    return super().sendEvent(1)
            else:
                client.errMsg[guild.id] = "[CreateEmbed - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Invalid color type"
                return super().sendEvent(1)
        else:
            color = ""
        embed = {
            "title": values[0],
            "description":  values[1],
            "url": values[3],
            "color": color,
            "fields": []
        }
        super().setValue(embed, 0)
        super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)