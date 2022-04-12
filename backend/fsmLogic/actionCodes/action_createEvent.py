from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class CreateEvent(Action):
    guildID = -1
    group = "Interaction"
    templID = 50
    inputs = [
        ValueInput("name", ValueType.Text),
        ValueInput("description", ValueType.Text),
        ValueInput("start time", ValueType.Datetime),
        ValueInput("end time", ValueType.Datetime),
        ValueInput("event type", ValueType.Combo, "stage", combo=[
            "stage",
            "voice",
            "custom"
        ]),
        ValueInput("channel ID", ValueType.Number),
        ValueInput("external location", ValueType.Text),
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
        import disnake
        from http.client import HTTPException
        if values[6] != "":
            metadata = disnake.GuildScheduledEventMetadata()
            metadata.location = values[6]
        if values[4] == "stage":
            entity = disnake.GuildScheduledEventEntityType.stage_instance
        elif values[4] == "voice":
            entity = disnake.GuildScheduledEventEntityType.voice
        else:
            entity = disnake.GuildScheduledEventEntityType.external
        try:
            await guild.create_scheduled_event(name=values[0], entity_type=entity, description=values[1], scheduled_start_time=values[2], scheduled_end_time=values[3], channel_id=values[5], entity_metadata=metadata, reason=values[7] if values[7] != "" else None)
        except HTTPException:
            client.errMsg[guild.id] = "[CreateEvent - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Discord could not create the event"
            return super().sendEvent(1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
