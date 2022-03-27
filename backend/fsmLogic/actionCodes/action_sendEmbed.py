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
        import datetime
        try:
            embed = disnake.Embed()
            if values[0]["title"] != "":
                embed.title = values[0]["title"]
            if values[0]["description"] != "":
                embed.description = values[0]["description"]
            if values[0]["color"] != "":
                embed.colour = values[0]["color"]
            if values[0]["url"] != "":
                embed.url = values[0]['url']
            for field in values[0]['fields']:
                embed.add_field(field["name"], field["value"], inline=field["inline"])
            if "footer" in values[0]:
                embed.set_footer(text=values[0]["footer"])
        except KeyError:
            client.errMsg[guild] = "[SendEmbed - " + datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "] Invalid embed structure"
            return super().sendEvent(1)
        ch = client.get_channel(values[1])
        if not ch:
            return super().sendEvent(1)
        await ch.send(embed=embed)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)