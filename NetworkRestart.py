import os
import time
#import SystemStatistic

i = 0
while True:
    i = i+1
    print("%s disable network %d times." % (time.asctime(time.localtime()),i))
    os.popen("devcon.exe disable *DEV_8168*")
    time.sleep(10)
    print("%s enble network %d times." % (time.asctime(time.localtime()),i))
    os.popen("devcon.exe enable *DEV_8168*")
    time.sleep(60)

    #os.popen("python SystemStatistic.py >> statis.log")
    

print("%s\nGood bye!", time.asctime(time.localtime()))
