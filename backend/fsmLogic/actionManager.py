import json


class ActionManager:
    _actions = {}
    _actionIDs = []

    @staticmethod
    def actionclass(cls):
        if cls.guildID not in ActionManager._actions:
            ActionManager._actions[cls.guildID] = {}
        if cls.__name__ not in ActionManager._actions[cls.guildID]:
            ActionManager._actionIDs.append(cls.templID)
        ActionManager._actions[cls.guildID][cls.__name__] = cls
        with open("fsmLogic/dataFiles/tracking/actions.json", "w") as file:
            json.dump(sorted(ActionManager._actionIDs), file, indent=4)

    @staticmethod
    def getAction(action, guild):
        if guild not in ActionManager._actions:
            ActionManager._actions[guild] = {}
        if action not in ActionManager._actions[guild]:
            return ActionManager._actions[-1].get(action)
        return ActionManager._actions[guild][action]

    @staticmethod
    def getActionList(guild):
        if guild not in ActionManager._actions:
            ActionManager._actions[guild] = {}
        return list(ActionManager._actions[guild].items()) + list(ActionManager._actions[-1].items())

    @staticmethod
    def getNewID():
        count = 0
        while count in ActionManager._actionIDs:
            count += 1
        ActionManager._actionIDs.append(count)
        return count

    @staticmethod
    def removeAction(guild, board):
        if guild not in ActionManager._actions or board not in ActionManager._actions[guild]:
            return
        ActionManager._actions[guild].pop(board)