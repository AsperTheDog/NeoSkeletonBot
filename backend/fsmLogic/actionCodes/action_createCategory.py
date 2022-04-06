import disnake

from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class CreateCategory(Action):
    guildID = -1
    group = "Interaction"
    templID = 47
    inputs = [
        ValueInput("name", ValueType.Text),
        ValueInput("reason", ValueType.Text)
    ]
    outputs = [
        ValueOutput("categoryID", ValueType.Number)
    ]
    outEvents = [
        EventOutput("completed")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)
        cat = await guild.create_category(values[0], reason=values[1] if values[1] != "" else None)
        super().setValue(cat.id, 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
