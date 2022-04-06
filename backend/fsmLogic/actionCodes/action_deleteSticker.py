from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class DeleteSticker(Action):
    guildID = -1
    group = "Interaction"
    templID = 56
    inputs = [
        ValueInput("sticker", ValueType.Text),
        ValueInput("reason", ValueType.Text)
    ]
    outputs = []
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
        from http.client import HTTPException
        stickers = guild.stickers
        sticker = None
        try:
            idSt = int(values[0])
        except ValueError:
            idSt = None
        for st in stickers:
            if idSt and st.id == idSt:
                sticker = st
                break
            elif st.name == values[0]:
                sticker = st
                break
        if not sticker:
            client.errMsg[guild.id] = "[DeleteEmoji - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Could not find the sticker"
            return super().sendEvent(1)
        try:
            await guild.delete_sticker(sticker, reason=values[1] if values[1] != "" else None)
        except HTTPException:
            client.errMsg[guild.id] = "[DeleteEmoji - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Discord could not delete the sticker"
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)

