from enum import IntEnum
from datetime import datetime

values = {
    0: int,
    1: str,
    2: str,
    3: dict,
    5: bool,
    6: str,
    7: datetime
}


class ValueType(IntEnum):
    Number = 0
    Text = 1
    Combo = 2
    Structure = 3
    Any = 4
    Boolean = 5
    Datetime = 6

    @staticmethod
    def getType(elem):
        if elem in values:
            return values[elem]

    @staticmethod
    def getNow():
        import datetime
        return datetime.datetime.now()

    @staticmethod
    def isStr(elem):
        if elem == ValueType.Text or elem == ValueType.Combo:
            return True
        return False
