"""
assignment4_ilp/configs/ilp_superscalar.py
O3CPU with configurable width parameters (fetch/decode/rename/dispatch/issue/wb/commit).

Example:
  build/<ISA>/gem5.opt assignment4_ilp/configs/ilp_superscalar.py --binary <bin> --width 1 --outdir m5out/width1
  build/<ISA>/gem5.opt assignment4_ilp/configs/ilp_superscalar.py --binary <bin> --width 4 --outdir m5out/width4
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
parser.add_argument("--width", type=int, default=4)
parser.add_argument("--outdir", default="m5out/width")
args = parser.parse_args()

requires(isa_required=ISA.NULL)

cache = PrivateL1PrivateL2CacheHierarchy(l1d_size="32KiB", l1i_size="32KiB", l2_size="256KiB")
memory = SingleChannelDDR3_1600(size="1GiB")

cpu = O3CPU()
w = args.width
cpu.fetchWidth = w
cpu.decodeWidth = w
cpu.renameWidth = w
cpu.dispatchWidth = w
cpu.issueWidth = w
cpu.wbWidth = w
cpu.commitWidth = w

processor = SimpleProcessor(cpu_type=CPUTypes.O3, num_cores=1)
processor.cores[0].core = cpu

board = SimpleBoard(clk_freq="2GHz", processor=processor, memory=memory, cache_hierarchy=cache)
board.set_se_binary_workload(BinaryResource(local_path=args.binary, arguments=args.args.split()))
sim = Simulator(board=board, outdir=args.outdir)
sim.run()
print("Finished simulation.")
