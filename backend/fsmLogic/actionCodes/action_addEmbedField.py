from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class AddEmbedField(Action):
    guildID = -1
    group = "Embed"
    templID = 0
    inputs = [
        ValueInput("embed", ValueType.Structure),
        ValueInput("title", ValueType.Text),
        ValueInput("description", ValueType.Text),
        ValueInput("inline", ValueType.Boolean)
    ]
    outputs = [
        ValueOutput("result", ValueType.Structure, "HIDDEN")
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
        embed = values[0]
        if 'fields' not in embed or not isinstance(embed['fields'], list):
            client.errMsg[guild.id] = "[AddEmbedField - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Invalid Embed structure"
            return super().sendEvent(1)
        embed['fields'].append({'name': values[1], 'value': values[2], 'inline': values[3]})
        super().setValue(embed, 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)