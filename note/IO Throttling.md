
##### mm/page-writeback.c
##### balance_dirty_pages
gdtc: 전체에 대한 dirty throttling controller
mdtc: 특정 메모리 cgroup에 대한 dtc, mem cgroup이 없으면 NULL

mem cgroup이 없다와 strictlimit이 아니라고 가정해서 단순화된 수도 코드
실제로 (strictlimit은 거의 설정되지 않는게 맞는듯? bdi dependent)
~~~
for loop (true) {
	 dirty = 현재 메모리의 dirty page 수
	 thresh = dirty_ratio 값 (기본 20)에 기반한 page 수
	 bg_thresh = dirty_background_ratio 값 (기본 10)에 기반한 page 수

	if (dirty <= ((thresh + bg_thresh) / 2)) 
	{
		current->dirty_paused_when = now
		current->nr_dirtied = 0;
		current->nr_dirtied_pause = 무언가 현재 상태에 기반 한 값 (추후  balance_dirty_pages를 실행할지 말지 계산에 사용됨 )
		break;
	}

	// gdtc의 wb_thresh, wb_bg_thresh, wb_dirty 값을 업데이트
	// 뭘보고? 뭘 위해? => 여기서 bdi의 min, max ratio 등장
	wb_dirty_limits(gdtc);

	dirty_exceeded = ????

	wb_position_ratio(gdtc);
	sdtc = gdtc;

	// wb의 dirty_ratelimit, balanced_dirty_ratelimit 재계산
	if (쓴지 일정시간 지났으면)
		__wb_update_bandwidth(gdtc, mdtc, true);
		

	dirty_ratelimit = wb->dirty_ratelimit;
	task_ratelimit = (dirty_ratelimit * sdtc->pos_ratio) >> RATELIMIT_CALC_SHIFT; // shift는 10

	min_pause = ????
	max_pasue = ????

	// pages_dirtied는 current->nr_dirtied
	period = HZ * pages_dirtied / task_ratelimit;
	pasue = period;
	if (current->dirty_paused_when)
		pause -= now - current->dirty_paused_when;

	if (pause < min_pause)
		후처리
		break;

	//실제 쓰로틀링 ㄱㄱ
	wb->dirty_sleep = now;
	io_schedule_timeout(pause);

	current->dirty_paused_when = now + pause;
	current->nr_dirtied = 0;
	current->nr_dirtied_pause = nr_dirtied_pause; // min_pause 계산시 같이 계산됨


	/*
		this is typically equal to (dirty < thresh) 
		and can also keep "1000+ dd on a slow USB stick"
		under control
		=> 뭔말이야? 저 USB 문장 표현은 wb_thresh 계산할때 나오긴함 
	*/
	if (task_ratelimit)
	// 0이면 max_pause가 되고 있기 때문에
	// 엄청 큰 쓰로틀링이 필요한 상황이라고 추측
		break;
}
~~~



##### Block device의 WriteBack
- mm/backing-dev.c에서 default_bdi_init을 통해 "writeback" workqueue 생성후 bdi_wq 전역 변수에 대입
	- /sys/bus/workqueue/devices/writeback에서 관련 sysfs 확인 가능
	- 해당 writeback 워크큐의 워크를 수행하는 워커 쓰레드는 kworker/u~
	- **이 kworker는 block device당 하나야?**
	
- bdi 마다 wb_workfn을 수행하는 work가 queue_delayed_work를 통해 bdi_wq에 큐잉됨
	- bdi_wq는 위에 적힌 듯 전역 변수
	- work는 bdi의 wb_list에 달려있는데, 일반적으로는 하나의 wb이고, cgroup 때문에 여러개가 매달릴 수 있는 구조인듯
- wb_workfn에서는 실제로 writeback을 수행하는데, 이 때 wb_writeback_work 구조체가 매달려 있는 work_list만을 가지고 loop를 돌고, 비어있으면 수행이 끝남
	- 여기에서 wb_wb_work마다 sb를 가지고 있어서 파일시스템에 접근 가능

- wb구조체에는 dirty inode들이 매달려있는 b_dirty 리스트가 있음
- b_dirty 리스트에서 expire된 아이노드들을 b_io로 옮김
- b_io로 옮겨진 아이노드들 중에서 지금 작업하는 wb_wb_work의 sb에 해당하는 아이노드들만을 writeback 수행함
- 이때 b_dirty, b_io 등은 /sys/kernel/debug/bdi/\<device number\>에서 확인 가능함

#Linux/Kernel 