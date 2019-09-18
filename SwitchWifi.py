import os
import time
#import SystemStatistic

i = 0
while True:
    i = i+1
    print("%s use wifi 'UCLogic' network %d times." % (time.asctime(time.localtime()),i))
    os.popen('netsh wlan connect name="UCLogic"')
    time.sleep(3)
    print("%s use wifi 'UCLogic2' network %d times." % (time.asctime(time.localtime()),i))
    os.popen('netsh wlan connect name="UCLogic2"')
    time.sleep(3)

    #os.popen("python SystemStatistic.py >> statis.log")
    

print("%s\nGood bye!", time.asctime(time.localtime()))
