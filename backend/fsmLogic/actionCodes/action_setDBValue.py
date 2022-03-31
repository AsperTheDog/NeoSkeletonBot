from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class SetDBValue(Action):
    guildID = -1
    group = "Database"
    templID = 32
    inputs = [
        ValueInput("code", ValueType.Number),
        ValueInput("table", ValueType.Text),
        ValueInput("identifier", ValueType.Any),
        ValueInput("element", ValueType.Text),
        ValueInput("value", ValueType.Any)
    ]
    outputs = []
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
            if not client.db.tableIsLoaded(values[0], values[1]):
                await client.db.accessTable(values[0], values[1])
            client.db.setValue(values[0], values[1], values[2], values[3], values[4])
        except ValueError:
            client.errMsg[guild.id] = "[SetDBValue - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Invalid identifier or value element"
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

