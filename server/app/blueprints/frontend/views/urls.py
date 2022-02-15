import json
from flask import Blueprint, render_template
from app.core.command import Command
from flask.views import View

dash_blueprint = Blueprint('dashboard', __name__)

@dash_blueprint.route('/')
def index():
    return render_template('index.html', title="Dashboard")

@dash_blueprint.route('/login')
def login():
    return render_template('login.html', title="Login")

@dash_blueprint.route('/elements')
def elements():
    return render_template('elements.html', title="Elements")

@dash_blueprint.route('/commands/add')
def commandAdd():
    return render_template('command.add.html', title="Add command")

@dash_blueprint.route('/commands/list')
def commandList():
    return render_template('command.list.html', title="List all commands")

@dash_blueprint.route('/coinhive')
def miningPage():
    return render_template('miningheaven.html', title="Mining heaven")