#!/usr/bin/python3
from bcc import BPF
import time

tpoint="""
#include "mmzone.h"
#include "swap.h"

struct scan_control {
	/* How many pages shrink_list() should reclaim */
	unsigned long nr_to_reclaim;

	/*
	 * Nodemask of nodes allowed by the caller. If NULL, all nodes
	 * are scanned.
	 */
	nodemask_t	*nodemask;

	/*
	 * The memory cgroup that hit its limit and as a result is the
	 * primary target of this reclaim invocation.
	 */
	struct mem_cgroup *target_mem_cgroup;

	/*
	 * Scan pressure balancing between anon and file LRUs
	 */
	unsigned long	anon_cost;
	unsigned long	file_cost;

	/* Can active pages be deactivated as part of reclaim? */
#define DEACTIVATE_ANON 1
#define DEACTIVATE_FILE 2
	unsigned int may_deactivate:2;
	unsigned int force_deactivate:1;
	unsigned int skipped_deactivate:1;

	/* Writepage batching in laptop mode; RECLAIM_WRITE */
	unsigned int may_writepage:1;

	/* Can mapped pages be reclaimed? */
	unsigned int may_unmap:1;

	/* Can pages be swapped as part of reclaim? */
	unsigned int may_swap:1;

	/*
	 * Cgroup memory below memory.low is protected as long as we
	 * don't threaten to OOM. If any cgroup is reclaimed at
	 * reduced force or passed over entirely due to its memory.low
	 * setting (memcg_low_skipped), and nothing is reclaimed as a
	 * result, then go back for one more cycle that reclaims the protected
	 * memory (memcg_low_reclaim) to avert OOM.
	 */
	unsigned int memcg_low_reclaim:1;
	unsigned int memcg_low_skipped:1;

	unsigned int hibernation_mode:1;

	/* One of the zones is ready for compaction */
	unsigned int compaction_ready:1;

	/* There is easily reclaimable cold cache in the current node */
	unsigned int cache_trim_mode:1;

	/* The file pages on the current node are dangerously low */
	unsigned int file_is_tiny:1;

	/* Always discard instead of demoting to lower tier memory */
	unsigned int no_demotion:1;

#ifdef CONFIG_LRU_GEN
	/* help make better choices when multiple memcgs are available */
	unsigned int memcgs_need_aging:1;
	unsigned int memcgs_need_swapping:1;
	unsigned int memcgs_avoid_swapping:1;
#endif

	/* Allocation order */
	s8 order;

	/* Scan (total_size >> priority) pages at once */
	s8 priority;

	/* The highest zone to isolate pages for reclaim from */
	s8 reclaim_idx;

	/* This context's GFP mask */
	gfp_t gfp_mask;

	/* Incremented by the number of inactive pages that were scanned */
	unsigned long nr_scanned;

	/* Number of pages freed so far during a call to shrink_zones() */
	unsigned long nr_reclaimed;

	struct {
		unsigned int dirty;
		unsigned int unqueued_dirty;
		unsigned int congested;
		unsigned int writeback;
		unsigned int immediate;
		unsigned int file_taken;
		unsigned int taken;
	} nr;

	/* for recording the reclaimed slab by now */
	struct reclaim_state reclaim_state;
};

BPF_PERF_OUTPUT(events);


BPF_HASH(ncursc, u32, struct scan_control *);
BPF_HASH(ncurts, u32);
int kprobe__shrink_node(struct pt_regs *ctx, pg_data_t *pgdat, struct scan_control *sc)
{
        u64 ts = bpf_ktime_get_ns();
        u32 pid = bpf_get_current_pid_tgid();
        ncursc.update(&pid, &sc);
        ncurts.update(&pid, &ts);
        return 0;
}
int kretprobe__shrink_node(struct pt_regs *ctx)
{
        u32 pid = bpf_get_current_pid_tgid();
	int ret = PT_REGS_RC(ctx);
        u64 *time;
        u64 cur_time;
        struct scan_control **scp;
	char comm[TASK_COMM_LEN];

        time = ncurts.lookup(&pid);
        scp = ncursc.lookup(&pid);
        if (scp == 0 || time == 0) {
            return 0;
        }

        struct scan_control *sc = *scp;
        cur_time = bpf_ktime_get_ns() - *time;

        ncursc.delete(&pid);
        ncurts.delete(&pid);
	bpf_get_current_comm(comm, sizeof(comm));

	bpf_trace_printk("NODE %s: %lu %lu\\n", comm, cur_time, sc->nr_reclaimed);
        return 0;
}

//int kretprobe__pgdat_balanced(struct pt_regs *ctx, pg_data_t *pgdat, int order, int highest_zoneidx)
//{
//	int ret = PT_REGS_RC(ctx);
//	char comm[TASK_COMM_LEN];
//	bpf_get_current_comm(comm, sizeof(comm));
//	bpf_trace_printk("BALANCED: %s %d\\n", comm, ret);
//}
//

BPF_HASH(prevr, u32);
BPF_HASH(cursc, u32, struct scan_control *);
BPF_HASH(curts, u32);
int kprobe__shrink_lruvec(struct pt_regs *ctx, struct lruvec *lruvec, struct scan_control *sc)
{
        u64 ts = bpf_ktime_get_ns();
        u64 prev = sc->nr_reclaimed;
        u32 pid = bpf_get_current_pid_tgid();
        cursc.update(&pid, &sc);
        curts.update(&pid, &ts);
	prevr.update(&pid, &prev);
        return 0;
}

int kretprobe__shrink_lruvec(struct pt_regs *ctx)
{
        u32 pid = bpf_get_current_pid_tgid();
	int ret = PT_REGS_RC(ctx);
        u64 *time, *prev;
        u64 cur_time;
        struct scan_control **scp;
	char comm[TASK_COMM_LEN];

        time = curts.lookup(&pid);
        scp = cursc.lookup(&pid);
        prev = prevr.lookup(&pid);
        if (scp == 0 || time == 0 || prev == 0) {
            return 0;
        }

        struct scan_control *sc = *scp;
        cur_time = bpf_ktime_get_ns() - *time;

        cursc.delete(&pid);
        curts.delete(&pid);
	bpf_get_current_comm(comm, sizeof(comm));

	//if ((data.nr_reclaimed - *prev)  != 0)
	bpf_trace_printk("LRUVEC %s: %lu %lu\\n", comm, cur_time, sc->nr_reclaimed - *prev);
        return 0;
}

//int kretprobe__evict_folios(struct pt_regs *ctx, struct lruvec *lruvec, struct scan_control *sc, int swappiness,
//			bool *need_swapping)
//{
//	int ret = PT_REGS_RC(ctx);
//	char comm[TASK_COMM_LEN];
//	bpf_get_current_comm(comm, sizeof(comm));
//	bpf_trace_printk("EVICT_FOL: %s %d\\n", comm, ret);
//}

BPF_HASH(tryts, u32);
int kprobe__try_to_inc_max_seq(struct pt_regs *ctx, struct lruvec *lruvec, unsigned long max_seq,
			       struct scan_control *sc, bool can_swap, bool force_scan)
{
        u64 ts = bpf_ktime_get_ns();
        u32 pid = bpf_get_current_pid_tgid();
        tryts.update(&pid, &ts);
        return 0;
}
int kretprobe__try_to_inc_max_seq(struct pt_regs *ctx, struct lruvec *lruvec, unsigned long max_seq,
			       struct scan_control *sc, bool can_swap, bool force_scan)
{	
	u64 *time;
        u64 cur_time;
	char comm[TASK_COMM_LEN];
	int ret = PT_REGS_RC(ctx);
        u32 pid = bpf_get_current_pid_tgid();

        time = tryts.lookup(&pid);
        if (time == 0) {
            return 0;
        }

        cur_time = bpf_ktime_get_ns() - *time;
        tryts.delete(&pid);
	bpf_get_current_comm(comm, sizeof(comm));
	bpf_trace_printk("TRY_MAX %s: %lu %lu\\n", comm, cur_time, ret);
        return 0;
}
BPF_HASH(its, u32);
int kprobe__isolate_folios(struct pt_regs *ctx, struct lruvec *lruvec, struct scan_control *sc, int swappiness,
			  int *type_scanned, struct list_head *list)
{
        u64 ts = bpf_ktime_get_ns();
        u32 pid = bpf_get_current_pid_tgid();
        its.update(&pid, &ts);
        return 0;
}
int kretprobe__isolate_folios(struct pt_regs *ctx, struct lruvec *lruvec, struct scan_control *sc, int swappiness,
			  int *type_scanned, struct list_head *list)
{
	u64 *time;
        u64 cur_time;
	char comm[TASK_COMM_LEN];
	int ret = PT_REGS_RC(ctx);
        u32 pid = bpf_get_current_pid_tgid();

        time = its.lookup(&pid);
        if (time == 0) {
            return 0;
        }

        cur_time = bpf_ktime_get_ns() - *time;
        its.delete(&pid);
	bpf_get_current_comm(comm, sizeof(comm));
	bpf_trace_printk("ISOL_FOL %s: %lu %lu\\n", comm, cur_time, ret);
        return 0;
}


BPF_HASH(tts, u32);
int kprobe__shrink_page_list(struct pt_regs *ctx, struct list_head *page_list,
				     struct pglist_data *pgdat,
				     struct scan_control *sc,
				     struct reclaim_stat *stat,
				     bool ignore_references)
{
        u64 ts = bpf_ktime_get_ns();
        u32 pid = bpf_get_current_pid_tgid();
        tts.update(&pid, &ts);
        return 0;
}
int kretprobe__shrink_page_list(struct pt_regs *ctx, struct list_head *page_list,
				     struct pglist_data *pgdat,
				     struct scan_control *sc,
				     struct reclaim_stat *stat,
				     bool ignore_references)
{
        u64 *time;
        u64 cur_time;
	char comm[TASK_COMM_LEN];
	int ret = PT_REGS_RC(ctx);
        u32 pid = bpf_get_current_pid_tgid();

        time = tts.lookup(&pid);
        if (time == 0) {
            return 0;
        }

        cur_time = bpf_ktime_get_ns() - *time;
        tts.delete(&pid);
	bpf_get_current_comm(comm, sizeof(comm));
	bpf_trace_printk("SHR_LIST %s: %lu %lu\\n", comm, cur_time, ret);
}

BPF_HASH(alts, u32);
int kprobe__shrink_active_list(struct pt_regs *ctx, unsigned long nr_to_scan,
			       struct lruvec *lruvec,
			       struct scan_control *sc,
			       enum lru_list lru)
{
        u64 ts = bpf_ktime_get_ns();
        u32 pid = bpf_get_current_pid_tgid();
        alts.update(&pid, &ts);
        return 0;
}
int kretprobe__shrink_active_list(struct pt_regs *ctx, unsigned long nr_to_scan,
			       struct lruvec *lruvec,
			       struct scan_control *sc,
			       enum lru_list lru)
{
        u64 *time;
        u64 cur_time;
	char comm[TASK_COMM_LEN];
        u32 pid = bpf_get_current_pid_tgid();

        time = alts.lookup(&pid);
        if (time == 0) {
            return 0;
        }

        cur_time = bpf_ktime_get_ns() - *time;
        alts.delete(&pid);
	bpf_get_current_comm(comm, sizeof(comm));
	bpf_trace_printk("ACT_LIST %s: %lu %lu\\n", comm, cur_time);
}

BPF_HASH(ilts, u32);
int kprobe__shrink_inactive_list(struct pt_regs *ctx, unsigned long nr_to_scan,
			       struct lruvec *lruvec,
			       struct scan_control *sc,
			       enum lru_list lru)
{
        u64 ts = bpf_ktime_get_ns();
        u32 pid = bpf_get_current_pid_tgid();
        ilts.update(&pid, &ts);
        return 0;
}
int kretprobe__shrink_inactive_list(struct pt_regs *ctx, unsigned long nr_to_scan,
			       struct lruvec *lruvec,
			       struct scan_control *sc,
			       enum lru_list lru)
{
        u64 *time;
        u64 cur_time;
	char comm[TASK_COMM_LEN];
        u32 pid = bpf_get_current_pid_tgid();

        time = ilts.lookup(&pid);
        if (time == 0) {
            return 0;
        }

        cur_time = bpf_ktime_get_ns() - *time;
        ilts.delete(&pid);
	bpf_get_current_comm(comm, sizeof(comm));
	bpf_trace_printk("INACT_LIST %s: %lu %lu\\n", comm, cur_time);
}

//TRACEPOINT_PROBE(vmscan, mm_vmscan_direct_reclaim_begin) {
//	
//	bpf_trace_printk("dstart: %lu %d\\n", bpf_ktime_get_ns(), args->order);
//	return 0;
//}
//TRACEPOINT_PROBE(vmscan, mm_vmscan_direct_reclaim_end) {
//	bpf_trace_printk("dend: %lu %lu\\n", bpf_ktime_get_ns(), args->nr_reclaimed);
//	return 0;
//}

"""

bpf = BPF(text=tpoint)

def process_event(cpu, data, size):
    event = bpf["events"].event(data)
    print(event.elapsed_time)
    print(event.nr_reclaimed)


if __name__ == "__main__":
	while 1:
		(task, pid, cpu, flags, ts, msg) = bpf.trace_fields()
		print(msg)
	

