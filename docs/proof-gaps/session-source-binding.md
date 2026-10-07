# Session source binding boundary

## Evidence and current limitation

V4 `SessionState::SourceIdentity` stores two rolling residues, animation index,
frame count and node count. `StudioModel::fingerprint` computes residues over
the source bytes, and `StudioSessionSourcePolicy::compare` checks equality of
the five stored fields. Its contracts establish field equality only.

The residues have finite domains; different byte sequences can share them.
Neither residue equality nor equal rig dimensions establishes exact source
bytes, semantic bone correspondence or safe ownership of a stored correction
index. This is a source-binding design gap, not a request to weaken the prover
or to infer an unstated equality theorem from a successfully compiled law.

## Required work

- Add explicit v4 matching-metadata restore review. Cancellation and Open as
  new take retain the current document until ordinary replacement confirmation.
- The next schema records versioned content digest and byte count with its
  declared collision assumption, animation selection and semantic rig binding.
- Resolve correction nodes through validated semantic rig identities; refuse
  ambiguous/missing mappings and expose unmapped repairs before confirmation.
- Direct retained-byte comparison may establish exact equality when available.
  Digest comparison must not be described as mathematical collision freedom.
- Qualify reordered/equal-count rigs, missing originals, changed animations,
  unsupported digest versions, malformed identities and session migration.

The Locate workflow is being integrated. No native or authenticated proof
acceptance is established by this record. See the M1 roadmap for exit gates.
