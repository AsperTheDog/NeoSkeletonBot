from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class GetIDFromMention(Action):
    guildID = -1
    group = "Values"
    templID = 58
    inputs = [
        ValueInput("mention", ValueType.Text)
    ]
    outputs = [
        ValueOutput("ID", ValueType.Number)
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
        import re
        import datetime
        idStr = re.match(r"<.+?([0-9]+)>", values[0].strip())
        if not idStr:
            client.errMsg[guild.id] = "[GetIDFromMention - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Invalid mention"
            return super().sendEvent(1)
        try:
            idNum = int(idStr)
        except ValueError:
            client.errMsg[guild.id] = "[GetIDFromMention - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Invalid mention"
            return super().sendEvent(1)
        super().setValue(idNum, 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
