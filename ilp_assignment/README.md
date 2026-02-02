# ILP Assignment (gem5)

## Folder structure
- `configs/` : gem5 configuration files (SE-mode) for pipeline, branch prediction, superscalar width, SMT
- `workloads/` : C workloads (hello + ILP microbenchmarks). Compile to the target ISA and run in SE mode.
- `output/` : helper scripts, example outputs, figures, and (optional) compiled binaries
- `screenshots/` : your *real* terminal screenshots (and included examples)
- `report/` : final report (DOCX/PDF). Update with your GitHub repo link and replace example metrics with your measured values.

## Typical run (from gem5 repo root)
```bash
build/X86/gem5.opt configs/ilp_basic.py --binary <path_to_binary>
```


