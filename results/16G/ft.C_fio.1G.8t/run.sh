mpirun -np 8 /home/jongseok/mglru/benchmark/NPB3.4.2/NPB3.4-MPI/bin/ft.C.x >> ${1}_1 &
cd /home/jongseok/mglru/benchmark/fio_test/
fio --name fio_test --rw=randrw --bs=4k --size=1G --numjobs=8 --group_reporting >> /home/jongseok/mglru/eval/16G/ft.C_fio.1G.8t/${1}_2 &
