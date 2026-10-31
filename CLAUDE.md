# CLAUDE.md

Project constitution. Read this before proposing anything.

## What this is

A personal training assistant for one athlete. Disciplines: cycling (primary
endurance), bouldering and climbing (primary), strength (non negotiable),
running (minor, low intensity). Objective is longevity led, performance
secondary.

This is not a general coaching product. It does not need to generalise, scale,
or serve other athletes. Optimise for correctness and honesty over features.

## The point of this project

The training corpus you were trained on is saturated with conventions that the
evidence does not support. This repo exists because those conventions were
checked against systematic reviews and meta analyses, and many failed. The
value of this system is entirely in holding those positions consistently.

If a suggestion feels obviously right and standard, that is a reason to check
RULES.md, not a reason to proceed.

## Non negotiable positions

These will feel wrong. They are correct and they are the whole point.

1. **ACWR never gates a decision.** It may be displayed. It may not trigger,
   block, or modify a session. Mathematical coupling, no causal estimate, an
   acute to random ratio performs equivalently. Do not add ACWR thresholds.
2. **No hardcoded intensity distribution.** Not 80/20, not polarized. The meta
   analyses are split (Rosenblat 2019 pro polarized, Silva Oliveira 2024 null).
   Pyramidal leaning is a default, not a target to optimise toward.
3. **The weekly 10 percent rule is not evidence based.** GRONORUN found no
   effect. Do not implement it for running and do not port it to climbing.
4. **No single combined load number drives decisions.** Three axes, tracked
   separately: systemic, finger and upper limb mechanical, lower limb
   structural. Combining masks single discipline spikes.
5. **No climbing progression threshold exists.** Do not invent one. Do not
   import the running spike cap. Different tissue, different timescale, no
   evidence.
6. **No injury prediction.** No wearable output, no model, no score presented
   as validated. None exists for endurance athletes.
7. **Confidence labels survive everything.** CONSENSUS, CONTESTED and
   PRACTITIONER labels are inherited from the reviews. A rule that has lost
   its label is just an assertion. Never strip them when summarising,
   refactoring, or generating output.

## Contested stays contested

Where evidence is split, the system exposes the split and the moderating
variables. It does not pick a winner and present it as settled. This applies
to output shown to the athlete, not just to internal comments.

## Rehab mode is a state, not an exception

REHAB.md governs when active and supersedes progression logic in RULES.md. Its
constraints exist because rehab is where confident wrong advice does the most
damage and where no data signal catches the error. Do not soften them, do not
add a loading protocol, and do not let plan generation resume on a timer.

## Files

```
CLAUDE.md            this file
DOSSIER.md           athlete declared context, the only source for goal,
                     injury history, training age, events. Gitignored,
                     created locally from DOSSIER.template.md
RULES.md             rules layer, activation tagged
REHAB.md             rehab mode, governs when active
private/rehab-case.md
                     the active rehab case and rehab state. Gitignored
.claude/skills/training/SKILL.md
                     workflow and output format, invocable as a skill
reviews/
  01-endurance.md    sections 1 to 7, the original evidence review
  02-climbing.md     climbing, bouldering, resistance training review
  03-session-prescription.md
                     session-level prescription: intervals, strength session
                     content, progression logic
  04-acsm-rt.md      ACSM 2026 resistance training position stand,
                     single-source extraction
```

Personal health information (dossier contents, rehab case) never goes in a
tracked file. Reference files name rules and tissues generically; the case
itself lives in `private/`.

Reviews are numbered in the order they were produced. A new review takes the
next number and keeps its topic slug; numbers are never reused or reordered,
because `source:` fields in RULES.md cite the filename.

Keep the reviews in the repo. Rules cite section numbers back to them and a
rule whose provenance is unverifiable is not usable.

## Data

Read via the intervals.icu MCP server. Athlete id in DOSSIER.md.

Do not build a normalisation layer, a metrics engine, or an impulse response
model. intervals.icu computes CTL, ATL, TSB and ramp server side. Single
athlete, single source. The complexity is not earned.

Strength and climbing sessions may not be in intervals.icu. Where a rule needs
data that is absent, say so explicitly rather than inferring. Absent data is
absent, not zero.

## Boundary

Rules and judgment live in this repo. If anything moves into
hhopke/intervals-icu-mcp later, it is derived metrics only, never coaching
positions. An MCP server serves data and tools. Making it opinionated makes it
useless to everyone else.

## Style

Concise and technically precise. No encouragement, no motivational framing, no
athlete addressed prose in reference files. State uncertainty plainly rather
than hedging around it.
