from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class CreateRGB(Action):
    guildID = -1
    group = "Values"
    templID = 7
    inputs = [
        ValueInput("Red", ValueType.Number),
        ValueInput("Blue", ValueType.Number),
        ValueInput("Green", ValueType.Number)
    ]
    outputs = [
        ValueOutput("RBG", ValueType.Structure)
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
        super().setValue({'r': values[0], 'g': values[1], 'b': values[2]}, 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)