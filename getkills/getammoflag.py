import json
import sys
import mongoconn

def now(mongohandle, typeid):
    """return 1 if typeid is in ammo group"""
    ammogroups = {
        83: 1,
        85: 1,
        86: 1,
        87: 1,
        88: 1,
        89: 1,
        90: 1,
        372: 1,
        373: 1,
        374: 1,
        375: 1,
        376: 1,
        377: 1,
        384: 1,
        385: 1,
        386: 1,
        387: 1,
        394: 1,
        395: 1,
        396: 1,
        479: 1,
        482: 1,
        500: 1,
        548: 1,
        648: 1,
        653: 1,
        654: 1,
        655: 1,
        656: 1,
        657: 1,
        772: 1,
        864: 1,
        907: 1,
        908: 1,
        909: 1,
        910: 1,
        911: 1,
        916: 1,
        1769: 1,
        1771: 1,
        1772: 1,
        1773: 1,
        1774: 1,
    }

    groupid = mongoconn.get_groupid_from_typeid(mongohandle, typeid)
    return ammogroups.get(groupid, 0)
    

if __name__ == "__main__":
    testhandle = mongoconn.connect()
    testarg = now(testhandle, int(sys.argv[1]))
    print(testarg)
