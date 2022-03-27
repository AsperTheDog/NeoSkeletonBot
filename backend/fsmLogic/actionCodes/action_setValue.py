from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class SetValue(Action):
    guildID = -1
    group = "Values"
    templID = 20
    inputs = [
        ValueInput("Value", ValueType.Any)
    ]
    outputs = [
        ValueOutput("Value", ValueType.Any)
    ]
    outEvents = [
        EventOutput("Completed")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)
        super().setValue(values[0], 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)