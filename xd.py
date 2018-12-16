#!/usr/bin/env python
import os,sys
import commands
XDHISTSIZE = int(os.environ.get('XDHISTSIZE') or 32)
HOME = os.path.expanduser('~')
XDHISTFILE = os.path.join(HOME,'.xd_history')
def test():
    'Main func entry'
    his = commands.getoutput('date')
    print(his)
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

if __name__ == "__main__":
    # test()
    # addHistory('first')
    # addHistory('second')
    readHistory()