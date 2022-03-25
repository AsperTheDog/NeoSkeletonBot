from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class extractValue(Action):
    guildID = -1
    group = "Structure"
    templID = 1
    inputs = [
        ValueInput("Extract tag", ValueType.Text),
        ValueInput("Structure", ValueType.Structure)
    ]
    outputs = [
        ValueOutput("result", ValueType.Any)
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
        super().setValue(values[1]['value'][values[0]['value']], 0)
        super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

