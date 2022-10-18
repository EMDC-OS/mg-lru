#!/bin/bash


echo "test"
echo 3 > /proc/sys/vm/drop_caches
#numactl --cpubind=0 --membind=0 mpirun -np 32 ./hacc_io_write 2700000 /home/jongseok/pmem/
mpirun -np 128 ./hacc_io_write 2700000 /home/jongseok/pmem/

