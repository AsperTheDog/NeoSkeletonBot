from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class RandomNumber(Action):
    guildID = -1
    group = "Math"
    templID = 14
    inputs = []
    outputs = [
        ValueOutput("random", ValueType.Number)
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
        import random
        super().setValue(random.random(), 0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

