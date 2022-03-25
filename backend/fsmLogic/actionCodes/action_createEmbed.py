from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class CreateEmbed(Action):
    guildID = -1
    group = "Embed"
    templID = 11
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
        if values[2]['value'] != "":
            if isinstance(values[2]['value'], dict):
                if ["r", "g", "b"] != list(values[2]['value'].keys()):
                    return super().sendEvent(1)
                color = disnake.Color.from_rgb(values[2]['value']["r"], values[2]['value']["g"], values[2]['value']["b"])
            elif isinstance(values[2]['value'], str):
                try:
                    color = eval("disnake.Color." + values[2]['value'] + "()")
                except AttributeError:
                    return super().sendEvent(1)
            else:
                return super().sendEvent(1)
        else:
            color = ""
        embed = {
            "title": values[0]['value'],
            "description":  values[1]['value'],
            "url": values[3]['value'],
            "color": color,
            "fields": []
        }
        super().setValue(embed, 0)
        super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)