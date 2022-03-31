from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class AddTillWeekday(Action):
    guildID = -1
    group = "Time"
    templID = 26
    inputs = [
        ValueInput("datetime", ValueType.Datetime),
        ValueInput("weekday", ValueType.Combo, [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]),
        ValueInput("beginnig of day", ValueType.Boolean)
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
        from datetime import timedelta, datetime
        weeks = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6
        }
        oldWday = values[2].weekday()
        newTime = values[2] + timedelta(days=(weeks[values[1]] - oldWday + 7) % 7)
        if values[2]:
            newTime = newTime.today()
            newTime = datetime(year=newTime.year, month=newTime.month, day=newTime.day)
        super().setValue(newTime, 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

