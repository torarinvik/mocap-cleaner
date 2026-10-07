# Limb length conversion and floating-point boundary qualification

## Current implementation

`Limb::solve_chain` uses 0.1 mm integer reach lengths. `LengthUnits` preserves
nearest rounding with ties away from zero, bounds integer conversion without
saturation, and exposes the canonical units-per-metre scale. The float/engine adapter now rounds directly to the final scale, avoiding an
intermediate micrometre rounding step. The integer micrometre converter remains
available for integer wire/report boundaries. Pole angles and
other angular rotation-vector values remain in microradians.

Commit `33f00d5` refuses non-finite segment lengths, target distance and requested
end rotation before integer conversion or joint writes. The guard uses strict
IEEE subtraction (`x - x != 0.0`) and is not annotated for fast math. Source O0
compilation succeeds; that result does not prove optimized executable behavior.

## Evidence required before closure

- Discharge the current integer contracts in `length_units_laws` and
  `limb_length_boundary_laws`, with independent replay and source correspondence.
- Qualify the actual optimized application compiler product and linked runtime;
  confirm floating-point guard bodies are emitted and strict semantics retained.
- Verify NaN, both infinities, finite large values, short/degenerate bones and
  valid inputs through the real adapter. Invalid inputs must leave joint edits
  unapplied; refreshing the caller-owned world cache is not a pose edit.
- Compare rounding behavior and motion quality on the current corpus, including
  contact targets and limbs near the 0.1 mm quantization boundary.
- Verify CLI, preview and export agree on the same integer/engine boundary.

The integer laws do not cover IEEE conversion, engine IK or native execution.
The existing fixture was compiled without execution. This record identifies
remaining qualification; it does not claim a new observed prover counterexample.
Other operation/physics length adapters still use legacy micrometre units and
require separate dimension-aware migration.
