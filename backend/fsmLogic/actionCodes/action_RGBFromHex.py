from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class RGBFromHex(Action):
    guildID = -1
    group = "Values"
    templID = 19
    inputs = [
        ValueInput("Hex", ValueType.Text)
    ]
    outputs = [
        ValueOutput("RBG", ValueType.Structure)
    ]
    outEvents = [
        EventOutput("Completed"),
        EventOutput("Error")
    ]

    def __init__(self):
        super().__init__()
        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)

    async def execute(self, client, guild):
        values = super().getValues()
        super().checkValues(values)
        h = values[0]['value'].lstrip('#')
        try:
            rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            return super().sendEvent(1)
        rgb = {'r': rgb[0], 'g': rgb[1], 'b': rgb[2]}
        super().setValue(rgb, 0)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)