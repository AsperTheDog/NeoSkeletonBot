from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class ReplaceCharacter(Action):
    guildID = -1
    group = "Text"
    templID = 71
    inputs = [
        ValueInput("text", ValueType.Text),
        ValueInput("char", ValueType.Text),
        ValueInput("index", ValueType.Number)
    ]
    outputs = [
        ValueOutput("text", ValueType.Text)
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
            super().setValue(values[0][:values[2]] + values[1] + values[0][values[2] + 1:], 0)
        except KeyError:
            client.errMsg[guild.id] = "[ReplaceCharacter - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Index is bigger than text length"
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

