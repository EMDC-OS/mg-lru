#!/bin/bash

echo 7 > /sys/kernel/mm/lru_gen/enabled

for ((i=4; i<=10; i++))
do
  echo $i
  echo 3 > /proc/sys/vm/drop_caches
  mpirun -np 8 /home/jongseok/mglru/benchmark/NPB3.4.2/NPB3.4-MPI/bin/ft.C.x >> ./mglru/${i}_1 &
  mpirun -np 8 /home/jongseok/mglru/benchmark/NPB3.4.2/NPB3.4-MPI/bin/ft.C.x >> ./mglru/${i}_2 &
  sleep 180
done


echo 0 > /sys/kernel/mm/lru_gen/enabled
for ((i=4; i<=10; i++))
do
  echo $i
  echo 3 > /proc/sys/vm/drop_caches
  mpirun -np 8 /home/jongseok/mglru/benchmark/NPB3.4.2/NPB3.4-MPI/bin/ft.C.x >> ./lru/${i}_1 &
  mpirun -np 8 /home/jongseok/mglru/benchmark/NPB3.4.2/NPB3.4-MPI/bin/ft.C.x >> ./lru/${i}_2 &
  sleep 180
done
