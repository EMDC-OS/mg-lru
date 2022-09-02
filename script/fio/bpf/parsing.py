#!/usr/bin/python3
import re
if __name__ == "__main__":
	tags = ["NODE", "LRUVEC", "TRY_MAX", "ISOL_FOL", 
		"SHR_LIST", "ACT_LIST", "INACT_LIST"]
	dod = {}
	zeros = {}
	maxs = []

	for t in tags:
		dod[t] = {}

	with open("./trace/lru_elap_time_test_ver", "r") as f:
		for l in f:
			l = l.rstrip('\n')
			s = re.split('\'|:| ', l)
			tag = s[1]
			id = s[2]
			v1 = s[4]
			v2 = s[5]
			if id not in dod[tag]:
				dod[tag][id] = (0, 0, 0)
			if tag == "LRUVEC" and v2 == "0":
				if id not in zeros:
					zeros[id] = 0
				zeros[id] = zeros[id] + 1
			if tag == "NODE":
				if id != "kswapd0":
				#if id not in maxs:
				#	maxs[id] = []
					maxs.append(int(v1))



			cur = dod[tag][id]
			dod[tag][id] = (cur[0]+1, cur[1]+int(v1), cur[2]+int(v2))
			#print(cur)


			#print(tag, id, v1, v2)
	for k, v in dod.items():
		print(k)
		for k2, v2 in v.items():
			print(k2, v2)

	for k, v in zeros.items():
		print(k, v)

	maxs.sort(reverse=True)
	lenth = len(maxs)
	idx = int(lenth / 100)
	print(lenth, idx)
	print(maxs[0])
	print(maxs[idx])

