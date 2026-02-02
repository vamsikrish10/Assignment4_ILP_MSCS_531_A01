"""
assignment4_ilp/configs/ilp_smt.py
Run two SE binaries concurrently on one O3 core using SMT (numThreads=2).

Example:
  build/<ISA>/gem5.opt assignment4_ilp/configs/ilp_smt.py \
      --bin0 <bin0> --args0 "<args>" --bin1 <bin1> --args1 "<args>" --outdir m5out/smt2
"""
import argparse
from gem5.utils.requires import requires
from gem5.isas import ISA
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_cache_hierarchy import (
    PrivateL1PrivateL2CacheHierarchy
)
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.o3_cpu import O3CPU
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator

parser = argparse.ArgumentParser()
parser.add_argument("--bin0", required=True)
parser.add_argument("--args0", default="")
parser.add_argument("--bin1", required=True)
parser.add_argument("--args1", default="")
parser.add_argument("--outdir", default="m5out/smt")
args = parser.parse_args()

requires(isa_required=ISA.NULL)

cache = PrivateL1PrivateL2CacheHierarchy(l1d_size="32KiB", l1i_size="32KiB", l2_size="512KiB")
memory = SingleChannelDDR3_1600(size="2GiB")

cpu = O3CPU(numThreads=2)
processor = SimpleProcessor(cpu_type=CPUTypes.O3, num_cores=1)
processor.cores[0].core = cpu

board = SimpleBoard(clk_freq="2GHz", processor=processor, memory=memory, cache_hierarchy=cache)

# Workloads: two BinaryResources into one CPU (SMT threads)
from m5.objects import Process
p0 = Process(cmd=[args.bin0] + (args.args0.split() if args.args0 else []))
p1 = Process(cmd=[args.bin1] + (args.args1.split() if args.args1 else []))
# Board helper for multiple processes isn't universal; set directly.
board.get_processor().get_cores()[0].core.workload = [p0, p1]
board.get_processor().get_cores()[0].core.createThreads()

sim = Simulator(board=board, outdir=args.outdir)
sim.run()
print("Finished simulation.")
