#!/usr/bin/env python
import fcntl, termios
import os
import sys
import json
XDHISTSIZE = int(os.environ.get('XDHISTSIZE') or 32)
HOME = os.path.expanduser('~')
XDHISTFILE = os.path.join(HOME,'.xcd_data')
HELP = '''\

XCD is a quick directory changer. In practice work,
we generally switch between several commonly used directories.
When you use XCD to switch directories, XCD will remember these directories
so that you can quickly switch to the history directory next time.

Usage examples:
xcd            : List the current stack and its indices.
xcd somepath   : Add "somepath" to your directory stack and cd there.
xcd -h         : Print this help.
'''

def addHistory(hist):
    'add a cd history to .xd_history'
    hl = []
    paths = getHistory()
    if hist in paths:
        paths.remove(hist)
    paths.insert(0,hist)
    if len(paths) > XDHISTSIZE:
        paths.pop()
    for p in paths:
        pd = {}
        pd['path'] = p
        hl.append(pd)
    return hl

def writeHistory(h):
    hl = addHistory(h)
    data = readDateFile()
    data['history'] = hl
    writedDateFile(data)

def addBookMark(name, b):
    'add a cd bookmark and return the bookmark dict'
    bl = []
    t = {}
    bm = getBookmark()
    if bm is not None:
        for b in bm:
            if b['name'] == name:
                continue
            else:
                bl.append(b)

    t['name'] = name
    t['path'] = b
    bl.append(t)
    return bl

def writeBookMark(name,b):
    'write bookmark to data file'
    bl = addBookMark(name,b)
    data = readDateFile()
    data['bookmark'] = bl
    writedDateFile(data)

def getHistory():
    'get history list '
    hl = []
    data = readDateFile()
    hist = data.get('history')
    if hist is None:
        return hl
    for h in hist:
        hl.append(h['path'])
    return hl

def getBookmark():
    'get bookmark list'
    data = readDateFile()
    bl = data.get('bookmark')
    return bl

def findBookMark(name):
    bm = getBookmark()
    for b in bm:
        if b['name'] == name:
            return b['path']
    return ''

def printBookMark():
    bm = getBookmark()
    for b in bm:
        print("{name}:{path}".format(name=b['name'],path=b['path']))


def printHistory(hist):
    'print the history to shell'
    if len(hist) == 0:
        print('have no cd history\n')
    else:
        for h in hist:
            # print('%s.' + h.replace('\n','') %(hist.index(h)))
            print("{num}.{path}".format(num=hist.index(h),path=h.replace('\n','')))

def readDateFile():
    'read the xd_history to json'
    data = {}
    try:
        with open(XDHISTFILE,'r') as fd:
            data = json.load(fd)
    except IOError:
        pass
    return data

def writedDateFile(data):
    'write the xd_history to json'
    try:
        with open(XDHISTFILE,'w') as fd:
             json.dump(data,fd)
    except IOError:
        pass

def hackCd(dest):
    # use of this means that it only works in an interactive session
    # (and if the user types while it runs they could insert characters between the characters in 'text'!)
    t = "cd " + dest + "\n"
    for c in t:
        fcntl.ioctl(1, termios.TIOCSTI, c)

def getFullPath():
    pwd = os.environ.get('PWD') or os.getcwd()
    return pwd

def parsePath(s):
    if  s[0] == '/':
        return s
    pwd = getFullPath() + '/' + s
    return pwd

def main():
    if len(sys.argv) <= 1:
        n = 0
        hist = getHistory()
        printHistory(hist)
        num = raw_input('input the num(0):')
        try:
            n = int(num)
        except ValueError:
            pass
        hackCd(hist[n])
        writeHistory(hist[n])
        return 0
    if sys.argv[1][0] == '-':
        if len(sys.argv) == 2:
            arg = sys.argv[1]
            if arg == '-h':
                print(HELP)
                return 1
            if arg == '-b':
                printBookMark()
        if len(sys.argv) == 4:
            arg = sys.argv[1]
            if arg == '-b':
                print('test bookmark')
                p = parsePath(sys.argv[3])
                if os.path.isdir(p):
                    p = os.path.normpath(p)
                    writeBookMark(sys.argv[2],p)
                else:
                    print('invalid path')

    else:
        p = parsePath(sys.argv[1])
        if os.path.isdir(p):
            p = os.path.normpath(p)
            hackCd(p)
            writeHistory(p)
        #maybe is a bookmark
        else:
            path = findBookMark(sys.argv[1])
            if path != '':
                hackCd(path)
            else:
                print('invalid path')

if __name__ == "__main__":
    main()
