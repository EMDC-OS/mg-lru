#!/bin/bash

modprobe zram
echo 6G > /sys/block/zram0/disksize
mkswap /dev/zram0
swapon -p 100 /dev/zram0

cat /proc/swaps

mkdir /var/run/redis

echo 1 > /proc/sys/vm/overcommit_memory
