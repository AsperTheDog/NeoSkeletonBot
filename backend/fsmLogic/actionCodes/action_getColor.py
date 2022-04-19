import disnake

from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class GetColor(Action):
    guildID = -1
    group = "Values"
    templID = 49
    inputs = [
        ValueInput("color", ValueType.Combo, "blue", combo=[
            "blue",
            "blurple",
            "brand_green",
            "brand_red",
            "dark_blue",
            "dark_gold",
            "dark_gray",
            "dark_green",
            "dark_grey",
            "dark_magenta",
            "dark_orange",
            "dark_purple",
            "dark_red",
            "dark_teal",
            "dark_theme",
            "darker_gray",
            "darker_grey",
            "default",
            "fuchsia",
            "gold",
            "green",
            "greyple",
            "light_gray",
            "light_grey",
            "lighter_gray",
            "lighter_grey",
            "magenta",
            "og_blurple",
            "old_blurple",
            "orange",
            "purple",
            "red",
            "teal",
            "yellow",
            "random"
        ])
    ]
    outputs = [
        ValueOutput("rgb", ValueType.Structure, "r (Number), g (Number), b (Number)")
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
        import disnake
        color = eval("disnake.Color." + values[0] + "()")
        color = {'r': color.r, 'g': color.g, 'b': color.b}
        super().setValue(color, 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)
