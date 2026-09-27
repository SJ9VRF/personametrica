# Compute resources

All controlled PersonaMetrica-Bench experiments in this release run on CPU; no GPU is required.

Validation environment used for the checked-in timings:

- CPU: Intel Xeon Platinum 8573C (5 visible CPU cores)
- RAM available to the container: ~5.8 GiB
- OS: Linux x86_64, kernel 6.18.44
- Python experiments are single-process unless a script explicitly states otherwise.

Measured wall-clock examples on this environment:

| Experiment | Wall time | Peak RSS |
|---|---:|---:|
| Standard distribution-shift benchmark script | 2.22 s | ~96.5 MiB |
| 10-seed PBS component ablations | 2.63 s | ~95.2 MiB |
| 48-cell stress grid | 4.68 s | ~93.3 MiB |

These values are environment-specific and are provided to make the scale of the experiments transparent, not as performance claims. The broader reproduction pipeline takes longer because it also rebuilds datasets, figures, dashboards, paper artifacts, training-data audits, and release validation.

The project contains no hidden GPU training run supporting the paper's primary controlled claims. External-model experiments are explicitly marked not run in this environment.
