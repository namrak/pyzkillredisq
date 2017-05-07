from pymongo import MongoClient, errors
import tstp
from mdb import creds

def connect():
    """connect to mongodb"""
    try:
        client = MongoClient(creds['ip'], int(creds['port']))
        db = client.fpLoss
        db.authenticate(creds['un'], creds['pw'])
        return db
    except errors.ServerSelectionTimeoutError as err:
        print(time.strftime('%m/%d %H:%M:%S'), 'Timeout Error - Aborting')
        timeoutlog = (tstp.now() + ' Log - Server timeout - ' + str(icount) + '\n')
        logfile.write(timeoutlog)
        logfile.write(err)
        logfile.close()
        sys.exit()
    except errors.ConnectionFailure as err:
        print(time.strftime('%m/%d %H:%M:%S'), 'Connection Failure - Aborting')
        failconnlog = (tstp.now() + ' Log - Failed connection - ' + str(icount) + '\n')
        logfile.write(failconnlog)
        logfile.write(err)
        logfile.close()
        sys.exit()

def insert2mongo(mongohandle, killmail):
    """insert formatted killmail to mongodb"""
    try:
        allkills = mongohandle.allkills
        allkills.insert_one(killmail)
        return 0
    except errors.ServerSelectionTimeoutError as err:
        print(time.strftime('%m/%d %H:%M:%S'), 'Timeout Error - Aborting')
        timeoutlog = (tstp.now() + ' Log - Server timeout - ' + str(icount) + '\n')
        logfile.write(timeoutlog)
        logfile.write(err)
        logfile.close()
        sys.exit()
    except errors.ConnectionFailure as err:
        print(time.strftime('%m/%d %H:%M:%S'), 'Connection Failure - Aborting')
        failconnlog = (tstp.now() + ' Log - Failed connection - ' + str(icount) + '\n')
        logfile.write(failconnlog)
        logfile.write(err)
        logfile.close()
        sys.exit()

def get_groupid_from_typeid(mongohandle, typeid):
    """get item name from typeid db"""
    try:
        typeids = mongohandle.typeIDs
        cursor = typeids.find_one({"typeID": typeid}, {"groupID": 1})
        if cursor is not None:
            return cursor['groupID']
        else:
            print(tstp.now() + '!!ERROR!! Group ID not found for Type ID: ' + str(typeid) + '\n')
            return 0
    except errors.ServerSelectionTimeoutError as err:
        print(time.strftime('%m/%d %H:%M:%S'), 'Timeout Error - Aborting')
        timeoutlog = (tstp.now() + ' Log - Server timeout - ' + str(icount) + '\n')
        logfile.write(timeoutlog)
        logfile.write(err)
        logfile.close()
        sys.exit()
    except errors.ConnectionFailure as err:
        print(time.strftime('%m/%d %H:%M:%S'), 'Connection Failure - Aborting')
        failconnlog = (tstp.now() + ' Log - Failed connection - ' + str(icount) + '\n')
        logfile.write(failconnlog)
        logfile.write(err)
        logfile.close()
        sys.exit()