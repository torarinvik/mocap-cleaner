# FBX topology and skin pose comparison

## Captured conversion

This comparison used `bladed_cross.fbx` (SHA-256 `4aac7f8dda4a03d9a452dcec450ced74e7057cdb807434eb7314b2d3ce28fec8`) and the successful Studio generation `build/studio-build.yOXPzH`. The captured Studio executable SHA-256 is `97ea9a61994205f488848d198df163c631fd9d24e562648455eacd74a0486585`; the `studio_fbx_to_glb.o` SHA-256 is `409a3c59043415f9ba04fd62271687e3461fac6c0d89cad05deb87726c2b8817`; and the linked ufbx object SHA-256 is `47a6e89d77f927c99e09d17500438ceb342ef8a0445840bee15ad96dc46d43a0`. The captured compiler and runtime product hashes are `36389f6b18268d4266bd68aacd813c703cd788956b611b9fad9964da11a2aa32` and `51365ba4a06e13e0af344b5e21790795e15f1b7fbba23c0b5b94b5a52b00ccee`.

The native Studio object driver and the FBX native dylib both converted at 30 Hz and emitted byte-identical GLBs (SHA-256 `2f4710772c0b082e41ab1f41cbea31b4fdff60fa54089b3168c4556e1145ee21`). The fixture contains one mesh, one skin, one animation, and 52 bones. Blender 5.2.2 imported both FBX and GLB independently. Bone names matched 52/52 at four sampled animation times; the worst bone-head position error was 1.34 micrometres.

## Topology count difference

The 11998-versus-12000 triangle difference is not caused by degenerate triangles. Blender's FBX import exposes 6014 vertices and 11998 triangles; its minimum triangle area is `1.2910120609e-7 m²`, with zero triangles at or below `1e-9 m²` and zero duplicate geometric triangles at `1e-7 m` position rounding. The ufbx parse used by the converter exposes 6014 vertices, 12000 faces/triangles, and 36000 indices. The GLB has 12000 triangles, no degenerate triangles at the same thresholds, and two duplicate geometric triangle excesses at `1e-7 m` rounding.

The two extra triangles in the ufbx/GLB path are opposite-winding copies of existing geometry: ufbx faces 5548/5522 use source vertex IDs `{1481,1482,1483}`, and faces 11070/11087 use `{3732,3734,3736}`. Blender's GLB import locates the two duplicate copies within 0.32 and 0.69 micrometres of the corresponding FBX-imported triangles. Thus the converter preserves two duplicate faces present in the ufbx mesh data; Blender's FBX importer presents 11998 triangles and no duplicates. These observations locate the count difference in the importers' treatment of duplicate faces. They do not establish why Blender omits those copies. The converter did not create degenerate triangles.

At a coarse 1 mm coordinate rounding, 11972 triangle keys are shared between Blender's FBX and GLB imports. The remaining key differences include triangulation/coordinate representation differences and the two duplicate faces, so this rounded triangle-key comparison is not a full topology equivalence proof.

## Skin deformation discrepancy

The initial fixed nearest-rest-vertex comparison reported a maximum deformation-delta error of 9.243 mm at normalized phase 0.25 (95th percentile 0.108 mm). This maximum is not evidence of ambiguous duplicate-vertex matching: the GLB corner map records source vertex 1988 for GLB vertex 9861, and Blender's imported FBX vertex indices match the ufbx source vertex indices for all 6014 vertices by normalized joint-weight comparison (zero mismatches above `1e-5` L1 error).

The converter keeps at most four joint influences per vertex and renormalizes the retained weights. Source vertex 1988 has a fifth `mixamorig:RightArm` influence of `0.0369800`, which the converter drops. At GLB vertex 9861, comparing the GLB animation against Blender's full five-weight FBX evaluation reproduces the 9.243 mm error. Re-evaluating the same FBX vertex with the exact converter top-four weights reduces that error to 0.00497 mm. Across the whole mesh, top-four-pruned source versus GLB deformation-delta errors have a maximum of 0.0104 mm at phase 0.25 and a 95th percentile of 0.00880 mm; the full-weight comparison retains a 9.243 mm maximum, so the maximum is explicitly reported rather than hidden by the percentile.

This isolates the large outlier to the converter's four-influence truncation for this vertex and fixture. It does not establish that truncation is harmless for other assets: another source vertex loses up to 11.50% normalized weight, and 3243 of 6014 source vertices have more than four influences. The top-four experiment is an attribution check, not a broad fidelity guarantee.

## Method and limits

Blender 5.2.2 evaluated the FBX and GLB Armature modifiers at five normalized clip phases. Bone poses were compared by matched bone names. Mesh deformation used a fixed rest correspondence; the refined check additionally used ufbx's exact source logical vertex ID for every exploded GLB corner and verified source joint-weight identity against Blender's FBX import. The top-four control applied the converter's exact four-largest-influences selection and renormalization to the Blender-imported FBX mesh.

The captured comparison artifacts are under `build/fbx-pose-check-bb274/`, including `topology-analysis.json`, `topology-compare.json`, `top4-skin-comparison.json`, and `exact-skin-weight-audit.json`. This is independent evidence for one FBX fixture and these captured binaries. It is not general FBX compatibility evidence, a complete topology equivalence proof, or Studio UI visual verification.
