#!/usr/bin/env python
import pipes
import fcntl, termios
import os
import sys
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
    return hist

def printHistory(hist):
    'print the history to shell'
    if len(hist) == 0:
        print('have no cd history\n')
    else:
        for h in hist:
            # print('%s.' + h.replace('\n','') %(hist.index(h)))
            print("{num}.{path}".format(num=hist.index(h),path=h.replace('\n','')))

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
    if h in paths:
        paths.remove(h)
    paths.insert(0,h)
    if len(paths) > XDHISTSIZE:
        paths.pop()
    return paths

def hackCd(dest):
    # use of this means that it only works in an interactive session
    # (and if the user types while it runs they could insert characters between the characters in 'text'!)
    t = "cd " + dest
    for c in t:
        fcntl.ioctl(1, termios.TIOCSTI, c)

def getFullPath():
    pwd = os.environ.get('PWD') or os.getcwd()
    return pwd

def addPath(path, hist):
    hist.insert(0,path)
    try:
        with open(XDHISTFILE,'rw') as fd:
            old = fd.readlines()
            print(old)
    except IOError:
        pass


def parsePath(s):
    if  s[0] == '/':
        return s
    pwd = getFullPath() + '/' + s
    return pwd

def main():
    tty = open('/dev/tty','w')
    if len(sys.argv) <= 1:
        hist = readHistory()
        printHistory(hist)
        num = raw_input('input the num(0):')
        hackCd(hist[int(num)])
    else:
        p = parsePath(sys.argv[1])
        print(p)
        print(os.path.isdir(p))
        if os.path.isdir(p):
            p = os.path.normpath(p)
        print(p)

if __name__ == "__main__":
    main()