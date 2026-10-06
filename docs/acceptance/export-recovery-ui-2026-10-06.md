# Export recovery UI qualification

Date: 2026-10-06

The recovery UI source and policy frontend-checked with the current Stage1 compiler (`720896f4034eca0b79235442e818993ea5fe2424`) during a compile-only Studio build:

```sh
STUDIO_SKIP_CHECKS=1 bash scripts/build_studio.sh
```

The frontend accepted the source, but backend code generation declined 25 function bodies and emitted no Studio object. One decline is `publish_export_recovery_accessibility@57 (expression statement)`, at the `UiCore::accessibility_with_metadata(...)` call in `src/studio/app/app_accessibility_dialogs.elisa`. The full output is preserved in `build/recovery-accessibility-after-copy.log`. A compile-only include-context reproduction is in `build/repro/studio-app-context.elisa`; it includes `src/studio/app/app.elisa` and reproduces the decline. Smaller repros for the action enum/index and a reduced metadata call compile, so the failure remains specific to the integrated include context.

This evidence does not qualify an emitted application binary, runtime behavior, native accessibility exposure, or VoiceOver behavior. The recovery UI policy proof laws have not been independently rerun for this slice while the repository proof gate is active. Do not treat this record as acceptance of the backend decline.

## Frame argument repair

The call's frame argument originally passed a `StudioPanels::Box` directly to `UiCore::accessibility_with_metadata`, whose frame parameter is `UiCore::Rect`. Frontend checking accepted this structural shape, but the backend declined the containing function at the call expression. An include-context compile with that single frame expression replaced by a `UiCore::Rect(...)` constructor removed the accessibility function from the declined-function list. The source now converts the Box fields explicitly.

A fresh compile-only Studio build on the same Stage1 then reported 24 backend-declined bodies and no `publish_export_recovery_accessibility` decline. The remaining full-unit declines still prevent emitting a Studio object, so this does not qualify the application binary or runtime accessibility behavior. The prior include-context and argument-elimination repros remain in `build/repro/accessibility_variants/`.
