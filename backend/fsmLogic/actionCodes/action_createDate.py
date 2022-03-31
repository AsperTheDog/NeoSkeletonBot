from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class CreateDate(Action):
    guildID = -1
    group = "Time"
    templID = 5
    inputs = [
        ValueInput("year", ValueType.Number),
        ValueInput("month", ValueType.Number),
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
        from datetime import datetime
        super().setValue(datetime(year=values[0], month=values[1], day=values[2], hour=values[3], minute=values[4], second=values[5]), 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

