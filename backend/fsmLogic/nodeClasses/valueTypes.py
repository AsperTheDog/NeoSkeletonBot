from enum import IntEnum

values = {
    0: int,
    1: str,
    2: str,
    3: dict,
    5: bool,
    6: str
}

class ValueType(IntEnum):
    Number = 0
    Text = 1
    Combo = 2
    Structure = 3
    Any = 4
    Boolean = 5

    @staticmethod
    def getType(elem):
        if elem in values:
            return values[elem]
