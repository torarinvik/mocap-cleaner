# Remaining physics unit migration

[Shared acceptance requirements](acceptance-and-dependencies.md)

Source inventory at primary `9a952f8`. Limb reach lengths already use 0.1 mm;
the following physics paths still use micrometres. This inventory is remaining
work, not qualification evidence.

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

- Authenticated rounding, sign, domain, saturation and inverse laws.
- Negative coordinates, sub-unit heights, half-unit ties, extreme supported
  coordinates and nonfinite input refusal.
- Contact thresholds around rounding boundaries, zero/one-frame takes and
  nonuniform sample times; preserve or explicitly qualify the frame-rate model.
- Ballistic residuals, corrections and exported micrometre reports compared
  with a fixed corpus. Record expected precision changes before acceptance.
- Keep angular cap, acceleration and drift outputs unchanged by this migration.
- Current complete compiler/prover qualification and native overlay review.
