# Practice take

`practice_take` writes a copy of a real take with typical capture problems
added on purpose. Beginners can use it to see what Studio finds and fixes
before they open their own capture.

```
practice_take SOURCE.glb build/practice/NAME.glb [ANIMATION-INDEX]
```

Build it with the same Stage1 as the CLI:
`scripts/elisac_stage1.sh -emit exe -o practice_take src/practice/main.elisa`.

What it adds, on every arm and leg rotation channel of the chosen
animation (`src/io/practice_take.elisa`):
- a two-frame burst at 20% of the take;
- single-frame spikes at 55% and 80%;
- each one a ~40 degree nudge, renormalised.

Key counts and timing are unchanged. Channels with different key counts are
first aligned onto one grid, as Studio does at load. OUTPUT must be inside
a `build/` folder and differ from SOURCE; source takes are never
modified.

On the boxer jab (animation 9) the practice copy has 325 spikes, and the
default cleanup removes all of them. So it shows detection and the
automatic stack at work. To practise the find/fix/undo loop (W, 1-6,
Cmd-Z), turn a stack step off (D) and watch the findings return.
`test/practice_take.elisa` checks that every marked frame gains spikes,
frame counts stay, and the source document is unchanged.
