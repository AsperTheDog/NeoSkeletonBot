from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class GetUser(Action):
    guildID = -1
    group = "Values"
    templID = 16
    inputs = [
        ValueInput("User ID", ValueType.Number)
    ]
    outputs = [
        ValueOutput("User", ValueType.Structure)
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
        from Bot.utils import formatUser
        usr = client.get_user(values[0])
        if not usr:
            return super().sendEvent(1)
        super().setValue(formatUser(usr, [usr.id]), 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
