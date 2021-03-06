from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class GetGlobalVariable(Action):
    guildID = -1
    group = "Values"
    templID = 41
    inputs = [
        ValueInput("variable", ValueType.Text)
    ]
    outputs = [
        ValueOutput("value", ValueType.Any)
    ]
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
        import datetime
        try:
            super().setValue(client.db.getGlobalVariable(guild.id, values[0]), 0)
        except ValueError:
            client.errMsg[guild.id] = "[GetGlobalVariable - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Global variable not found"
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

