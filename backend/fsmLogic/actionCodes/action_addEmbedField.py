from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class AddEmbedField(Action):
    guildID = -1
    group = "Embed"
    templID = 13
    inputs = [
        ValueInput("embed", ValueType.Structure),
        ValueInput("title", ValueType.Text),
        ValueInput("description", ValueType.Text),
        ValueInput("inline", ValueType.Boolean)
    ]
    outputs = [
        ValueOutput("result", ValueType.Structure)
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
        embed = values[0]['value']
        if 'fields' not in embed or not isinstance(embed['fields'], list):
            return super().sendEvent(1)
        embed['fields'].append({'name': values[1]['value'], 'value': values[2]['value'], 'inline': bool(values[3]['value'])})
        super().setValue(embed, 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)