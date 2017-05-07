import sys
import tstp
import requests
from mdb import zkillurl

def get_mail(logfile):
    """get killmail from zkillboard"""
    try:
        rawkillmail = requests.get(zkillurl)
        killmail = rawkillmail.json()
        return killmail
    except requests.exceptions.Timeout as err:
        print(tstp.now(), 'zkillboard - Timeout error - exiting')
        log = (tstp.now() + ' zkillboard - timeout error - ' + '\n')
        logfile.write(log)
        logfile.write(err)
        logfile.close()
        sys.exit()
    except requests.exceptions.TooManyRedirects as err:
        print(tstp.now(), 'zkillboard - Redirect error - exiting')
        log = (tstp.now() + ' zkillboard - redirect error - ' + '\n')
        logfile.write(log)
        logfile.write(err)
        logfile.close()
        sys.exit()
    except requests.exceptions.RequestException as err:
        print(tstp.now(), 'zkillboard - Request error - exiting')
        log = (tstp.now() + ' zkillboard - request error - ' +  '\n')
        logfile.write(log)
        logfile.write(err)
        logfile.close()
        sys.exit()
    except ValueError as err:
        print(tstp.now(), 'zkillboard - Value error - exiting')
        log = (tstp.now() + ' zkillboard - value errror - ' +  '\n')
        logfile.write(log)
        logfile.write(err)
        logfile.close()
        sys.exit()
