import disnake

from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class GetUser(Action):
    guildID = -1
    group = "Values"
    templID = 11
    inputs = [
        ValueInput("user ID", ValueType.Number)
    ]
    outputs = [
        ValueOutput("user", ValueType.Structure, "id (Number)\navatar (Text)\nbot (Boolean)\nbanner (Text)\ncreated date (Datetime)\nname (Text)\nnick (Text)\ndiscriminator (Text)\nfullUsername (Text)\nmention (Text)\ntop role ID (Number)")
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
        from Bot.utils import formatMember
        import datetime
        usr = await guild.getch_member(values[0])
        if not usr:
            client.errMsg[guild.id] = "[GetUser - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Could not find user"
            return super().sendEvent(1)
        super().setValue(formatMember(usr), 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
