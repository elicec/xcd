#!/usr/bin/env python
import pipes
import fcntl, termios
import os
XDHISTSIZE = int(os.environ.get('XDHISTSIZE') or 32)
HOME = os.path.expanduser('~')
XDHISTFILE = os.path.join(HOME,'.xd_history')
def test():
    'Main func entry'
    # his = commands.getoutput('date')
    # print(his)
    # (status, output) = commands.getstatusoutput('cd /home/')
    # his1 = os.system('cd /home')
    # print(status,output)
    # subprocess.call("cd /home",shell=True)
    os.chdir('/home')
def addHistory(h):
    'add a cd history to .xd_history'
    try:
        with open(XDHISTFILE,'a') as fd:
            fd.write(h+'\n')
    except IOError:
        pass

def readHistory():
    'read the xd_history'
    try:
        with open(XDHISTFILE,'r') as fd:
            hist = fd.readlines()
    except IOError:
        pass
    print(hist)
    return hist

def updateHistory(h):
    'update the xd_history'
    paths = updateList(h)
    try:
        with open(XDHISTFILE,'w') as fd:
            fd.writelines(paths)
    except IOError:
        print('File Error!')

def updateList(h):
    paths = readHistory()
    paths.insert(0,h)
    if len(paths) > XDHISTSIZE:
        paths.pop()
    return paths

def hackCd(dest):
    # use of this means that it only works in an interactive session
    # (and if the user types while it runs they could insert characters between the characters in 'text'!)
    s = pipes.quote(dest)
    t = "cd" + s + "\n"
    for c in t:
        fcntl.ioctl(1, termios.TIOCSTI, c)

def getFullPath():
    os.environ.get('PWD')
    pwd = os.environ.get('PWD') or os.getcwd()
    print(pwd)

def addPath(path, hist):
    hist.insert(0,path)
    try:
        with open(XDHISTFILE,'rw') as fd:
            old = fd.readlines()
            print(old)
    except IOError:
        pass


def removeOld():
    'remove the old path'

if __name__ == "__main__":
    test()
    getFullPath()
    print(os.getcwd())

    addHistory('first')
    addHistory('second')
    updateHistory('zero')
    # readHistory()
