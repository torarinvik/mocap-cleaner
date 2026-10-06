# Finding policy diagnostic compilation

The fresh diagnostic Stage1 at compiler HEAD `1f136742` reports current
provenance. It includes the uncommitted module-qualified ownership repair and
temporary backend owner tracing; these results do not qualify a clean compiler
release. All three compile-only commands returned zero and emitted fresh,
nonempty objects in unique directories:

| Input | Object |
| --- | --- |
| `proof/studio_issue_explanation_laws.elisa` | `build/finding-policy-compile.OiI4wr/explanation.o` |
| `proof/studio_issue_browser_laws.elisa` | `build/finding-browser-compile.OQgRsr/laws.o` |
| Existing `test/studio_issue_annotation.elisa` | `build/finding-intent-compile.adX5mK/fixture.o` |

Logs sit beside their objects. This accepts syntax and object generation for
the guarded exact frame conversion, navigation admission laws and typed intent
fixture. The fixture was not executed. Proof replay, full application code
generation and native input/accessibility behavior remain unqualified.
