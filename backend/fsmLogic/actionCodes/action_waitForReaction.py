import disnake

from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class WaitForReaction(Action):
    guildID = -1
    group = "Interaction"
    templID = 24
    inputs = [
        ValueInput("Message", ValueType.Number),
        ValueInput("Timeout", ValueType.Number)
    ]
    outputs = [
        ValueOutput("Author", ValueType.Number),
        ValueOutput("EmojiReaction", ValueType.Text)
    ]
    outEvents = [
        EventOutput("completed"),
        EventOutput("timeout")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)

        def check(reaction, user):
            return reaction.message.id == values[0]

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=values[1] if values[1] > 0 else None, check=check)
        except TimeoutError:
            return super().sendEvent(1)
        super().setValue(user.id, 0)
        if isinstance(reaction.emoji, str):
            super().setValue(reaction.emoji, 1)
        else:
            super().setValue(reaction.emoji.name, 1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
