class ValueInput:
    def __init__(self, inpID, name, valueType, connection, combo=None):
        self.inpID = inpID
        self.valType = valueType
        self.name = name
        self.connection = connection
        if self.valType == 2:
            self.combo = combo
        else:
            self.combo = None

    def __str__(self):
        raise NotImplementedError("Please override function __str__() in your action")

    @staticmethod
    def getTemplate(name, valType, combo):
        return {
            "id": 0,
            "name": name,
            "nature": "in",
            "valueType": valType,
            "inColor": "black",
            "fromVariable": False,
            "flipped": False,
            "comboValues": combo,
            "transitionNumber": 0,
            "offset": {
                "x": 0,
                "y": 0
            }
        }


class ValueOutput:
    def __init__(self, inpID, name, valueType, connection):
        self.inpID = inpID
        self.valType = valueType
        self.name = name
        self.connection = connection

    def __str__(self):
        raise NotImplementedError("Please override function __str__() in your action")

    @staticmethod
    def getTemplate(name, valType):
        return {
          "id": 0,
          "name": name,
          "nature": "out",
          "valueType": valType,
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
    def __init__(self, inpID):
        self.inpID = inpID

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
    def __init__(self, inpID, name):
        self.inpID = inpID
        self.name = name

    def __str__(self):
        raise NotImplementedError("Please override function __str__() in your action")

    @staticmethod
    def getTemplate(name):
        return {
            "id": 0,
            "name": name,
            "nature": "out",
            "flipped": False,
            "transitionNumber": 0,
            "offset": {
                "x": 0,
                "y": 0
            }
        }
