from pymongo import MongoClient
from mdb import creds

def connect():
    """connect to mongodb"""
    try:
        client = MongoClient(creds['ip'], int(creds['port']))
        db = client.fpLoss
        db.authenticate(creds['un'], creds['pw'])
        return db
    except pymongo.errors.ServerSelectionTimeoutError:
        print(time.strftime('%m/%d %H:%M:%S'), 'Timeout Error - Aborting')
        timeoutlog = (tstp.now() + ' Log - Server timeout - ' + str(icount) + '\n')
        logfile.write(timeoutlog)
        logfile.close()
        sys.exit()
    except pymongo.errors.ConnectionFailure:
        print(time.strftime('%m/%d %H:%M:%S'), 'Connection Failure - Aborting')
        failconnlog = (tstp.now() + ' Log - Failed connection - ' + str(icount) + '\n')
        logfile.write(failconnlog)
        logfile.close()
        sys.exit()

def insert2mongo(mongohandle, killmail):
    """insert formatted killmail to mongodb"""
    allkills = mongohandle.allkills
    allkills.insert_one(killmail)
    return 0

def get_groupid_from_typeid(mongohandle, typeid):
    """get item name from typeid db"""
    typeids = mongohandle.typeIDs
    cursor = typeids.find_one({"typeID": typeid}, {"groupID": 1})
    groupid = cursor['groupID']
    return groupid