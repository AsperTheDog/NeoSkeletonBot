from fsmLogic.nodeClasses.variable import Variable


class ValueInput:
    def __init__(self, name, valueType, preview=None, combo=None):
        self.inpID = 0
        self.valType = valueType
        self.name = name
        self.preview = preview if preview is not None else str(Variable.getInitValue(valueType))
        if self.valType == 2:
            self.combo = combo
        else:
            self.combo = None

    def __str__(self):
        raise NotImplementedError("Please override function __str__() in your action")

    def getTemplate(self):
        return {
            "id": 0,
            "name": self.name,
            "nature": "in",
            "preview": self.preview,
            "valueType": self.valType,
            "inColor": "black",
            "fromVariable": False,
            "flipped": False,
            "comboValues": self.combo,
            "transitionNumber": 0,
            "offset": {
                "x": 0,
                "y": 0
            }
        }


class ValueOutput:
    def __init__(self, name, valueType, preview=None):
        self.inpID = 0
        self.valType = valueType
        self.preview = preview if preview is not None else str(Variable.getInitValue(valueType))
        self.name = name

    def __str__(self):
        raise NotImplementedError("Please override function __str__() in your action")

    def getTemplate(self):
        return {
            "id": 0,
            "name": self.name,
            "nature": "out",
            "preview": self.preview,
            "valueType": self.valType,
            "inColor": "black",
            "fromVariable": False,
            "flipped": False,
            "comboValues": None,
            "transitionNumber": 0,
            "offset": {
                "x": 0,
                "y": 0
            }
        }


class EventInput:
    def __init__(self):
        self.inpID = 0

    def __str__(self):
        raise NotImplementedError("Please override function __str__() in your action")

    @staticmethod
    def getTemplate():
        return {
            "id": 0,
            "name": "incoming event",
            "nature": "in",
            "flipped": False,
            "transitionNumber": 0,
            "offset": {
                "x": 0,
                "y": 0
            }
        }


class EventOutput:
    def __init__(self, name):
        self.inpID = 0
        self.name = name

    def __str__(self):
        raise NotImplementedError("Please override function __str__() in your action")

    def getTemplate(self):
        return {
            "id": 0,
            "name": self.name,
            "nature": "out",
            "flipped": False,
            "transitionNumber": 0,
            "offset": {
                "x": 0,
                "y": 0
            }
        }
