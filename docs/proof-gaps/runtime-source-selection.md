# Studio runtime source selection

The current-context viewport reduction ended without an object. Its source
closure included runtime declarations from both `Elisa-compiler` and the
historical `Elisa-compiler-m5-runtime-origin`. Duplicate std declarations and
dependent errors prevent attributing its later diagnostics to viewport
ownership. The log is `build/view-camera-reduction/actual-context.log`.
The Go bootstrap comparison failed while parsing current app syntax and
provides no evidence about the relevant Stage1 semantics.

Both Studio workers now include `build/generated/studio_runtime.elisa`.
The normal build-identity generation step writes that bridge from the exact
configured compiler's runtime source. Snapshot/check modes require the bridge
to match that selection and refuse any runtime source in the expanded closure
that resolves outside the selected compiler. Thus an `ELISA_STAGE1` override
selects declarations and the linked runtime together.

Generation and source snapshot creation pass with the matched compiler
`d2754a8e`. The closure record is
`build/view-camera-reduction/runtime-unified-inputs.json`. This establishes
source selection only: the complete app has not yet compiled or run with it.
Current UI/controller changes require a new immutable generation before
qualification. Regenerate identity/bridge files inside that generation so
absolute include paths refer to its copied compiler, then retain the expanded
closure and source/product manifests through compilation and linking.
