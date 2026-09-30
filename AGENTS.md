# Mocap cleaner conventions

- Everything is written in Elisa. The UI uses elisa-ui. The 3D viewport, pose evaluation, GLB round-trip and animation math come from Elisa-engine. The mocap track is developed in `../elisa-engine-mocap`, on branch `mocap-track`.
- Write roughly as much proof code as business logic. Every kernel lands with its contracts and a proof file in `proof/`.
- Proof-critical logic uses integer fixed point: weights in permille and lengths in 0.1 mm.
- Fix prover gaps in `../elisa-proof-mocap` (branch `mocap-cleaner-proofs`) and record them in `docs/proof-gaps.md`.
- Never modify source takes. Derived files go in `build/`.
