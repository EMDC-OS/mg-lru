#!/usr/bin/python3
import re

dist = ["lru", "mglru"]
thread = ["16", "32"]
mem1 = ["2G", "3G", "4G", "5G"]
mem2 = ["1G", "2G", "3G"]
mem = [mem1, mem2]
pattern = ["random", "normal:40", "zipf:0.8"]
names = ["fio", "hitratio", "kswapd", "vmstat"]
# "fio", hitratio", "kswapd", "vmstat"
path="/home/jongseok/mglru/eval_tmp/"

kq = []
vq = []
vmstat_name = []
final_results = {"results" : [], "hit": [], "kswapd": [], "vmstat": []}
final_name = {"kind": [], "results" : [], "hit": [], "kswapd": [], "vmstat": []}

def results(file):
    # print(file)
    global final_results
    global final_name
    cur_results = []
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
                    # print(str(bw), end=" ")
                    cur_results.append(bw)

                elif re.search("99\.00th", l):
                    l = l.split('=')

                    # print(l[1].split('[')[1].split(']')[0].lstrip(' '), end=" ")
                    cur_results.append(l[1].split('[')[1].split(']')[0].lstrip(' '))

    except: 
        # print("xxx", end=" ")
        # print("xxx", end=" ")
        cur_results.append("xxx xxx")
    final_results.get("results").append(cur_results)
    return
    

def hitratio(file):
    # print(file)
    count = 0
    percent = 0
    global final_results
    global final_name
    cur_results = []
    try:
        with open(file, "r") as f:
            for l in f:
                l = l.rstrip('\n')
                # print(l)

                if re.search('\%', l):
                    percent+=float(l.split()[3].rstrip("%"))
                    count += 1
        
        # print(round(percent/count, 2), end=" ")
        cur_results.append(round(percent/count, 2))
    except: 
        # print("xxx", end=" ")
        cur_results.append("xxx")
    final_results.get("hit").append(cur_results)

    return



def kswapd(name, d, t, mm, p, i):
    start_file = name +"_start_" + d + "_" + t +"t_" + mm + "_" + p + "_" + str(i)
    stop_file = name +"_stop_" + d + "_" + t +"t_" + mm + "_" + p + "_" + str(i)
    startv = []
    stopv = []
    global final_results
    global final_name
    cur_results = []

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

        for i in range(0, 4):
            cur_results.append(round(stopv[i] - startv[i],2))

    except: 
        # print("xxx xxx xxx xxx xxx xxx")
        cur_results.append("xxx xxx xxx xxx xxx xxx xxx xxx")
    final_results.get("kswapd").append(cur_results)


def vmstat(name, d, t, mm, p, i):
    start_file = name +"_start_" + d + "_" + t +"t_" + mm + "_" + p + "_" + str(i)
    stop_file = name +"_stop_" + d + "_" + t +"t_" + mm + "_" + p + "_" + str(i)
    startv = []
    stopv = []
    global final_results
    global final_name
    cur_results = []

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
        for i in range(0, vlen):
            cur_results.append(stopv[i] - startv[i])
    except: 
        # print("xxx xxx xxx xxx xxx xxx")
        # print("xxx xxx xxx xxx xxx xxx")
        cur_results.append("xxx xxx xxx xxx xxx xxx xxx xxx")
    final_results.get("vmstat").append(cur_results)


fn = {0: results, 1: hitratio, 2: kswapd, 3: vmstat}

def forp(name, case):
    print("# access \\ dist,thread")
    print("# 3 iters")
    print("# memory size\n")

    global final_name
    my_print = fn[case]
    for m in mem:
        for mm in m:
            for i in range(1,4):
                for p in pattern:
                    for t in thread:
                        for d in dist:
                            fname = name +"_" + d + "_" + t +"t_" + mm + "_" + p + "_" + str(i)
                            if case == 0:
                                final_name.get("kind").append(fname)
                            if case < 2:
                                my_print(fname)
                                # results(fname)
                                # hitratio(fname)
                            else:
                                my_print(name, d, t, mm, p, i)
                                #kswapd(name, d, t, mm, p, i)
                                #vmstat(name, d, t, mm, p, i)
                            # print("")
                    # print("")
                # print("")

if __name__ == "__main__":
    i = 0
    for n in names:
        forp(n, i)
        i+=1


    klen = len(final_name.get("kind"))
    for k in range(0, klen):
        print(final_name.get("kind")[k], end=" ")
        # re = final_results.get("results")[k]
        # hit = final_results.get("hit")[k]
        # ks = final_results.get("kswapd")[k]
        # vm = final_results.get("vmstat")[k]
        for _, v in final_results.items():
            cur_list = v[k]
            for c in cur_list:
                print(c, end=" ")
        print("")


