from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class ToNumber(Action):
    guildID = -1
    group = "Values"
    templID = 6
    inputs = [
        ValueInput("value", ValueType.Text),
    ]
    outputs = [
        ValueOutput("result", ValueType.Number)
    ]
    outEvents = [
        EventOutput("completed"),
        EventOutput("parse error")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)
        try:
            super().setValue(int(values[0]['value']), 0)
        except ValueError:
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

