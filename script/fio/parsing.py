#!/usr/bin/python3
import re

dist = ["lru", "mglru"]
thread = ["16", "32"]
mem1 = ["2G", "3G", "4G", "5G"]
mem2 = ["1G", "2G", "3G"]
mem = [mem1, mem2]
pattern = ["random", "normal:40", "zipf:0.8"]
names = ["fio"]
#"hitratio", "kswapd", "vmstat"

path="/home/jongseok/mglru/eval_tmp/"

def forp(name, case):
    print("# access \\ dist,thread")
    print("# 3 iters")
    print("# memory size\n")
    for m in mem:
        for mm in m:
            for i in range(1,4):
                for p in pattern:
                    for t in thread:
                        for d in dist:
                            if case < 2:
                                fname = name +"_" + d + "_" + t +"t_" + mm + "_" + p + "_" + str(i)
                                results(fname)
                                #hitratio(fname)
                            else:
                                continue
                                # print("later")
                                #kswapd(name, d, t, mm, p, i)
                                #vmstat(name, d, t, mm, p, i)
                    print("")
                print("")

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
    

def hitratio(fname):
    print("hit", 1)


def kswapd(name, d, t, mm, p, i):
    print("kswapd", 2)


def vmstat(name, d, t, mm, p, i):
    print("vmstat", 3)


if __name__ == "__main__":
    i = 0
    for n in names:
        forp(n, i)
        i += 1
