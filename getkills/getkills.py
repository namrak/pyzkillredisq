"""main module to get killmails and process them"""

import time
import sys
import parse
import zkill
import tstp
import mongoconn

def process_zkill_redisq():
    """start download and processing of zkillboard redisq queue"""
    mongohandle = mongoconn.connect()
    print(tstp.now(), 'Main - Connecting to MongoDB - waiting 1 second')
    logfile = open('fpLog.txt', 'a+')
    startlog = (tstp.now() + ' Log - Begin processing of killmails\n')
    logfile.write(startlog)
    time.sleep(1)
    icount = 0
    while True:
        kmail = zkill.get_mail(logfile)
        if 'package' in kmail:
            if kmail['package'] is None:
                print(tstp.now(), 'Main - Empty Killmail - exiting')
                emptylog = (tstp.now() +
                            ' Log - Done - Processed ' +
                            str(icount) +
                            ' killmails\n')
                logfile.write(emptylog)
                logfile.close()
                sys.exit()
            else:
                icount += 1
                if 'name' in kmail['package']['killmail']['victim']['corporation']:
                    corp = kmail['package']['killmail']['victim']['corporation']['name']
                else:
                    corp = kmail['package']['killmail']['victim']['corporation']['id']
                if 'name' in kmail['package']['killmail']['victim']['shipType']:
                    ship = kmail['package']['killmail']['victim']['shipType']['name']
                else:
                    ship = kmail['package']['killmail']['victim']['shipType']['id']
                print(tstp.now(), 'Main -', icount, 'Info:', corp, ':', ship)
                mail2insert = parse.killmail(mongohandle, logfile, kmail)
                mongoconn.insert2mongo(mongohandle, logfile, mail2insert)
        else:
            print(time.strftime('%m/%d %H:%M:%S'), 'Main - Error: No package - exiting')
            errorlog = (tstp.now() + ' Log - No package - ' + str(icount) + '\n')
            logfile.write(errorlog)
            logfile.close()
            sys.exit()

if __name__ == "__main__":
    process_zkill_redisq()
