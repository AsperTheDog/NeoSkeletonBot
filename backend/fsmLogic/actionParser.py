import importlib
import inspect
import os

import re

from manager import Board
from fsmLogic.nodeClasses.variable import Variable
from fsmLogic.actionManager import ActionManager

elements = {}


def hashGuildID(guildID):
    hash = ""
    for char in guildID:
        hash += chr(int(char) + 97)
    return hash


def prepareData(data):
    for action in data['actions']:
        elements[action['id']] = {"type": "action", "element": action}
        for input in action['inputs']:
            input['hook'] = -1
            elements[input['id']] = {"type": "inOut", "parent": action['id'], "element": input}
        for output in action['outputs']:
            output['hook'] = []
            elements[output['id']] = {"type": "inOut", "parent": action['id'], "element": output}
        for event in action['events']:
            event['hook'] = -1
            elements[event['id']] = {"type": "event", "parent": action['id'], "element": event}
        elements[action['inputEvent']['id']] = {"type": "event", "parent": action['id'], "element": action['inputEvent']}
    for variable in data['varInstances']:
        elements[variable['id']] = {"type": "varInstance", "element": variable}
        elements[variable['output']['id']] = {"type": "inOut", "parent": variable['id'], "element": variable['output']}
        elements[variable['input']['id']] = {"type": "inOut", "parent": variable['id'], "element": variable['input']}
    for variable in data['variables']:
        elements[variable['id']] = {"type": "variable", "element": variable}
    for pipe in data['pipelines']:
        elements[pipe['id']] = {"type": "pipeline", "element": pipe}
        if pipe['point'] is not None:
            pipe['point']['hook'] = []
            elements[pipe['point']['id']] = {"type": "inOut", "parent": pipe['id'], "element": pipe['point']}
        if pipe['eventPoint'] is not None:
            pipe['eventPoint']['hook'] = -1
            elements[pipe['eventPoint']['id']] = {"type": "event", "parent": pipe['id'], "element": pipe['eventPoint']}
    for gev in data['globalEvents']:
        elements[gev['id']] = {"type": "globalEvent", "element": gev}
        elements[gev['output']['id']] = {"type": "inOut", "parent": gev['id'], "element": gev['output']}
        elements[gev['eventOutput']['id']] = {"type": "event", "parent": gev['id'], "element": gev['eventOutput']}
        gev['output']['hook'] = []
        gev['eventOutput']['hook'] = -1


def getNewID():
    newID = 0
    while newID in elements:
        newID += 1
    return newID


def processConnections(board):
    processedVars = {}

    for transition in board['transitions']:
        origNode, origInput = elements[transition['origin'][0]], elements[transition['origin'][1]]
        destNode, destInput = elements[transition['destination'][0]], elements[transition['destination'][1]]
        if origNode['type'] == "varInstance":
            destInput['element']['hook'] = origNode['element']['varAttr']
        elif destNode['type'] == "varInstance":
            origInput['element']['hook'].append(destNode['element']['varAttr'])
        elif 'valueType' in origInput['element']:
            if transition['destination'][0] not in processedVars:
                newVar = getNewID()
                processedVars[transition['destination'][0]] = newVar
                board['variables'].append({
                    "id": newVar,
                    "initialValue": "",
                    "valueType": destInput['element']['valueType']
                })
                elements[newVar] = {"type": "variable", "element": board['variables'][-1]}
                destInput['element']['hook'] = newVar
                origInput['element']['hook'].append(newVar)
            else:
                origInput['element']['hook'].append(processedVars[transition['destination'][0]])
        else:
            origInput['element']['hook'] = transition['destination'][0]
    board.pop('transitions')
    board.pop('varInstances')


def genCodeFuncs(board, guild):
    functions = []
    funcRefs = []
    for action in board['actions']:
        conns = genCodeConns(action)
        finalCode = ""
        funcRefs.append(str(action['id']))
        actInstance = ActionManager.getAction(action['type'], guild)()
        code = inspect.getsource(actInstance.execute)
        code = code.replace("async def execute(self)", "async def act" + str(action['id']) + "(vrs)")
        matches = set(re.findall(r"values\[([0-9])]", code))
        for match in matches:
            if action['inputs'][int(match)]['hook'] == -1:
                inpVal = str(Variable.getInitValue(action['inputs'][int(match)]['valueType']))
            else:
                inpVal = "vrs[" + str(action['inputs'][int(match)]['hook']) + "]"
            code = code.replace("values[" + match + "]", inpVal)
        for line in code.splitlines():
            if line.strip() == "values = super().getValues()" or \
                    line.strip() == "async def changeVar(vrs, vr, val):" or \
                    line.strip() == "async with vrs['lock']:" or \
                    line.strip() == "vrs[vr] = val":
                code = code.replace(line + "\n", "")
            else:
                count = 0
                for cha in line:
                    if cha != ' ':
                        break
                    count += 1
                tabs = " " * count
                matches = re.findall(r"super\(\)\.sendEvent\((\S+)\)", line)
                if len(matches) != 0:
                    code = code.replace(line, tabs + "return pipes[" + matches[0] + "]")
                else:
                    matches = re.findall(r"super\(\)\.setValue\(([^,]+),([ 0-9]+)\)", line)
                    if len(matches) != 0:
                        outs = action['outputs'][int(matches[0][1])]['hook']
                        outStr = ""
                        for out in outs:
                            outStr += tabs + "await changeVar(vrs, " + str(out) + ", " + matches[0][0] + ")\n"
                        outStr = outStr[:-1]
                        code = code.replace(line, outStr)
        finalCode += "    " + code.splitlines()[0] + "\n"
        finalCode += conns
        for line in code.splitlines()[1:]:
            finalCode += "    " + line + "\n"
        functions.append(finalCode)

    return functions, funcRefs


def genCodeConns(act):
    conns = "            pipes = {\n"
    for count, ev in enumerate(act['events']):
        conns += "                " + str(count) + ": " + str(ev['hook']) + ",\n"
    conns += "            }\n"
    return conns


def genCodeVars(board, isMain=False):
    bName = board['name'].replace(" ", "").strip()
    if isMain:
        variables = "    vrs_Main = {\n"
        tabs = "    "
    else:
        variables = "        vrs_" + bName + " = {\n"
        tabs = "        "
    variables += tabs + "    " + "'lock': asyncio.Lock(),\n"
    for variable in board['variables']:
        if variable['initialValue'] == "":
            initVal = Variable.getInitValue(variable['valueType'])
        else:
            initVal = variable['initialValue']
        if variable['valueType'] == 0:
            variables += tabs + "    " + str(variable['id']) + ": " + str(initVal) + ",\n"
        else:
            variables += tabs + "    " + str(variable['id']) + ": '" + str(initVal) + "',\n"
    variables += tabs + "}\n"
    return variables


def genCodePipelines(board):
    pipelines = {'in': [], 'out': [], 'inEvent': None, 'outEvent': []}
    for pipe in board['pipelines']:
        if pipe['type'] == "actionValueInput":
            pipelines['in'].append({'name': pipe['name'], 'valueType': pipe['point']['valueType'], 'hook': pipe['point']['hook']})
        elif pipe['type'] == "actionValueOutput":
            pipelines['out'].append({'name': pipe['name'], 'valueType': pipe['point']['valueType'], 'hook': pipe['point']['hook']})
        elif pipe['type'] == "actionEventInput":
            pipelines['inEvent'] = {'id': pipe['id'], 'name': pipe['name'], 'hook': pipe['eventPoint']['hook']}
        elif pipe['type'] == "actionEventOutput":
            pipelines['outEvent'].append({'id': pipe['id'], 'name': pipe['name'], 'hook': pipe['eventPoint']['hook']})
    return pipelines


def genCodeGEvents(board):
    gEvents = {event: [] for event in Board.globalEvents}
    for event in board['globalEvents']:
        gEvents[event['name']].append((event['output']['hook'], event['eventOutput']['hook']))
    return gEvents


def genCodeAction(board, guild, actID=None):
    bName = board['name'].replace(" ", "").strip()
    functions, funcRefs = genCodeFuncs(board, guild)
    variables = genCodeVars(board)
    pipelines = genCodePipelines(board)

    finalCode = "from fsmLogic.nodeClasses.actionTemplate import Action\n"
    finalCode += "from fsmLogic.actionManager import ActionManager\n"
    finalCode += "from fsmLogic.nodeClasses.inputs import ValueInput, ValueOutput, EventOutput\n"
    finalCode += "import asyncio\n"
    finalCode += "\n\n"
    finalCode += "@ActionManager.actionclass\n"
    finalCode += "class " + bName + "(Action):\n"
    if not actID:
        finalCode += "    templID = " + str(ActionManager.getNewID()) + "\n"
    else:
        finalCode += "    templID = " + str(actID) + "\n"
    finalCode += "    guildID = '" + guild + "'\n"
    finalCode += "    inputs = [\n"
    for inPipe in pipelines['in']:
        finalCode += "        ValueInput(0, '" + inPipe['name'] + "', " + str(inPipe['valueType']) + ", None),\n"
    finalCode += "    ]\n"
    finalCode += "    outputs = [\n"
    for outPipe in pipelines['out']:
        finalCode += "        ValueOutput(0, '" + outPipe['name'] + "', " + str(outPipe['valueType']) + ", None),\n"
    finalCode += "    ]\n"
    finalCode += "    outEvents = [\n"
    for outEvPipe in pipelines['outEvent']:
        finalCode += "        EventOutput(0, '" + outEvPipe['name'] + "'),\n"
    finalCode += "    ]\n"
    finalCode += "\n"
    finalCode += "    def __init__(self):\n"
    finalCode += "        super().__init__()\n"
    finalCode += "        super().addConnections(self.__class__.inputs, self.__class__.outputs, self.__class__.outEvents)\n"
    finalCode += "\n"
    finalCode += "    async def execute(self):\n"
    finalCode += "        values = super().getValues()\n"
    finalCode += "        async def changeVar(vrs, vr, val):\n"
    finalCode += "            async with vrs['lock']:\n"
    finalCode += "                vrs[vr] = val\n"
    finalCode += "\n"
    for func in functions:
        finalCode += func
        finalCode += "\n"
    finalCode += variables
    finalCode += "        actions_" + bName + " = {\n"
    for func in funcRefs:
        finalCode += "            " + func + ": act" + func + ",\n"
    finalCode += "        }\n"
    finalCode += "        nxt_" + bName + " = " + str(pipelines['inEvent']['hook']) + "\n"
    finalCode += "        events_" + bName + " = {\n"
    for count, evOutPipe in enumerate(pipelines['outEvent']):
        finalCode += "            " + str(evOutPipe['id']) + ": " + str(count) + ",\n"
    finalCode += "        }\n"
    for count, inPipe in enumerate(pipelines['in']):
        for hook in inPipe['hook']:
            finalCode += "        vrs_" + bName + "[" + str(hook) + "] = values[" + str(count) + "]\n"
    finalCode += "        while nxt_" + bName + " in actions_" + bName + ":\n"
    finalCode += "            nxt_" + bName + " = await actions_" + bName + "[nxt_" + bName + "](vrs_" + bName + ")\n"
    for count, outPipe in enumerate(pipelines['out']):
        finalCode += "        super().setValue(vrs_" + bName + "[" + str(outPipe['hook']) + "], " + str(count) + ")\n"
    finalCode += "        return super().sendEvent(events_" + bName + "[nxt_" + bName + "])\n"
    finalCode += "\n"
    finalCode += "    @classmethod\n"
    finalCode += "    def getTemplate(cls):\n"
    finalCode += "        return super().getTemplate(cls)\n"

    if not os.path.isdir("fsmLogic/actionCodes/custom/" + hashGuildID(guild)):
        os.mkdir("fsmLogic/actionCodes/custom/" + hashGuildID(guild))
        with open("fsmLogic/actionCodes/custom/" + hashGuildID(guild) + "/__init__.py", "w") as file:
            file.write(
                "from os.path import dirname, basename, isfile, join\n"
                "import glob\n"
                "\n"
                "modules = glob.glob(join(dirname(__file__), '*.py'))\n"
                "__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]\n"
            )

    with open("fsmLogic/actionCodes/custom/" + hashGuildID(guild) + "/action_" + board['name'] + ".py", "w") as file:
        file.write(finalCode)


def genCodeMain(board, guild):
    functions, funcRefs = genCodeFuncs(board, guild)
    variables = genCodeVars(board, True)
    gEvs = genCodeGEvents(board)

    finalCode = "from fsmLogic.actionManager import ActionManager\n"
    finalCode += "import asyncio\n"
    finalCode += "\n\n"
    finalCode += "@ActionManager.actionclass\n"
    finalCode += "class MainBoard_" + guild + ":\n"
    finalCode += "    guildID = '" + guild + "'\n"
    finalCode += variables
    finalCode += "\n"
    finalCode += "    def __init__(self):\n"
    finalCode += "        super().__init__()\n"
    finalCode += "\n"
    finalCode += "    async def execute(self, initNext, initVar, initValue):\n"
    finalCode += "        async def changeVar(vrs, vr, val):\n"
    finalCode += "            async with vrs['lock']:\n"
    finalCode += "                vrs[vr] = val\n"
    finalCode += "\n"
    for func in functions:
        finalCode += func
        finalCode += "\n"
    finalCode += "        actions_Main = {\n"
    for func in funcRefs:
        finalCode += "            " + func + ": act" + func + ",\n"
    finalCode += "        }\n"
    finalCode += "        nxt_Main = initNext\n"
    finalCode += "        await changeVar(MainBoard_" + guild + ".vrs_Main, initVar, initValue)\n"
    finalCode += "        while nxt_Main in actions_Main:\n"
    finalCode += "            nxt_Main = await actions_Main[nxt_Main](MainBoard_" + guild + ".vrs_Main)\n"
    finalCode += "\n"

    with open("fsmLogic/mains/mainBoard_" + guild + ".py", "w") as file:
        file.write(finalCode)


def compileMain(board, guild):
    prepareData(board)
    processConnections(board)
    genCodeMain(board, guild)


def compileAction(board, guild):
    act = ActionManager.getAction(board['name'], guild)
    actID = None
    if act:
        actID = act.templID
    prepareData(board)
    processConnections(board)
    genCodeAction(board, guild, actID)

    importlib.import_module("fsmLogic.actionCodes.custom." + hashGuildID(guild) + ".action_" + board['name'])
