#!/bin/bash

dist=( "lru" "mglru" )
thread=( 16 32 )
mem1=( "2G" "3G" "4G" "5G")
mem2=( "1G" "2G" "3G" )
pattern=( "random" "normal:40" "zipf:0.8" )

FDIR="/home/jongseok/mglru/benchmark/fio_test"
EDIR="/home/jongseok/mglru/eval_tmp"

for t in ${thread[@]}
do
  if [ $t -eq 16 ] 
  then
    mem=${mem1[@]}
  else
    mem=${mem2[@]}
  fi

  for m in ${mem[@]}
  do
    for d in ${dist[@]}
    do
      if [ $d = "lru" ] 
      then
        enabled=0
      else
        enabled=7
      fi
      for p in ${pattern[@]}
      do

        echo 3 > /proc/sys/vm/drop_caches
        echo $enabled > /sys/kernel/mm/lru_gen/enabled
        
        for ((i=1; i<=3; i++))
        do
          echo hitratio_${d}_${t}t_${m}_${p}_${i}
          echo $enabled
          echo 3 > /proc/sys/vm/drop_caches

          cat /proc/131/sched > /kswapd_start_${d}_${t}t_${m}_${p}_${i}
          cat /proc/vmstat > ${EDIR}/vmstat_start_${d}_${t}t_${m}_${p}_${i}
          sleep 5
        
          /usr/share/bcc/tools/cachestat 10 > ${EDIR}/hitratio_${d}_${t}t_${m}_${p}_${i} &
          pid=`ps -aux | grep cachestat | head -n 1 | awk '{print $2}'`
          echo start >> ${EDIR}/hitratio_${d}_${t}t_${m}_${p}_${i}
        
          fio --name=randread \
           --directory=${FDIR} --size=${m} --io_size=1000TB \
           --time_based --numjobs=${t} --ioengine=io_uring \
           --ramp_time=20m --runtime=10m --iodepth=128 \
           --iodepth_batch_submit=32 --iodepth_batch_complete=32 \
           --rw=randread --random_distribution=${p} \
           --direct=0 --norandommap --group_reporting > ${EDIR}/fio_${d}_${t}t_${m}_${p}_${i}

          echo stop >> ${EDIR}/hitratio_${d}_${t}t_${m}_${p}_${i}
          sudo kill -9 $pid

          cat /proc/131/sched > ${EDIR}/kswapd_stop_${d}_${t}t_${m}_${p}_${i}
          cat /proc/vmstat > ${EDIR}/vmstat_stop_${d}_${t}t_${m}_${p}_${i}
        
        done #iter

      done # pattern
    done # dist
  done # mem
done # thread
