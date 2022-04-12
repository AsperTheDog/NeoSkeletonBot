import json
import os
import yaml

from flask import Flask, jsonify, request, redirect, abort
from flask_cors import CORS
import requests

from fsmLogic import serializeManager
from fsmLogic.actionManager import ActionManager
from fsmLogic.boardManager import BoardManager
from SessionManager import SessionManager

exec("from fsmLogic.mains import *")
exec("from fsmLogic.actionCodes import *")
actionPaths = os.listdir("fsmLogic/actionCodes/custom")
for pth in actionPaths:
    if pth != ".gitkeep":
        exec("from fsmLogic.actionCodes.custom." + pth + " import *")

with open('Bot/bot.yaml') as f:
    botCreds = yaml.load(f, Loader=yaml.FullLoader)

frontURL = ""
backURL = ""

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = "8wY7gtqDw8rhhEl4ms89fg"

BoardManager.updateGEvents()
BoardManager.updateValueTypes()


@app.route('/boards', methods=['POST', 'GET'])
def getBoards():
    if request.method == "POST":
        data = request.get_json()
        ret = serializeManager.saveBoard(data)
        print(ret)
        return jsonify({'status': ret})
    exists = SessionManager.existsCookie(request.args.get('token'))
    if not exists:
        return jsonify([])

    return serializeManager.loadBoards(request.args.get('guild'))


@app.route('/boards/<guild>/<board>', methods=['GET', 'DELETE'])
def boards(guild=None, board=None):
    if request.method == "DELETE":
        serializeManager.deleteFiles(guild, board)
        ActionManager.removeAction(guild, board)
        return jsonify({'status': 'OK'})
    elif request.method == "GET":
        ret = serializeManager.getBoard(guild, board)
        if not ret:
            return abort(400, 'Board not found')
        return ret


@app.route('/actions', methods=['GET'])
def getActions():
    exists = SessionManager.existsCookie(request.args.get('token'))
    if not exists:
        return jsonify([])
    acts = []
    for act in ActionManager.getActionList(int(request.args.get('guild'))):
        acts.append(act[1].getTemplate())

    return jsonify(acts)


@app.route('/globalEvents', methods=['GET'])
def getGlobalEvents():
    return jsonify({'events': BoardManager.globalEvents, 'customActionEvents': BoardManager.customActionEvents})


@app.route('/valueTypes', methods=['GET'])
def getValueTypes():
    return jsonify(BoardManager.valueTypes)


@app.route('/login', methods=['GET'])
def login():
    if 'code' not in request.args:
        return redirect(frontURL)
    app.logger.info(request.args['code'])
    data = {
        'client_id': botCreds['clientID'],
        'client_secret': botCreds['clientSecret'],
        'grant_type': 'authorization_code',
        'code': request.args['code'],
        'redirect_uri': backURL + "/login"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    r.raise_for_status()
    SessionManager.setCode(request.args['code'], {'usr': r.json(), 'guilds': []})
    return redirect(frontURL + "?usrCode=" + request.args['code'])


@app.route('/token', methods=['GET', 'POST'])
def getToken():
    return redirect(frontURL)


@app.route('/credentials', methods=['GET'])
def checkCreds():
    token = SessionManager.checkCookie(request.args.get('token'))
    cde = SessionManager.get(token, request.args.get('code'))
    if not cde:
        return jsonify({"token": token, "usr": {'id': None}})
    ident = requests.get("https://discord.com/api/v9/users/@me", headers={'Authorization': "Bearer " + cde["usr"]['access_token']})
    ident.raise_for_status()
    guildList = requests.get("https://discord.com/api/v9/users/@me/guilds", headers={'Authorization': "Bearer " + cde["usr"]['access_token']}).json()
    SessionManager.setCookie(token, {'usr': cde["usr"], 'guilds': guildList})
    return jsonify({"token": token, "usr": ident.json()})


@app.route('/guilds', methods=['GET'])
def guilds():
    exists = SessionManager.existsCookie(request.args.get('token'))
    if not exists:
        return jsonify({'guilds': [{'name': 'login to get guilds', 'id': None}]})
    data = SessionManager.get(request.args.get('token'))
    return jsonify([{'name': elem['name'], 'id': elem['id'], 'icon': elem['icon'], 'permissions': elem['permissions']} for elem in data['guilds'] if elem['owner']])


def runFlask(firstArg):
    global frontURL, backURL

    isHttps = True if firstArg == "https" else False
    with open("../config.json", "r") as file:
        configs = json.load(file)
    frontURL = ("https://" if isHttps else "http://") + configs['rootAddr'] + ":" + str(configs['frontPort'])
    backURL = ("https://" if isHttps else "http://") + configs['rootAddr'] + ":" + str(configs['backPort'])

    if firstArg == "https":
        app.run(debug=False, host=configs['backListen'], port=12546, ssl_context=('cert/cert.pem', 'cert/key.pem'))
    else:
        app.run(debug=False, host=configs['backListen'], port=12546)
