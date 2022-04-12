from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class GetDBTable(Action):
    guildID = -1
    group = "Database"
    templID = 73
    inputs = [
        ValueInput("code", ValueType.Number),
        ValueInput("table", ValueType.Text)
    ]
    outputs = [
        ValueOutput("table", ValueType.Structure, "UNKNOWN")
    ]
    outEvents = [
        EventOutput("completed"),
        EventOutput("Error")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)
        import datetime
        try:
            await client.db.accessTable(values[0], values[1])
        except ValueError:
            client.errMsg[guild.id] = "[GetDBTable - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Invalid code"
            return super().sendEvent(1)
        try:
            super().setValue(client.db.getTable(values[0], values[1]), 0)
        except ValueError:
            client.errMsg[guild.id] = "[GetDBTable - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Data requested does not exist"
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

