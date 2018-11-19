#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import time
import os
import win32com.client
import re


def check_process_exist_by_name(process_name):
    try:
        WMI = win32com.client.GetObject('winmgmts:')
        processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
    except Exception as e:
        print
        process_name + "error : ", e;
    if len(processCodeCov) > 0:
        print
        process_name + " exist";
        return 1
    else:
        print
        process_name + " is not exist";
        return 0


dmp_dir = 'C:\\Project\\PanGu\\build\\log'


def find_dmps(dmp_dir):
    dmps = []
    for f in os.listdir(dmp_dir):
            dmp_full_path = dmp_dir + '\\' + f
            if re.search('\.dmp$', f) and os.path.isfile(dmp_full_path):
                    print('find dmp:' + f)
                    dmps.append(dmp_full_path)
    return dmps


def check_dmp():
    dmps = find_dmps(dmp_dir)
    return len(dmps) > 0


def clear_dmp():
    dmps = find_dmps(dmp_dir)
    for dmp in dmps:
        os.remove(dmp)


#process1 = 'E:\\ProjectSrc\\PanGu_upgrade_baselib\\build\\Debug\\Yealink UME Desktop.exe'
process1 = 'C:\\Project\\PanGu\\build\\Debug\\Yealink UME Desktop.exe'
process_name1 = 'Yealink UME Desktop.exe'
#process2 = 'E:\\ProjectSrc\\PanGu_upgrade_baselib\\build\\Debug\\MockClient.exe'
#process_name2 = 'MockClient.exe'

if __name__ == '__main__':
    print("clear dmp")
    clear_dmp()

    # 不输出内容到控制台
    devNull = os.open(os.devnull, os.O_WRONLY)

    i = 0
    print("begin loop")
    for i in range(100):
        print('run %d' % i)
        proc = subprocess.Popen(process1, shell=True, stdout=devNull)
        # print('subprocess Popen ret:' + ret)
        # os.popen('E:\\ProjectSrc\\PanGu_upgrade_baselib\\build\\Debug\\Yealink UME Desktop.exe')
        time.sleep(10)
        # p = os.popen('tasklist /FI "IMAGENAME eq %s"' % "Yealink UME Desktop.exe")

        if not check_process_exist_by_name(process_name1):
            print('no process ')
            break
        if check_dmp():
            print('generated dmp')
            break
        print('kill')
        kill_str = 'taskkill /F /IM "' + process_name1 + '"'
        subprocess.run(kill_str)
        #proc.kill()
        time.sleep(2)
    print('script over:%d' % i)
