from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class ReplaceMatch(Action):
    guildID = -1
    group = "Text"
    templID = 72
    inputs = [
        ValueInput("text", ValueType.Text),
        ValueInput("original subtext", ValueType.Text),
        ValueInput("new subtext", ValueType.Text)
    ]
    outputs = [
        ValueOutput("text", ValueType.Text)
    ]
    outEvents = [
        EventOutput("completed")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)
        super().setValue(values[0].replace(values[1], values[2]), 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

