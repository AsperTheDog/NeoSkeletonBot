from fsmLogic.nodeClasses.actionTemplate import Action
from fsmLogic.actionManager import ActionManager
from fsmLogic.nodeClasses.inputs import ValueInput, EventOutput, ValueOutput
from fsmLogic.nodeClasses.valueTypes import ValueType


@ActionManager.actionclass
class Command(Action):
    guildID = -1
    group = "Command"
    templID = 1
    inputs = [
        ValueInput("raw text", ValueType.Text)
    ]
    outputs = [
        ValueOutput("command", ValueType.Text),
        ValueOutput("arguments", ValueType.Structure, "0 (Text)\n1 (Text)\n2 (Text)\n...")
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
        import shlex
        cmd = values[0].split(" ", 1)
        mainCmd = cmd[0]
        if len(cmd) > 1:
            args = cmd[1]
            try:
                args = shlex.split(args)
            except ValueError:
                args = shlex.split(args + '"')
            args = {str(count): arg for count, arg in enumerate(args)}
            super().setValue(mainCmd, 0)
            super().setValue(args, 1)
        else:
            super().setValue(mainCmd, 0)
            super().setValue({}, 1)
        return super().sendEvent(0)

    @classmethod
    def getTemplate(cls):
        return super().getTemplate(cls)