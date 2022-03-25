from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class Print(Action):
    guildID = -1
    group = "Debug"
    templID = 4
    inputs = [
        ValueInput("value", ValueType.Any),
    ]
    outputs = []
    outEvents = [
        EventOutput("completed")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)
        import json
        if isinstance(values[0]['value'], dict):
            try:
                print(json.dumps(values[0]['value'], indent=4))
            except TypeError:
                print(values[0]['value'])
        else:
            print(values[0]['value'])
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

