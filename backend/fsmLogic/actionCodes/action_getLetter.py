from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class GetLetter(Action):
    guildID = -1
    group = "Text"
    templID = 9
    inputs = [
        ValueInput("text", ValueType.Text),
        ValueInput("index", ValueType.Number),
    ]
    outputs = [
        ValueOutput("letter", ValueType.Text)
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
            super().setValue(values[0][values[1]], 0)
        except IndexError:
            client.errMsg[guild.id] = "[GetLetter - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Letter index is bigger than text length"
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)