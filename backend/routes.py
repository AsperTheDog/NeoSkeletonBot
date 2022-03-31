import os

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

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = "8wY7gtqDw8rhhEl4ms89fg"

BoardManager.updateGEvents()
BoardManager.updateValueTypes()


@app.route('/boards', methods=['GET'])
def getBoards():
    exists = SessionManager.existsCookie(request.args.get('token'))
    if not exists:
        return jsonify([])

    return serializeManager.loadBoards(request.args.get('guild'))


@app.route('/actions', methods=['GET'])
def getActions():
    exists = SessionManager.existsCookie(request.args.get('token'))
    if not exists:
        return jsonify([])
    acts = []
    for act in ActionManager.getActionList(int(request.args.get('guild'))):
        acts.append(act[1].getTemplate())

    return jsonify(acts)


@app.route('/revertBoard', methods=['GET'])
def getBoard():
    guild = request.args.get('guild')
    name = request.args.get('name')
    ret = serializeManager.getBoard(guild, name)
    if not ret:
        return abort(400, 'Board not found')
    return ret


@app.route('/getGlobalEvents', methods=['GET'])
def getGlobalEvents():
    return jsonify({'events': BoardManager.globalEvents, 'customActionEvents': BoardManager.customActionEvents})


@app.route('/getValueTypes', methods=['GET'])
def getValueTypes():
    return jsonify(BoardManager.valueTypes)


@app.route('/saveBoard', methods=['POST'])
def saveBoard():
    data = request.get_json()
    ret = serializeManager.saveBoard(data)
    print(ret)
    return jsonify({'status': ret})


@app.route("/deleteBoard/<guild>/<board>", methods=['DELETE'])
def deleteBoard(guild=None, board=None):
    serializeManager.deleteFiles(guild, board)
    ActionManager.removeAction(guild, board)
    return jsonify({'status': 'OK'})


@app.route('/login', methods=['GET'])
def login():
    if 'code' not in request.args:
        return redirect("https://freechmod.ddns.net:12547")
    app.logger.info(request.args['code'])
    data = {
        'client_id': 682744116143980699,
        'client_secret': 'rp4y3LhAvPg-spKrqlmWo82CrNNU1eP7',
        'grant_type': 'authorization_code',
        'code': request.args['code'],
        'redirect_uri': "https://freechmod.ddns.net:12546/login"
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    r.raise_for_status()
    SessionManager.setCode(request.args['code'], {'usr': r.json(), 'guilds': []})
    return redirect("https://freechmod.ddns.net:12547?usrCode=" + request.args['code'])


@app.route('/getToken', methods=['GET', 'POST'])
def getToken():
    return redirect("https://freechmod.ddns.net:12547")


@app.route('/checkCreds', methods=['GET'])
def checkCreds():
    token = SessionManager.checkCookie(request.args.get('token'))
    cde = SessionManager.get(token, request.args.get('code'))
    if not cde:
        return jsonify({"token": token, "usr": {'id': None}})
    ident = requests.get("https://discord.com/api/v9/users/@me", headers={'Authorization': "Bearer " + cde["usr"]['access_token']})
    ident.raise_for_status()
    guilds = requests.get("https://discord.com/api/v9/users/@me/guilds", headers={'Authorization': "Bearer " + cde["usr"]['access_token']}).json()
    SessionManager.setCookie(token, {'usr': cde["usr"], 'guilds': guilds})
    return jsonify({"token": token, "usr": ident.json()})


@app.route('/getGuilds', methods=['GET'])
def getGuilds():
    exists = SessionManager.existsCookie(request.args.get('token'))
    if not exists:
        return jsonify({'guilds': [{'name': 'login to get guilds', 'id': None}]})
    data = SessionManager.get(request.args.get('token'))
    return jsonify([{'name': elem['name'], 'id': elem['id'], 'icon': elem['icon'], 'permissions': elem['permissions']} for elem in data['guilds'] if elem['owner']])


def runFlask():
    app.run(debug=False, host="0.0.0.0", port=12546, ssl_context=('cert/cert.pem', 'cert/key.pem'))