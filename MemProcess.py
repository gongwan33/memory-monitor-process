from subprocess import Popen, PIPE
from distutils import spawn
import os
import time
import sys
import platform
import time

target_name = 'python pose2d_sample.py'

def getMemProcess():
    cmd = "ps"

    try:
        p = Popen([cmd, '-o', 'pid,%mem,command', 'a'], stdout=PIPE)
        stdout, stderror = p.communicate()
    except:
        return []
    output = stdout.decode('UTF-8')

    Mems = {}
    lines = output.split(os.linesep)
    process_start_line = -1
    for idx, line in enumerate(lines):
        if line is not None and len(line) > 0:
            if line.find('PID') != -1 and line.find('COMMAND') != -1 and line.find('MEM') != -1:
                process_start_line = idx + 1
                break

    if process_start_line != -1:
        for line in lines[process_start_line : ]:
            parts = line.split()
            if len(parts) >= 3:
                mem_use = parts[1]
                command = ' '.join(parts[2:])
                Mems[command] = float(mem_use)

    return Mems

max_mem = 0
sep_flag = True

while True:
    mems = getMemProcess()
    found_flag = False
    for mem in mems:
        if mem.find(target_name) != -1:
            found_flag = True
            if mems[mem] > max_mem:
                print(mems[mem])
                max_mem = mems[mem]

    if found_flag == True:
        sep_flag = False
    else:
        max_mem = 0
        if sep_flag == False:
            print("------------------------------------------")
            sep_flag = True

    time.sleep(0.5)
