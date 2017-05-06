import sys
import tstp
import requests
from mdb import zkillurl

def get_mail():
    """get killmail from zkillboard"""
    try:
        rawkillmail = requests.get(zkillurl)
        killmail = rawkillmail.json()
        return killmail
    except requests.exceptions.Timeout as err:
        print(tstp.now(), 'zkillboard - Timeout error - exiting')
        print(err)
        sys.exit()
    except requests.exceptions.TooManyRedirects as err:
        print(tstp.now(), 'zkillboard - Redirect error - exiting')
        print(err)
        sys.exit()
    except requests.exceptions.RequestException as err:
        print(tstp.now(), 'zkillboard - Request error - exiting')
        print(err)
        sys.exit()
    except ValueError as err:
        print(tstp.now(), 'zkillboard - Value error - exiting')
        print(err)
        sys.exit()
