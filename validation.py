import re

def validBoardName(boardName):
    reg = re.compile('^[\w\s-]{1,50}$')
    if reg.match(boardName):
        return True
    return False

def validLabel(label):
    reg = re.compile('^[\w\s-]{1,20}$')
    if reg.match(label):
        return True
    return False