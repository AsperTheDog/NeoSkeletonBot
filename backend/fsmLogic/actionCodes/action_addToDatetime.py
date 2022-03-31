from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class AddToDatetime(Action):
    guildID = -1
    group = "Time"
    templID = 27
    inputs = [
        ValueInput("datetime", ValueType.Datetime),
        ValueInput("day", ValueType.Number),
        ValueInput("hour", ValueType.Number),
        ValueInput("minute", ValueType.Number),
        ValueInput("second", ValueType.Number)
    ]
    outputs = [
        ValueOutput("datetime", ValueType.Datetime)
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
        from datetime import timedelta
        td = timedelta(days=values[1], hours=values[2], minutes=values[3], seconds=values[4])
        newTime = values[0] + td
        super().setValue(newTime, 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

