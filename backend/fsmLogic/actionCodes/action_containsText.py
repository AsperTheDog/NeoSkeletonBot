import disnake

from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class ContainsText(Action):
    guildID = -1
    group = "Text"
    templID = 4
    inputs = [
        ValueInput("Text", ValueType.Text),
        ValueInput("Subtext", ValueType.Text)
    ]
    outputs = []
    outEvents = [
        EventOutput("Contained"),
        EventOutput("Not contained")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)
        if values[1] in values[0]:
            return super().sendEvent(0)
        return super().sendEvent(1)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
