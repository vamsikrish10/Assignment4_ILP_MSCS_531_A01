"""
assignment4_ilp/configs/ilp_basic.py
A minimal SE-mode config using gem5 stdlib components.
Runs a single binary on a MinorCPU (in-order pipeline) and enables MinorTrace for per-cycle pipeline viewing.

Run (from gem5 repo root):
  build/<ISA>/gem5.opt assignment4_ilp/configs/ilp_basic.py --binary <path> --args "<args>" --outdir m5out/basic

Notes:
- MinorCPU has a fixed in-order pipeline and supports MinorTrace/minorview.py visualization.
"""
import argparse
from gem5.utils.requires import requires
from gem5.isas import ISA
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator

parser = argparse.ArgumentParser()
parser.add_argument("--binary", required=True, help="Path to statically-linked SE binary")
parser.add_argument("--args", default="", help="Arguments string passed to the binary")
parser.add_argument("--outdir", default="m5out/basic")
args = parser.parse_args()

# This script is ISA-agnostic but gem5 must be built for the target ISA.
requires(isa_required=ISA.NULL)

board = SimpleBoard(
    clk_freq="2GHz",
    processor=SimpleProcessor(cpu_type=CPUTypes.MINOR, num_cores=1),
    memory=SingleChannelDDR3_1600(size="1GiB"),
    cache_hierarchy=NoCache(),
)

board.set_se_binary_workload(BinaryResource(local_path=args.binary, arguments=args.args.split()))
sim = Simulator(board=board)
sim.run()
print("Finished simulation.")
