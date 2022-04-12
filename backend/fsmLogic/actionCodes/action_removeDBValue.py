from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class RemoveDBValue(Action):
    guildID = -1
    group = "Database"
    templID = 34
    inputs = [
        ValueInput("code", ValueType.Number),
        ValueInput("table", ValueType.Text),
        ValueInput("element", ValueType.Text)
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
            await client.db.accessTable(values[0], values[1])
            client.db.removeProperty(values[0], values[1], values[2])
        except ValueError:
            client.errMsg[guild.id] = "[RemoveDBValue - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Invalid code"
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

