"""process killmail for insertion to mongodb"""

import calendar
import time
import hashlib
import getflagtype
import getammoflag

def strtime2unix(strtime):
    """convert zkill time string to unix epoch time"""
    utime = calendar.timegm(time.strptime(strtime, '%Y.%m.%d %H:%M:%S'))
    return utime

def killmail(mongohandle, jsonmail):
    """process killmail to package with selected info
    create a hash of fitted non-ammo items for comparison"""
    fpmail = {}
    fpmail['kill_id'] = jsonmail['package']['killID']
    fpmail['kill_time'] = jsonmail['package']['killmail']['killTime']
    fpmail['unix_kill_time'] = strtime2unix(jsonmail['package']['killmail']['killTime'])
    fpmail['solar_system_id'] = jsonmail['package']['killmail']['solarSystem']['id']

    if 'name' in jsonmail['package']['killmail']['solarSystem']:
        fpmail['solar_system_name'] = jsonmail['package']['killmail']['solarSystem']['name']
    else:
        fpmail['solar_system_name'] = None
    fpmail['corporation_id'] = jsonmail['package']['killmail']['victim']['corporation']['id']
    if 'name' in jsonmail['package']['killmail']['victim']['corporation']:
        fpmail['corporation_name'] = jsonmail['package']['killmail']['victim']['corporation']['name']
    else:
        fpmail['corporation_name'] = None
    if 'alliance' in jsonmail['package']['killmail']['victim']:
        fpmail['alliance_id'] = jsonmail['package']['killmail']['victim']['alliance']['id']
        if 'name' in jsonmail['package']['killmail']['victim']['alliance']:
            fpmail['alliance_name'] = jsonmail['package']['killmail']['victim']['alliance']['name']
        else:
            fpmail['alliance_name'] = None
    else:
        fpmail['alliance_id'] = None
        fpmail['alliance_name'] = None

    fpmail['ship'] = {}
    fpmail['ship']['type_id'] = jsonmail['package']['killmail']['victim']['shipType']['id']
    if 'name' in jsonmail['package']['killmail']['victim']['shipType']:
        fpmail['ship']['name'] = jsonmail['package']['killmail']['victim']['shipType']['name']
    else:
        fpmail['ship']['name'] = None

    slotarray = []
    for item in jsonmail['package']['killmail']['victim']['items']:
        slotarray.append(item['flag'])
    itemarray = []
    fitarray = []
    for item in jsonmail['package']['killmail']['victim']['items']:
        imail = {}
        imail['type_id'] = item['itemType']['id']
        if 'name' in item['itemType']:
            imail['name'] = item['itemType']['name']
        else:
            imail['name'] = None
        isammo = getammoflag.now(mongohandle, item['itemType']['id'])
        if isammo == 1:
            imail['is_ammo'] = True
        else:
            imail['is_ammo'] = False
        imail['slot'] = item['flag']
        imail['is_cargo'] = False
        imail['is_attached'] = False
        imail['is_drone_bay'] = False
        imail['is_implant'] = False
        imail['is_unk_flag'] = False

        flagtype = getflagtype.now(item['flag'])

        if flagtype == 1:
            imail['is_cargo'] = True
        elif flagtype == 2:
            imail['is_attached'] = True
        elif flagtype == 3:
            imail['is_drone_bay'] = True
        elif flagtype == 4:
            imail['is_implant'] = True
        else:
            imail['is_unk_flag'] = True

        if 'quantityDestroyed' in item:
            imail['quantity'] = item['quantityDestroyed']
            imail['dropped'] = False
        elif 'quantityDropped' in item:
            imail['quantity'] = item['quantityDropped']
            imail['dropped'] = True
        else:
            imail['quantity'] = None
            imail['dropped'] = False

        slotcounter = 0
        for slot in slotarray:
            if slot is item['flag']:
                slotcounter += 1
        if slotcounter > 1 and flagtype == 2:
            imail['shared_slot'] = True
        else:
            imail['shared_slot'] = False
        itemarray.append(imail)

        if imail['is_attached'] is True and imail['is_ammo'] is False:
            fitarray.append(imail['type_id'])

    fpmail['items'] = itemarray
    fitarray.sort()
    fitarray.append(fpmail['ship']['type_id'])
    fithash = hashlib.md5(str(fitarray).encode('utf-8')).hexdigest()
    fpmail['fithash'] = fithash
    return fpmail
