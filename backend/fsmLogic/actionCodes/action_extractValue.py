from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class ExtractValue(Action):
    guildID = -1
    group = "Structure"
    templID = 8
    inputs = [
        ValueInput("Extract tag", ValueType.Text),
        ValueInput("Structure", ValueType.Structure, "UNKNOWN")
    ]
    outputs = [
        ValueOutput("result", ValueType.Any)
    ]
    outEvents = [
        EventOutput("Completed"),
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
            super().setValue(values[1][values[0]], 0)
        except KeyError:
            client.errMsg[guild.id] = "[ExtractValue - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Key received not included in structure"
        super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

