from datetime import datetime

class Client:

    def __init__(self, **kwargs):
        self.name = kwargs['machine_name']
        self.ip = kwargs['machine_ip']
        self.so = kwargs['system_version']
        self.status = 1
        self.info = kwargs['system_info']
        self.version = kwargs['botnet_version']
        self.lastPing = str(datetime.now())
