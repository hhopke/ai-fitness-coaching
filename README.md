# ai-fitness-coaching

Personal training assistant for a single athlete. Cycling, climbing and
bouldering, strength, and low-intensity running. Longevity-led, performance
secondary.

Not a product. It does not generalise, scale, or serve other athletes.

Read [CLAUDE.md](CLAUDE.md) before proposing anything — it holds the seven
non-negotiable positions that the rest of the repo exists to enforce.

## Disclaimer

**Not medical advice.** This is a personal rules layer for one athlete, not
guidance for anyone else. It does not diagnose, and it defers to a clinician
on anything injury-related.

**The evidence base is only partly verified.** Reviews `01`-`03` come from a
single research pass by a language model. They have been spot-checked, not
re-derived: every HARD-rule numeric and every absence claim was checked
against primary sources, and one figure failed and was corrected. DISCLOSURE
and SOFT material is unchecked. Review `04` was extracted from the full text
of its source. Read the verification status in
[reviews/README.md](reviews/README.md) before treating any rule as settled.

## Layout

| Path | Role |
| --- | --- |
| `CLAUDE.md` | Project constitution and non-negotiable positions |
| `DOSSIER.template.md` | Template for `DOSSIER.md` — copy it locally and fill it in |
| `DOSSIER.md` | Athlete-declared context — sole source for goal, injury history, training age, events. **Gitignored** |
| `RULES.md` | Rules layer, activation-tagged, cited back to `reviews/` |
| `REHAB.md` | Rehab mode — supersedes progression logic in `RULES.md` while active |
| `private/rehab-case.md` | Active rehab case; rehab state is read from it. **Gitignored** — format in `REHAB.md` |
| `.claude/skills/training/` | Workflow and output format — `daily` and `weekly` modes, invocable as `/training` |
| `reviews/` | Source evidence reviews, numbered `NN-topic.md` (`01`-`04`) |
| `HANDOFF.md` | Kickoff brief. Delete once the build is running |

## Data

Read via the intervals.icu MCP server; athlete id lives in `DOSSIER.md`. No
normalisation layer, metrics engine, or impulse-response model — intervals.icu
computes CTL, ATL, TSB and ramp server-side.

Strength and climbing sessions may not be in intervals.icu. Where a rule needs
absent data, say so. Absent data is absent, not zero.

Personal health information — the dossier and the rehab case — stays local.
Both paths are gitignored; tracked files refer to rules and tissues
generically.

## Status

Rules layer and workflow are written. `RULES.md` is at v0.4 — 73 rules, every
one carrying `source:` back to a review section or `judgment_call:` naming the
position as this repo's rather than a review finding.

v0.4 integrates `reviews/04-acsm-rt.md`, the ACSM 2026 resistance-training
position stand. Four strength rules were refined against it, and one
contradiction was resolved by splitting
`progress_effort_not_a_fixed_percentage` into `strength_progression_is_load`,
`hypertrophy_progression_is_volume_and_effort` and
`no_fixed_percentage_progression`. Details in `reviews/README.md`.

Outstanding before first use:

- **Fill in `DOSSIER.md` by hand.** This is the blocker. Roughly a third of the
  rules do not activate without it, and two empty fields each gate a HARD rule:
  bone stress injury history and the fuelling question. Empty is a valid answer,
  a guess is not.
- **Rehab state** is read from `private/rehab-case.md`. While a case is
  active, both `training` skill modes hand off to `REHAB.md`, and the seven
  rules tagged `NOT state:rehab` do not load.
- **Review-checkpoint logic is unbuilt.** `plateau_order_of_operations` owns the
  order of operations on a flat response; what counts as flat — review period,
  measurement error, how long a plateau must persist — belongs to checkpoint
  logic that does not exist yet. The skill states this rather than improvising
  a threshold.
- **Open items in `HANDOFF.md`** — two HARD-despite-CONTESTED rules to revisit,
  what to record manually for climbing load, and where strength gets logged.

## License

Split by content type:

- **Code and structure** — the skill workflow in `.claude/skills/`, repo
  configuration, and the file and rule-schema layout — under the
  [MIT License](LICENSE).
- **Rules and documentation** — `RULES.md`, `REHAB.md`, `CLAUDE.md`, this
  README, `DOSSIER.template.md`, `HANDOFF.md` and `reviews/` — under
  [CC BY 4.0](LICENSE-DOCS).

Quotations from cited works remain under their authors' terms. In particular,
`reviews/04-acsm-rt.md` quotes a CC BY-NC-ND source; those quotations are not
relicensed.
