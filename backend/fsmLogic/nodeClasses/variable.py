from fsmLogic.nodeClasses.valueTypes import ValueType


class Variable:
    def __init__(self, varID, name, valueType, initialValue):
        self.varID = varID
        self.name = name
        self.valueType = valueType
        if self.valueType == ValueType.Number:
            self.value = int(initialValue)
        else:
            self.value = initialValue

    def setValue(self, newVal):
        if self.valueType == ValueType.Number:
            self.value = int(newVal)
        else:
            self.value = newVal

    def getValue(self):
        return self.value

    @staticmethod
    def serialize(name, valType, combo):
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

    @staticmethod
    def getInitValue(param):
        if param == 0:
            return 0
        elif param == 1:
            return "''"
        elif param == 5:
            return False
        else:
            return None

    @staticmethod
    def checkValueType(param):
        return not ValueType.getType(param['type']) or type(param['value']) == ValueType.getType(param['type'])
