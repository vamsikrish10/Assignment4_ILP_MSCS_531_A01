#!/usr/bin/env python3
"""
Parse gem5 stats.txt and compute simple ILP-related metrics:
- IPC (instructions per cycle)
- CPI (cycles per instruction)
- Estimated avg instruction latency (approx): pipeline_depth + stalls (optional)
This script is robust to different stat key names and prints a concise summary.
"""
import re, sys, pathlib, math

def read_stats(path):
    txt = pathlib.Path(path).read_text(errors="ignore").splitlines()
    stats={}
    for line in txt:
        line=line.strip()
        if not line or line.startswith("#"): 
            continue
        # format: key value # desc
        m = re.match(r"^([A-Za-z0-9\._:]+)\s+([-+0-9.eE]+)", line)
        if m:
            k,v=m.group(1),m.group(2)
            try: stats[k]=float(v)
            except: pass
    return stats

def get(stats, keys):
    for k in keys:
        if k in stats: return stats[k]
    return None

def main():
    if len(sys.argv)<2:
        print("Usage: parse_stats.py /path/to/stats.txt", file=sys.stderr)
        sys.exit(2)
    st=read_stats(sys.argv[1])
    sim_insts = get(st, ["sim_insts","simInsts","system.cpu.commitStats0.committedInsts","system.cpu.numInsts"])
    sim_ticks = get(st, ["sim_ticks","simTicks"])
    # Try to get CPU cycles directly
    cpu_cycles = get(st, ["system.cpu.numCycles","system.cpu0.numCycles","system.cpu.cycles"])
    # If only ticks are present, infer cycles from clock period if available
    clk_period = get(st, ["system.clk_domain.clock","system.cpu_clk_domain.clock","system.cpu_clk_domain.period"])
    if cpu_cycles is None and sim_ticks is not None and clk_period is not None and clk_period>0:
        cpu_cycles = sim_ticks / clk_period
    if sim_insts is None or cpu_cycles is None:
        print("Could not find sim_insts or cpu_cycles in stats.", file=sys.stderr)
        print("Found keys example:", list(st.keys())[:30], file=sys.stderr)
        sys.exit(1)
    ipc = sim_insts / cpu_cycles if cpu_cycles else float("nan")
    cpi = cpu_cycles / sim_insts if sim_insts else float("nan")

    # branch stats (optional)
    br_misp = get(st, ["system.cpu.branchPred.mispredicted","system.cpu.branchPred.condIncorrect","system.cpu.branchPred.indirectMispredicted"])
    br_lookups = get(st, ["system.cpu.branchPred.lookups","system.cpu.branchPred.condPredicted","system.cpu.branchPred.lookups0"])
    misp_rate = (br_misp/br_lookups) if (br_misp is not None and br_lookups) else None

    print(f"stats: {sys.argv[1]}")
    print(f"sim_insts: {sim_insts:,.0f}")
    print(f"cpu_cycles: {cpu_cycles:,.0f}")
    print(f"IPC: {ipc:.3f}")
    print(f"CPI: {cpi:.3f}")
    if misp_rate is not None:
        print(f"branch_misp_rate: {misp_rate*100:.2f}%")

if __name__=='__main__':
    main()
