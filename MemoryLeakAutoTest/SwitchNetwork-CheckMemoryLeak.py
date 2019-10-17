#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/17 17:06
# @Author  : Huang Yu
# @File    : test_telnet_login_logout.py
# @Software: PyCharm
import telnetlib
import time
import os
import subprocess

def login(telnet_client):
    telnet_client.write(b'login\r\n')


def logout(telnet_client):
    telnet_client.write(b'logout\r\n')

# 64 Bit
UMHD_EXE_PATH = "."
#UMHD_EXE_PATH = "D:\\Program Files (x86)\\Debugging Tools for Windows (x86)"
UMHD_EXE = "umdh.exe"
DUMP_PATH = "G:\\MemLeakRelust_{0}\\".format(time.strftime("%Y%m%d%H%M%S+0000", time.gmtime()))
TEST_PROCESS = "MockClient.exe"
#TEST_PROCESS_SYMBOL_PATH = "E:\\Project\\ComponentDevTest\\PanGu_Debug\\PanGu\\src\\UC-Logic\\win\\bin\\Debug"
#TEST_PROCESS_SYMBOL_PATH = "E:\\Project\\ComponentDevTest\\PanGu_Debug\\PanGu\\src\\UC-Logic\\win\\bin\\Release"
TEST_PROCESS_SYMBOL_PATH = "C:\\Project\\PanGu\\src\\UC-Logic\\build-Windows-Test\\bin"
CACHE_SRV_SYMBOL_PATH = "srv*C:\\mysymbol*https://msdl.microsoft.com/download/symbols"
#os.chdir(UMHD_EXE_PATH)
try:
    os.mkdir(DUMP_PATH)
except Exception as e:
    print(e)

os.popen("set _NT_SYMBOL_PATH={0};{1}".format(TEST_PROCESS_SYMBOL_PATH, CACHE_SRV_SYMBOL_PATH))

def run_exe(path, exe_name):
    exe_path = "{0}\\{1}".format(path, exe_name)
    print(exe_path)
    subprocess.call(exe_path)

def dump(processname, dump_index):
    os.popen("{0} -pn:{1} -f:{3}{1}_{2}".format(UMHD_EXE,processname, dump_index, DUMP_PATH))

def cmp_dump(processname, dump_index1, dump_index2):
    os.popen("{0} -d {4}{1}_{2} {4}{1}_{3} -f:{4}DumpDiff{2}.log".format(UMHD_EXE, processname, dump_index1, dump_index2, DUMP_PATH))


if __name__ == '__main__':
    #run_exe(TEST_PROCESS_SYMBOL_PATH, TEST_PROCESS)
    time.sleep(5)

    client = telnetlib.Telnet("10.85.1.52", 60001)
    client.set_debuglevel(4)

    print(os.getcwd())
    # i=0
    # while True:
    #     login(client)
    #     time.sleep(20)
    #     logout(client)
    #     time.sleep(10)
        

        #dump(TEST_PROCESS, i)
        #if i>0:
        #    cmp_dump(TEST_PROCESS, i-1, i)

        #i= i+1
    i = 0
    while True:
        print("%s enble network %d times." % (time.asctime(time.localtime()),i))
        os.popen("devcon.exe enable *DEV_8168*")
        time.sleep(20)

        print("%s disable network %d times." % (time.asctime(time.localtime()),i))
        os.popen("devcon.exe disable *DEV_8168*")
        time.sleep(20)

        dump(TEST_PROCESS, i)
        if i>0:
           cmp_dump(TEST_PROCESS, i-1, i)

        i= i+1