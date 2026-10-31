# ai-fitness-coaching

Evidence-checked training assistant for one athlete per copy, run as a
Claude Code skill. The rules layer was checked against systematic reviews and
meta-analyses, and holds the positions that survived — including several that
contradict standard coaching practice.

Not a coaching product. Copy the repo, describe yourself in `DOSSIER.md`, and
the rules for your disciplines and goal switch on.

Read [CLAUDE.md](CLAUDE.md) before proposing anything — it holds the seven
non-negotiable positions that the rest of the repo exists to enforce. They
hold in every copy: the dossier configures the athlete, never the evidence
stance.

## Setup

1. Connect the intervals.icu MCP server
   ([hhopke/intervals-icu-mcp](https://github.com/hhopke/intervals-icu-mcp)).
2. Run `/setup`. It builds `DOSSIER.md` from `DOSSIER.template.md` by
   interview, reads what intervals.icu already knows, and records only what
   it cannot know. Thresholds are confirmed, not stored. Empty is a valid
   answer; a guess is not. `/setup --section <name>` redoes one section.
3. Run `/training daily` or `/training weekly`. Every output opens with a
   data block naming the tool behind each value; weekly drafts are checked by
   a read-only reviewer before you see them.

## Coverage

**Covered.** Cycling, running and swimming, multisport load combination and
taper (reviews `01`, `03`); climbing and bouldering (`02`); resistance
training (`02`, `03`, `04`). Triathletes are reasonably served by review `01`.

Unevenly covered, stated so it is not mistaken for full coverage:
- Swimming carries one dedicated rule; the rest of its coverage is shared
  endurance rules. Review `01` covers more than `RULES.md` encodes.
- Interval prescription, progression and plateau logic is written for
  cycling and does not load for running or swimming.
- The goal-specific defaults exist for a longevity goal only. A performance
  goal gets the discipline rules and no goal-specific ones.

**Not covered.** Rowing, team sports, pure strength or powerlifting goals,
youth athletes. These get no rules, and the assistant says so rather than
filling the gap.

## Disclaimer

**Not medical advice.** This is a rules layer an athlete configures for
themselves, not individual guidance. It does not diagnose, and it defers to a clinician
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
| `.claude/commands/setup.md` | `/setup` — builds and updates `DOSSIER.md` |
| `.claude/agents/plan-reviewer.md` | Read-only reviewer for weekly drafts |
| `tools/lint_rules.py` | Rules and data-ownership lint; `tools/lint_allowlist.txt` holds cited literature figures. Runs in CI on pull requests |
| `reviews/` | Source evidence reviews, numbered `NN-topic.md` (`01`-`04`) |
| `HANDOFF.md` | Kickoff brief. Delete once the build is running |

## Data

Read via the intervals.icu MCP server; athlete id lives in `DOSSIER.md`. No
normalisation layer, metrics engine, or impulse-response model — intervals.icu
computes CTL, ATL, TSB and ramp server-side.

Strength and climbing sessions may not be in intervals.icu. Where a rule needs
absent data, say so. Absent data is absent, not zero.

**Data ownership.** intervals.icu owns load, activities, wellness,
thresholds and zones. They are fetched each session and never written to a
repo file, the dossier included; the dossier records only what the platform
cannot know, plus how each threshold was set. See `CLAUDE.md`.

Personal health information — the dossier and the rehab case — stays local.
Both paths are gitignored; tracked files refer to rules and tissues
generically.

## Status

Rules layer and workflow are written. `RULES.md` is at v0.5.1 — 74 rules, every
one carrying `source:` back to a review section or `judgment_call:` naming the
position as this repo's rather than a review finding.

v0.4 integrates `reviews/04-acsm-rt.md`, the ACSM 2026 resistance-training
position stand. Four strength rules were refined against it, and one
contradiction was resolved by splitting
`progress_effort_not_a_fixed_percentage` into `strength_progression_is_load`,
`hypertrophy_progression_is_volume_and_effort` and
`no_fixed_percentage_progression`. Details in `reviews/README.md`.

v0.5 generalises the repo to one athlete per copy. Disciplines, goal and
events moved from `CLAUDE.md` into the dossier; longevity defaults load on
`goal: longevity`, taper rules on `event_date`, and `goal_type_branch` asks
when no goal is declared.

Outstanding before first use:

- **Fill in `DOSSIER.md` by hand.** This is the blocker. Without it no
  discipline or goal rules load — only the nine always-on rules and
  `goal_type_branch` — and two empty fields each gate a HARD rule: bone
  stress injury history and the fuelling question. Empty is a valid answer,
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

Copyright (c) 2026 Heiko Kromminga. Split by content type:

- **Code and structure** — under the [MIT License](LICENSE):
  `.claude/skills/`, `.claude/commands/`, `.claude/agents/`, `tools/`,
  `.github/`, `.gitignore`, and the file and rule-schema layout.
- **Rules and documentation** — under
  [CC BY 4.0](LICENSE-docs) ([summary](https://creativecommons.org/licenses/by/4.0/)):
  `RULES.md`, `REHAB.md`, `CLAUDE.md`, this README, `DOSSIER.template.md`,
  `HANDOFF.md` and `reviews/`.

Quotations from cited works remain under their authors' terms and are not
relicensed. In particular, `reviews/04-acsm-rt.md` quotes Currier et al.,
Med Sci Sports Exerc 2026;58(4):851-872, which is licensed CC BY-NC-ND.
