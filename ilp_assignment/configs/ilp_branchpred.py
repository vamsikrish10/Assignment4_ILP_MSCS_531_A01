"""
assignment4_ilp/configs/ilp_branchpred.py
Runs the same binary on O3CPU with configurable branch predictor (via --bp).

Example (from gem5 repo root):
  build/<ISA>/gem5.opt assignment4_ilp/configs/ilp_branchpred.py --binary <bin> --bp StaticBP --outdir m5out/bp_static
  build/<ISA>/gem5.opt assignment4_ilp/configs/ilp_branchpred.py --binary <bin> --bp LTAGE --outdir m5out/bp_ltage
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
parser.add_argument("--binary", required=True)
parser.add_argument("--args", default="")
parser.add_argument("--bp", default="LTAGE",
                    help="Branch predictor class name (e.g., StaticBP, LocalBP, TournamentBP, BiModeBP, LTAGE)")
parser.add_argument("--outdir", default="m5out/bp")
args = parser.parse_args()

requires(isa_required=ISA.NULL)

cache = PrivateL1PrivateL2CacheHierarchy(l1d_size="32KiB", l1i_size="32KiB", l2_size="256KiB")
memory = SingleChannelDDR3_1600(size="1GiB")

# Build O3 core with tunable branch predictor (via SimObject lookup)
from m5.objects import *
bp_cls = globals().get(args.bp, None)
if bp_cls is None:
    raise SystemExit(f"Unknown bp class '{args.bp}'. Try e.g. StaticBP, LocalBP, TournamentBP, BiModeBP, LTAGE.")

cpu = O3CPU(branchPred=bp_cls())
processor = SimpleProcessor(cpu_type=CPUTypes.O3, num_cores=1)
# Replace core 0 with our custom cpu instance
processor.cores[0].core = cpu

board = SimpleBoard(clk_freq="2GHz", processor=processor, memory=memory, cache_hierarchy=cache)
board.set_se_binary_workload(BinaryResource(local_path=args.binary, arguments=args.args.split()))
sim = Simulator(board=board, outdir=args.outdir)
sim.run()
print("Finished simulation.")
