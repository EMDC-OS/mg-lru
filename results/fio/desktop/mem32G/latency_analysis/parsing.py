#!/usr/bin/python3
import re

dist = ["lru", "mglru"]
thread = ["16", "32"]
mem1 = ["2G", "3G", "4G", "5G"]
mem2 = ["1G", "2G", "3G"]
mem = [mem1, mem2]
pattern = ["random", "normal:40", "zipf:0.8"]
names = ["hitratio"]
# "fio", hitratio", "kswapd", "vmstat"

path="/home/jongseok/mglru/eval_tmp/"

vmstat_name = []
kq = []
vq = []

def results(file):
    # print(file)
    try:
        with open(file, "r") as f:
            for l in f:
                l = l.rstrip('\n')
                # print(l)

                if re.search('bw', l) and re.search('avg', l):
                    l = l.split('=')

                    # print(l)
                    bw=l[4].split(',')[0]
                    if "KiB" in l[0]:
                        bw = round(float(l[4].split(',')[0])/1024,2)
                    print(str(bw), end=" ")

                elif re.search("99\.00th", l):
                    l = l.split('=')

                    print(l[1].split('[')[1].split(']')[0].lstrip(' '), end=" ")
    except: 
        print("xxx", end=" ")
        print("xxx", end=" ")
    return
    

def hitratio(file):
    # print(file)
    count = 0
    percent = 0
    try:
        with open(file, "r") as f:
            for l in f:
                l = l.rstrip('\n')
                # print(l)

                if re.search('\%', l):
                    percent+=float(l.split()[3].rstrip("%"))
                    count += 1
        
        print(round(percent/count, 2), end=" ")
    except: 
        print("xxx", end=" ")

    return



def kswapd(name, d, t, mm, p, i):
    start_file = name +"_start_" + d + "_" + t +"t_" + mm + "_" + p + "_" + str(i)
    stop_file = name +"_stop_" + d + "_" + t +"t_" + mm + "_" + p + "_" + str(i)
    startv = []
    stopv = []
    global kq

    try:
        with open(start_file, "r") as f:
            lines = f.readlines()[2:6]
            for l in lines:
                startv.append(round(float(l.rstrip('\n').split()[2]),2))

        with open(stop_file, "r") as f:
            lines = f.readlines()[2:6]
            stopv = []
            for l in lines:
                stopv.append(round(float(l.rstrip('\n').split()[2]),2))

        if len(kq) == 0:
            for i in range(0, 4):
                kq.append(startv[i])
                kq.append(stopv[i])
                kq.append(round(stopv[i] - startv[i],2))
        else:
            for i in range(0, 4):
                print(kq[i*3], end=" ")
                print(kq[i*3+1], end=" ")
                print(kq[i*3+2], end=" ")
                print(startv[i], end=" ")
                print(stopv[i], end=" ")
                print(round(stopv[i] - startv[i],2))
            kq = []

    except: 
        print("xxx xxx xxx xxx xxx xxx")
        print("xxx xxx xxx xxx xxx xxx")


def vmstat(name, d, t, mm, p, i):
    start_file = name +"_start_" + d + "_" + t +"t_" + mm + "_" + p + "_" + str(i)
    stop_file = name +"_stop_" + d + "_" + t +"t_" + mm + "_" + p + "_" + str(i)
    startv = []
    stopv = []
    global vq


    try:
        with open(start_file, "r") as f:
            name_len = len(vmstat_name)
            for l in f:
                startv.append(int(l.rstrip('\n').split()[1]))
                if name_len < 168:
                    vmstat_name.append(l.rstrip('\n').split()[0])

        with open(stop_file, "r") as f:
            for l in f:
                stopv.append(int(l.rstrip('\n').split()[1]))

        vlen = len(startv)
        if len(vq) == 0:
            for i in range(0, vlen):
                vq.append(startv[i])
                vq.append(stopv[i])
                vq.append(stopv[i] - startv[i])
        else:
            print(name + "_" + t +"t_" + mm + "_" + p + "_" + str(i))
            for i in range(0, vlen):
                print(vmstat_name[i], end=" ")
                print(vq[i*3], end=" ")
                print(vq[i*3+1], end=" ")
                print(vq[i*3+2], end=" ")
                print(startv[i], end=" ")
                print(stopv[i], end=" ")
                print(stopv[i] - startv[i])
            vq = []
        #
    except: 
        print("xxx xxx xxx xxx xxx xxx")
        print("xxx xxx xxx xxx xxx xxx")


fn = {0: results, 1: hitratio, 2: kswapd, 3: vmstat}

def forp(name, case):
    print("# access \\ dist,thread")
    print("# 3 iters")
    print("# memory size\n")
    my_print = fn[case]
    for m in mem:
        for mm in m:
            for i in range(1,4):
                for p in pattern:
                    for t in thread:
                        for d in dist:
                            if case < 2:
                                fname = name +"_" + d + "_" + t +"t_" + mm + "_" + p + "_" + str(i)
                                my_print(fname)
                                # results(fname)
                                # hitratio(fname)
                            else:
                                my_print(name, d, t, mm, p, i)
                                #kswapd(name, d, t, mm, p, i)
                                #vmstat(name, d, t, mm, p, i)
                            print("")
                    print("")
                print("")

if __name__ == "__main__":
    i = 0
    # for n in names:
    forp("vmstat", 3)
        # i += 1
