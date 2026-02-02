#!/usr/bin/env bash
# Build static Linux binaries inside Docker so they run in gem5 SE mode.
# Usage examples (from gem5 repo root):
#   ./assignment4_ilp/scripts/build_bins.sh x86_64
#   ./assignment4_ilp/scripts/build_bins.sh aarch64
set -euo pipefail
ISA="${1:-x86_64}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/outputs/bins/$ISA"
mkdir -p "$OUT"

if [[ "$ISA" == "x86_64" ]]; then
  IMG="ubuntu:22.04"
  CC="gcc"
  CFLAGS="-O2 -static -pthread"
elif [[ "$ISA" == "aarch64" ]]; then
  IMG="arm64v8/ubuntu:22.04"
  CC="gcc"
  CFLAGS="-O2 -static -pthread"
else
  echo "Unsupported ISA: $ISA (use x86_64 or aarch64)" >&2
  exit 1
fi

docker run --rm -v "$ROOT:/work" -w /work "$IMG" bash -lc "
  apt-get update >/dev/null && apt-get install -y build-essential >/dev/null
  mkdir -p $OUT
  $CC $CFLAGS benchmarks/hello.c -o $OUT/hello
  $CC $CFLAGS benchmarks/ilp_int.c -o $OUT/ilp_int
  $CC $CFLAGS benchmarks/ilp_mem.c -o $OUT/ilp_mem
  $CC $CFLAGS benchmarks/ilp_fp.c -o $OUT/ilp_fp
  $CC $CFLAGS benchmarks/smt_pthreads.c -o $OUT/smt_pthreads
  file $OUT/*
"
echo "Binaries in: $OUT"
