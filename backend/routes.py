import asyncio
import json
import os

from quart import Quart, jsonify, request, redirect
from quart_cors import cors
import requests

from fsmLogic import serializeManager
from fsmLogic.actionManager import ActionManager
from manager import Board
from SessionManager import SessionManager

from Bot.bot import runBot

exec("from fsmLogic.actionCodes import *")
actionPaths = os.listdir("fsmLogic/actionCodes/custom")
for pth in actionPaths:
    exec("from fsmLogic.actionCodes.custom." + pth + " import *")

app = Quart(__name__)
cors(app)
app.config['SECRET_KEY'] = "8wY7gtqDw8rhhEl4ms89fg"

Board.updateGEvents()


@app.route('/boards', methods=['GET'])
async def getBoards():
    exists = SessionManager.existsCookie(request.args.get('token'))
    if not exists:
        return jsonify([])

    return serializeManager.loadBoards(request.args.get('guild'))


@app.route('/actions', methods=['GET'])
async def getActions():
    exists = SessionManager.existsCookie(request.args.get('token'))
    if not exists:
        return jsonify([])
    acts = []
    for act in ActionManager.getActionList(request.args.get('guild')):
        acts.append(act[1].getTemplate())

    return jsonify(acts)


@app.route('/gEvents')
async def getGlobalEvents():
    return jsonify(Board.globalEvents)


@app.route('/saveBoard', methods=['POST'])
async def saveBoard():
    data = json.loads(await request.get_data())
    ret = serializeManager.saveBoard(data)
    return jsonify({'status': 'OK', 'data': ret}) if ret else jsonify({'status': 'OK', 'data': None})


@app.route('/login', methods=['GET'])
async def login():
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
async def getToken():
    return redirect("https://freechmod.ddns.net:12547")


@app.route('/checkCreds', methods=['GET'])
async def checkCreds():
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
async def getGuilds():
    exists = SessionManager.existsCookie(request.args.get('token'))
    if not exists:
        return jsonify({'guilds': [{'name': 'login to get guilds', 'id': None}]})
    data = SessionManager.get(request.args.get('token'))
    return jsonify([{'name': elem['name'], 'id': elem['id'], 'icon': elem['icon'], 'permissions': elem['permissions']} for elem in data['guilds'] if elem['owner']])
