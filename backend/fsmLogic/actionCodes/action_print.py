from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class Print(Action):
    guildID = -1
    templID = 4
    inputs = [
        ValueInput(0, "value", ValueType.Any, None),
    ]
    outputs = []
    outEvents = [
        EventOutput(0, "completed")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self):
        values = super().getValues()
        print(values[0])
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

