from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class WaitUntil(Action):
    guildID = -1
    group = "Time"
    templID = 25
    inputs = [
        ValueInput("datetime", ValueType.Datetime),
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
        from datetime import datetime
        td = values[0] - datetime.now()
        if td.total_seconds() < 0:
            guild.errMsg[guild.id] = "[WaitUntil - " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Received date in the past"
            return super().sendEvent(1)
        await asyncio.sleep(td.total_seconds())
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
