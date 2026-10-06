# Module-qualified owned and borrowed returns

The fresh diagnostic compiler reports current provenance at HEAD `1f136742`.
Its source includes the ownership repair and temporary backend traces; this is
not qualification of a clean adopted compiler build.

Two independent compile-only reproductions were rerun into unique directories:

| Case | Directory | Compiler exit | Fresh object |
| --- | --- | --- | --- |
| `build/repro/storage-origin/minimal/owned-only.elisa` | `build/ownership-qualification.Ta6z2V` | 0 | nonempty `repro.o` |
| `build/repro/storage-origin/minimal/borrowed-only.elisa` | `build/ownership-qualification.FQHmwJ` | 1 | absent |

Each directory preserves `repro.log` and `exit.txt`. The borrowed case reports
that the view `text` cannot be used because a darray push of `doc` invalidated
its storage dependency. The owned case accepts the fresh array return.

This confirms that the repaired module-qualified return analysis distinguishes
the two cases. No executable test was run. Full application code generation,
runtime ownership behavior and clean toolchain adoption remain required.
