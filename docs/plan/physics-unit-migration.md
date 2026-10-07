# Remaining physics unit migration

[Shared acceptance requirements](acceptance-and-dependencies.md)

Source inventory at primary `9a952f8`. Limb reach lengths already use 0.1 mm;
the following physics paths still use micrometres. This inventory is remaining
work, not qualification evidence.

`PhysicsLengthBoundary` now supplies bounded integer micrometre admission,
0.1 mm conversion and explicit report conversion admission. Ten obligations
compile with d2754a8e. It is not yet wired into physics callers; authenticated
replay and the world-float boundary remain open. World floats must round once
at the final unit boundary, rather than first rounding to micrometres.
Coverage includes both signed half-unit ties, values below half a unit and
exact report-unit recovery; compilation does not establish proof validity.
The world adapter now has explicit finite/range admission and rounds once
directly from metres into 0.1 mm units, with a bounded inverse. Seven additional
world-boundary obligations cover nonfinite/out-of-range refusal, both supported
coordinate limits, signed half-unit ties and a one-metre inverse. Compilation
was refused before source processing because the compiler source changed during
its repair batch; current product rebuild and proof qualification are pending.
Physics callers remain on their old scale until the complete migration lands.
The floor inverse is now centralized in `Physics::floor_metres`, used by balance,
Studio drawing and the existing physics check. Three inverse obligations retain
the current micrometre scale; change producer, inverse and laws together during
migration. Compilation/replay awaits the repaired current compiler/prover.

| Boundary | Current callers | Required dimension |
| --- | --- | --- |
| Foot height and floor | `Physics::foot_lows`, `floor_of`, `foot_flags` | 0.1 mm |
| Horizontal foot speed and threshold | `Physics::foot_flags` | 0.1 mm per second |
| Support corners, margin and COM/capture point | `support`, `balance_frames` | 0.1 mm |
| Gravity step | `Physics::gravity_step` | 0.1 mm per frame squared |
| COM height and ballistic residual | `com_heights`, `residual`, `ballistic_fix` | 0.1 mm internally |
| Floor back to world coordinates | `balance_frames`, `StudioModel::balance_of` | Metres at inverse boundary |
| Ballistic correction back to world coordinates | `Physics::ballistic_fix` | Metres at inverse boundary |
| Ballistic CLI text and JSON | `src/cli/output.elisa` | Micrometres at report boundary |
| Angular acceleration and rotation drift | `accelerations`, momentum drift comparison | Keep microradians |

## Required implementation order

1. Add a dimension-specific physics length boundary, with explicit finite
   input admission, nearest rounding, saturation policy and a matching inverse.
   Keep speed and gravity time bases explicit even though they share length
   scaling. Do not change the generic angular `Limb::micro` multiplier.
2. Move foot heights, floor, speed and thresholds together. Replace the use of
   the angular `Hinge::Domain::LIMIT` for length bounds. Preserve contact
   threshold ordering and diagnose thresholds that collapse after rounding.
3. Move support corners, COM and capture points with their margins and bounds.
   Audit squared distances and signed-area products at extreme coordinates.
4. Move ballistic heights and gravity together with `Balance` length limits.
   Update the world-space inverse before enabling the migrated fix. Retain
   frame-domain limits and independent angular limits.
5. Convert residuals explicitly back to micrometres for existing report fields.
   Prove conversion and accumulated-sum overflow admission; never relabel a
   0.1 mm residual as micrometres. Update every text/JSON producer consistently.
6. Update the Studio floor inverse with the physics producer. Compare CLI and
   Studio contacts, balance and airborne decisions for the same source clip.

## Qualification still required

- Propagate a typed unavailable/refused outcome from invalid contact, COM and
  world-coordinate inputs through CLI reports and Studio overlays. Missing feet,
  nonfinite coordinates or collapsed thresholds must not become all-false
  contact flags that are interpreted as airborne or a clean balance result.
  Track-shape guards now refuse mismatched contact/COM counts before indexing;
  this prevents invalid access but does not yet supply that reporting outcome.
  Verify refused corrections preserve the source document and prior findings.
- Authenticated rounding, sign, domain, saturation and inverse laws.
- Negative coordinates, sub-unit heights, half-unit ties, extreme supported
  coordinates and nonfinite input refusal.
- Contact thresholds around rounding boundaries, zero/one-frame takes and
  nonuniform sample times; preserve or explicitly qualify the frame-rate model.
- Ballistic residuals, corrections and exported micrometre reports compared
  with a fixed corpus. Record expected precision changes before acceptance.
- Keep angular cap, acceleration and drift outputs unchanged by this migration.
- Current complete compiler/prover qualification and native overlay review.
