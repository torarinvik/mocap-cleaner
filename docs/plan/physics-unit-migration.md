# Physics length unit migration

[Shared acceptance requirements](acceptance-and-dependencies.md)

## Source implementation

Physics length inputs and kernels now use integer 0.1 mm units. The boundary
`src/physics/length_boundary.elisa` admits finite world coordinates within the
supported metre range, rounds once at the 0.1 mm boundary, and provides the
bounded inverse. Speed and per-frame-squared gravity conversions state their
time basis. Angular acceleration, drift, and angle gaps retain microradians;
the generic `Limb::micro` and angular limits were not rescaled.

The migration covers foot heights and floors, horizontal speed and contact
thresholds, support geometry and margins, COM/capture points, ballistic heights
and gravity, correction back to world coordinates, and the Studio floor
inverse. Contact thresholds that collapse at the migrated precision are
unavailable. Invalid world/contact/balance inputs and out-of-range corrections
are reported as unavailable instead of clean measurements. Ballistic residuals
are explicitly converted back to micrometres for the existing CLI fields;
report overflow clears both accumulated sums and is represented as unavailable
(JSON `null` plus an availability field).

Proof sources were updated or added for the length boundary, balance domains,
world admission and inverse, contact precision, COM/capture admission, report
conversion/overflow, and support-area bounds. They have not yet been qualified
against the current authenticated compiler/prover source and linked dependency
set. Source implementation is complete; native Studio overlay behavior and
corpus decision comparisons remain unverified.

## Migrated dimensions

| Boundary | Callers | Internal dimension |
| --- | --- | --- |
| Foot height and floor | `Physics::foot_lows`, `floor_of`, `foot_flags` | 0.1 mm |
| Horizontal foot speed and threshold | `Physics::foot_flags` | 0.1 mm per second |
| Support corners, margin, COM and capture point | `support_points`, `balance_frames` | 0.1 mm |
| Gravity step | `Physics::gravity_step` | 0.1 mm per frame squared |
| COM height and ballistic residual | `com_heights`, `residual`, `ballistic_fix` | 0.1 mm internally |
| Floor and ballistic correction inverse | `floor_metres`, `ballistic_fix`, `StudioModel::balance_of` | metres at world boundary |
| Ballistic CLI text and JSON | `src/cli/output.elisa` | micrometres at report boundary |
| Angular acceleration and rotation drift | `accelerations`, momentum drift comparison | microradians |

## Qualification still required

- Rebuild and authenticate the selected compiler and proof assistant against
  their exact current source and linked dependencies. Compile the current
  physics proof graph; compilation alone is not proof discharge.
- Compare CLI and Studio contacts, balance and airborne decisions against a
  fixed source corpus, including threshold-adjacent cases. Record expected
  changes caused by 0.1 mm rounding before acceptance.
- Cover negative coordinates, sub-unit heights, signed half-unit ties,
  supported-coordinate extremes, nonfinite input, invalid contact sources,
  collapsed thresholds and correction refusal. Verify refusal preserves the
  document and prior findings.
- Cover zero/one-frame clips, nonuniform sample times, report accumulation
  overflow, and explicit unavailable outcomes. Confirm no unavailable value
  appears as a measured zero in CLI or Studio.
- Review the native Studio overlay and correction behavior. No native
  qualification is claimed by the source migration or proof-source edits.
- Keep angular caps, acceleration and drift outputs unchanged by the length
  migration.
