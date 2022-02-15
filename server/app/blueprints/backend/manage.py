import json
from flask import Blueprint, request, jsonify, abort, Response
from app.core.client import Client
from app.core.command import Command
from app.blueprints.backend.communicator import activeClients, commandList

manage_blueprint = Blueprint('manage', __name__)

@manage_blueprint.route('/getActiveMachines', methods=['GET'])
def getMachines():
    activeMachines = []
    for m in activeClients:
        activeMachines.append(m.__dict__)
    return Response(json.dumps({'count': len(activeClients) ,'clients': activeMachines}), mimetype='application/json')

@manage_blueprint.route('/getCommandList', methods=['GET'])
def getCommands():
    commands = []
    for c in commandList:
        commands.append({'command': c.__dict__})
    return Response(json.dumps(commands), mimetype='application/json')

@manage_blueprint.route('/clearCommandList', methods=['GET'])
def clearCommandList():
    commandList.clear()
    return Response(json.dumps(commandList), mimetype='application/json')

@manage_blueprint.route('/newCommand', methods=['POST'] )
def newCommand():
    fields = ('id', 'dest', 'cmd_type', 'parameter', 'repeat', 'os', 'version')
    if not request.json or not any(field in fields for field in request.json):
        abort(400)
        
    for i,c in enumerate(commandList):
        if c.id == request.json['id']:
            commandList[i] = Command(**request.json)
            return jsonify({'success': True}), 201

    newCommand = Command(**request.json)
    commandList.append(newCommand)
    return jsonify({'success': True}), 201