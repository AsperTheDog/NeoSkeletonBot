from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class CompareTexts(Action):
    guildID = -1
    group = "Text"
    templID = 8
    inputs = [
        ValueInput("text 1", ValueType.Text),
        ValueInput("text 2", ValueType.Text)
    ]
    outputs = []
    outEvents = [
        EventOutput("equal"),
        EventOutput("not equal")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)
        if values[0]['value'] == values[1]['value']:
            return super().sendEvent(0)
        return super().sendEvent(1)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)