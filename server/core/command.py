from datetime import datetime

class Command:

    def __init__(self, id, dest, cmd_type, parameter, repeat, os, version):
        self.id = id
        self.dest = dest
        self.type = cmd_type
        self.parameter = parameter
        self.status = 1
        self.success = {}
        self.fail = {}
        self.result = {}
        self.os = os
        self.version = version
        self.repeat = repeat
        self.timestamp = str(datetime.now())

    def updateStatus(self, status):
        self.status = status
    
    def failed(self, machine_ip):
        count = 1
        if machine_ip in self.fail.keys():
            count = self.fail[machine_ip] + 1

        self.fail[machine_ip] = count

    def succeeded(self, machine_ip):
        count = 1
        if machine_ip in self.success.keys():
            count = self.success[machine_ip] + 1

        self.success[machine_ip] = count

    def feedResult(self, machine_ip, result):
        self.result[machine_ip] = result