#!/bin/bash

echo 7 > /sys/kernel/mm/lru_gen/enabled

for ((i=4; i<=10; i++))
do
  echo $i
  echo 3 > /proc/sys/vm/drop_caches

  mpirun -np 8 /home/jongseok/mglru/benchmark/NPB3.4.2/NPB3.4-MPI/bin/ft.C.x >> ./mglru/${i}_1 &
  cd /home/jongseok/mglru/benchmark/fio_test/
  fio --name fio_test --rw=randrw --bs=256k --size=2G --numjobs=8 --group_reporting >> /home/jongseok/mglru/eval/16G/ft.C_fio.2G.8t.256bs/mglru/${i}_2 &
  cd /home/jongseok/mglru/eval/16G/ft.C_fio.2G.8t.256bs/

  sleep 180
done

echo 0 > /sys/kernel/mm/lru_gen/enabled

for ((i=4; i<=10; i++))
do
  echo $i
  echo 3 > /proc/sys/vm/drop_caches

  mpirun -np 8 /home/jongseok/mglru/benchmark/NPB3.4.2/NPB3.4-MPI/bin/ft.C.x >> ./lru/${i}_1 &
  cd /home/jongseok/mglru/benchmark/fio_test/
  fio --name fio_test --rw=randrw --bs=256k --size=2G --numjobs=8 --group_reporting >> /home/jongseok/mglru/eval/16G/ft.C_fio.2G.8t.256bs/lru/${i}_2 &
  cd /home/jongseok/mglru/eval/16G/ft.C_fio.2G.8t.256bs/

  sleep 180
done
