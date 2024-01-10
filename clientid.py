from datetime import datetime
from datetime import timedelta


numIdentitiesInUse = 0
identitiesInUse = dict() #eventually, this should become a username/password combo, with the addition of guest passes


def getNewID(): #just generates a unique value. TODO: update to a hash
    global numIdentitiesInUse

    numIdentitiesInUse += 1
    identitiesInUse[numIdentitiesInUse] = None
    return numIdentitiesInUse

def isIDInUse(id: int):
    return (id in identitiesInUse)

def setIDtask(id: int, task: str):
    identitiesInUse[id] = (task, datetime.now())

def getIDtask(id: int):
    return identitiesInUse[id][0]

def getIDstart(id: int):
    return identitiesInUse[id][1]

def isIDInTask(id: int, time: timedelta, task: str) -> bool:
    '''Given an int `id`, how long it should take (timedelta `time`), and a str `task`, checks whether the given task is still being completed.'''
    if (isIDInUse(id) and (identitiesInUse[id] != None) and (getIDtask(id) == task)):
        oldtime = getIDstart(id)
        curtime = datetime.now()
        timePassed = curtime - oldtime

        return (time > timePassed)

    return False





