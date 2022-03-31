from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class WaitFor(Action):
    guildID = -1
    group = "Time"
    templID = 23
    inputs = [
        ValueInput("time", ValueType.Text),
    ]
    outputs = []
    outEvents = [
        EventOutput("completed"),
        EventOutput("error")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)
        import asyncio
        from datetime import timedelta, datetime
        import re
        weeks = re.match(r"([0-9]+)w", values[0])
        days = re.match(r"([0-9]+)d", values[0])
        minutes = re.match(r"([0-9]+)m", values[0])
        seconds = re.match(r"([0-9]+)s", values[0])
        weeks = int(weeks) if weeks else None
        days = int(days) if days else None
        minutes = int(minutes) if minutes else None
        seconds = int(seconds) if seconds else None
        td = timedelta(
            weeks=int(weeks) if weeks else 0,
            days=int(days) if days else 0,
            minutes=int(minutes) if minutes else 0,
            seconds=int(seconds) if seconds else 0
        )
        if td.total_seconds() <= 0:
            client.errMsg[guild.id] = "[WaitFor - " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Invalid time format"
            return super().sendEvent(1)

        await asyncio.sleep(td.total_seconds())
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

