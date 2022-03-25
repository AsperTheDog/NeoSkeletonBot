from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class SendEmbed(Action):
    guildID = -1
    group = "Embed"
    templID = 12
    inputs = [
        ValueInput("embed", ValueType.Structure),
        ValueInput("channel", ValueType.Number)
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
        import disnake
        try:
            embed = disnake.Embed()
            if values[0]['value']["title"] != "":
                embed.title = values[0]['value']["title"]
            if values[0]['value']["description"] != "":
                embed.description = values[0]['value']["description"]
            if values[0]['value']["color"] != "":
                embed.colour = values[0]['value']["color"]
            if values[0]['value']["url"] != "":
                embed.url = values[0]['value']['url']
            for field in values[0]['value']['fields']:
                embed.add_field(field["name"], field["value"], inline=field["inline"])
            if "footer" in values[0]['value']:
                embed.set_footer(text=values[0]['value']["footer"])
        except KeyError:
            return super().sendEvent(1)
        ch = client.get_channel(values[1]['value'])
        if not ch:
            return super().sendEvent(1)
        await ch.send(embed=embed)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)