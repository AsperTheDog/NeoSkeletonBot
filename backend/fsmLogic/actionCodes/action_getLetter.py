from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class GetLetter(Action):
    guildID = -1
    templID = 2
    inputs = [
        ValueInput(0, "text", ValueType.Text, None),
        ValueInput(0, "index", ValueType.Number, None),
    ]
    outputs = [
        ValueOutput(0, "letter", ValueType.Text, None)
    ]
    outEvents = [
        EventOutput(0, "completed")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self):
        values = super().getValues()
        super().setValue(values[0][values[1]], 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)