#!/usr/bin/env python3
"""
Given a CSV of experiment results, plot IPC and CPI.
CSV columns: experiment,config,ipc,cpi,notes
"""
import pandas as pd, matplotlib.pyplot as plt, sys, pathlib

def main():
    if len(sys.argv)<3:
        print("Usage: plot_results.py results.csv out_prefix", file=sys.stderr); sys.exit(2)
    df=pd.read_csv(sys.argv[1])
    out=sys.argv[2]
    # IPC
    ax=df.pivot(index="experiment", columns="config", values="ipc").plot(kind="bar", rot=0)
    ax.set_ylabel("IPC (inst/cycle)")
    plt.tight_layout()
    plt.savefig(out+"_ipc.png", dpi=200)
    plt.close()
    # CPI
    ax=df.pivot(index="experiment", columns="config", values="cpi").plot(kind="bar", rot=0)
    ax.set_ylabel("CPI (cycles/inst)")
    plt.tight_layout()
    plt.savefig(out+"_cpi.png", dpi=200)
    plt.close()

if __name__=="__main__":
    main()
