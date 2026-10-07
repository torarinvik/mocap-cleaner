# Generated Studio build cleanup prerequisite

The build input record now carries a generation schema, artifact kind and ID
derived from the unique `studio-build.*` directory. Packaging verifies that ID
against the input record's directory and executable digest. Each app bundle also
records its own `studio-package.*` ID, the source build ID, and executable
SHA-256 in `Contents/Resources/PACKAGE-GENERATION.json`. The sealed build input
record remains byte-for-byte intact in `BUILD-INPUTS.json`.

`StudioBuildGenerationPolicy` is a pure fail-closed prerequisite for a future
review flow. Cleanup eligibility requires a verified manifest/product and
filesystem identity, verified current/active/recovery protection facts, an
old unprotected generation beyond its retention period, and explicit
selection, review and confirmation. A caller may report `Identity.Matches`
only after binding the manifest ID to the directory basename and checking the
no-follow directory identity and sealed product digest. Missing activity or
protection inventory must remain unverified.

The policy and its nine proof laws compile to a nonempty O0 object with the
provenance-checked Stage1 product from compiler source `5b354650` (product
SHA-256 `89d1b2ea78f8fbfe675386d0d2b84767077bb1572e23dece46f30d9749d59ce4`,
runtime object SHA-256
`51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`). The
object is `build/build-generation-policy.lL6HHb/laws.o`. This is compile-only
source evidence; proof replay and native behavior are open.

The compiled policy source SHA-1 is
`913e2ed3a9f329c3929153a5edd385fa347f7304`; the law source SHA-1 is
`a6b9fd446f66f780737b31f612b6f64106f5bcb8`. Both match commit `c45541f`.

No generated-build inventory, active-generation lease, shared build/cleanup
lock, directory Trash receipt, or reviewed cleanup action exists yet. The
policy is not connected to mutation. Current products, active generations and
package `previous.app` recovery backups therefore remain protected by leaving
their directories in place. J04 and M7 cleanup acceptance remain open.
