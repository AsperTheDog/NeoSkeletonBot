from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class ToText(Action):
    guildID = -1
    group = "Values"
    templID = 22
    inputs = [
        ValueInput("value", ValueType.Any),
    ]
    outputs = [
        ValueOutput("result", ValueType.Text)
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
        import json
        if isinstance(values[0], dict):
            try:
                super().setValue(json.dumps(values[0], indent=4), 0)
            except TypeError:
                super().setValue(values[0], 0)
        else:
            super().setValue(str(values[0]), 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

