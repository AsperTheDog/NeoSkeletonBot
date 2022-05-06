import os
import random
import pickle
import asyncio
import sys


class SkeletonDB:
    def __init__(self):
        self.root = "database/dbFiles/"
        self.access = {}
        self.locks = {'lock': asyncio.Lock(), 'tables': {}, 'gvars': {}}
        self.sendToDel = set()
        self.globals = {}

    def _getNewCode(self):
        code = random.randint(0, 9999999999)
        while code in self.access:
            code = random.randint(0, 9999999999)
        return code

    def _exists(self, *, code, table=None, element=None, row=None):
        if code not in self.access \
                or (table is not None and table not in self.access[code]['tables']) \
                or (element is not None and element not in self.access[code]['tables'][table]['template']) \
                or (row is not None and row not in self.access[code]['tables'][table]['table']):
            return False
        return True

    async def _lockTable(self, table, guild):
        async with self.locks['lock']:
            if guild not in self.locks['tables']:
                self.locks['tables'][guild] = {}
            if table not in self.locks['tables'][guild]:
                self.locks['tables'][guild][table] = {'lock': asyncio.Lock(), 'using': 1}
            else:
                self.locks['tables'][guild][table]['using'] += 1
        await self.locks['tables'][guild][table]['lock'].acquire()

    async def _releaseTable(self, table, code):
        guild = self.access[code]['guild']
        self.locks['tables'][guild][table]['lock'].release()
        async with self.locks['lock']:
            if self.locks['tables'][guild][table]['using'] <= 1:
                self.locks['tables'][guild].pop(table)
            else:
                self.locks['tables'][guild][table]['using'] -= 1

    async def accessTable(self, code, table):
        if not self._exists(code=code):
            raise ValueError()
        if table in self.access[code]['tables']:
            if table in self.sendToDel:
                self.sendToDel.remove(table)
            return
        guild = self.access[code]['guild']
        await self._lockTable(table, guild)
        try:
            with open(self.root + str(guild) + "/_" + table, "rb") as file:
                data = pickle.load(file)
        except FileNotFoundError:
            data = {'table': {}, 'template': {}}
        self.access[code]['tables'][table] = {'table': data['table'], 'template': data['template']}

    def deleteTable(self, code, table):
        if not self._exists(code=code, table=table):
            return
        try:
            self.access[code]['tables'][table] = {'table': {}, 'template': {}}
            self.sendToDel.add(table)
        except KeyError:
            return

    def start(self, guild):
        code = self._getNewCode()
        self.access[code] = {
            'tables': {},
            'guild': guild
        }
        return code

    async def save(self, code):
        if code not in self.access:
            raise ValueError()
        guild = self.access[code]['guild']
        path = self.root + str(guild)
        for name, table in self.access[code]['tables'].items():
            if name in self.sendToDel:
                if os.path.isfile(path + "/_" + name):
                    os.remove(path + "/_" + name)
                    if len(os.listdir(path)) == 0:
                        os.rmdir(path)
                self.sendToDel.remove(name)
            else:
                if not os.path.isdir(path):
                    os.mkdir(path)
                with open(path + "/_" + name, "wb") as db:
                    pickle.dump(table, db)
            await self._releaseTable(name, code)
        self.access.pop(code)

    async def cancel(self, code):
        for name in self.access[code]['tables']:
            await self._releaseTable(name, code)
        self.access.pop(code)

    def defineProperty(self, code, table, element, initValue):
        if not self._exists(code=code, table=table):
            raise ValueError()
        if self._exists(code=code, table=table, element=element):
            return
        self.access[code]['tables'][table]['template'][element] = initValue
        for row in self.access[code]['tables'][table]['table'].values():
            row[element] = initValue

    def removeProperty(self, code, table, element):
        if not self._exists(code=code, table=table, element=element):
            return
        self.access[code]['tables'][table]['template'].pop(element)
        for row in self.access[code]['tables'][table]['table'].values():
            row.pop(element)

    def resetProperty(self, code, table, element):
        if not self._exists(code=code, table=table, element=element):
            raise ValueError()
        for row in self.access[code]['tables'][table]['table'].values():
            row[element] = self.access[code]['tables'][table]['template'][element]

    def addRow(self, code, table, row):
        if not self._exists(code=code, table=table):
            raise ValueError()
        if self._exists(code=code, table=table, row=row):
            return
        self.access[code]['tables'][table]['table'][row] = {key: val for key, val in self.access[code]['tables'][table]['template'].items()}

    def setValue(self, code, table, row, element, value):
        if not self._exists(code=code, table=table, row=row, element=element):
            raise ValueError()
        self.access[code]['tables'][table]['table'][row][element] = value

    def getData(self, code, table, row, element=None):
        if not self._exists(code=code, table=table, row=row, element=element):
            raise ValueError()
        if element is None:
            return self.access[code]['tables'][table]['table'][row]
        else:
            return self.access[code]['tables'][table]['table'][row][element]

    def getTable(self, code, table):
        if not self._exists(code=code, table=table):
            raise ValueError()
        return self.access[code]['tables'][table]['table']

    def removeRow(self, code, table, row):
        if not self._exists(code=code, table=table, row=row):
            return
        self.access[code]['tables'][table]['table'].pop(row)

    def emptyTable(self, code, table):
        if not self._exists(code=code, table=table):
            raise ValueError()
        self.access[code]['tables'][table]['table'] = {}

    def tableIsLoaded(self, code, table):
        return self._exists(code=code, table=table)

    def setGlobalVariable(self, guild, var, value):
        path = self.root + str(guild)
        data = {}
        if not os.path.isdir(path):
            os.mkdir(path)
        elif os.path.isfile(path + "/globals"):
            with open(path + "/globals", "rb") as file:
                data = pickle.load(file)
        self.globals[guild] = data
        self.globals[guild][var] = value
        with open(path + "/globals", "wb") as db:
            pickle.dump(self.globals[guild], db)

    def getGlobalVariable(self, guild, var):
        path = self.root + str(guild)
        data = {}
        if not os.path.isdir(path):
            os.mkdir(path)
        elif os.path.isfile(path + "/globals"):
            with open(path + "/globals", "rb") as file:
                data = pickle.load(file)
        self.globals[guild] = data
        try:
            return self.globals[guild][var]
        except KeyError:
            raise ValueError

    def getSize(self, code, table):
        if not self._exists(code=code, table=table):
            raise ValueError()
        return sys.getsizeof(self.access[code]['tables'][table]['table'])
