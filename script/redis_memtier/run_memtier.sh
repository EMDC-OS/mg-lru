#!/bin/bash

#load objects
for ((i=0;i<1;i++))
do
  echo /var/run/redis${i}/redis-server.sock
  memtier_benchmark -S /var/run/redis/redis-server.sock -P redis \
      -n allkeys -c 4 -t 4 --ratio 1:0 --pipeline 8 -d 4000 \
      --key-minimum=1 --key-maximum=8000000 --key-pattern=P:P &
done

wait

#run benchmark
for ((i=0;i<1;i++))
do
  memtier_benchmark -S /var/run/redis/redis-server.sock -P redis \
      --test-time=600 -c 4 -t 4 --ratio 0:1 --pipeline 8 \
      -- randomize --distinct-client-seed --key-minimum=1 \
      --key-maximum=8000000 --key-pattern=G:G &
done

wait
