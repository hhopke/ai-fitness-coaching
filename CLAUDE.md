# CLAUDE.md

Project constitution. Read this before proposing anything.

## What this is

A training assistant for one athlete per copy of this repo. The athlete is
declared in DOSSIER.md, created locally from DOSSIER.template.md: disciplines,
goal, events, injury history. Nothing in a tracked file describes a particular
athlete.

Covered: cycling, running, swimming and their multisport combination,
including taper (reviews 01, 03); climbing and bouldering; resistance training
(reviews 02, 03, 04). Not covered: rowing, team sports, pure strength or
powerlifting goals, youth athletes. A discipline with no rules gets no rules;
do not fill the gap from general knowledge.

This is not a coaching product. It serves one athlete per copy and does not
need to scale. Optimise for correctness and honesty over features.

**Generalising configures the athlete, never the evidence stance.** The seven
positions below are non-negotiable in every copy, whatever the dossier says.
There are no toggles for them: no dossier field, flag or setting switches one
off, and none may be added. Rules carrying `judgment_call:` keep that field
visible in every copy, so a system decision is never read as a review finding.

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
DOSSIER.template.md  setup guide: each field states which rules it activates
RULES.md             rules layer, activation tagged
capabilities.md      contract between rules and data: each capability a
                     rule may require, and the provider that supplies it
CONTRIBUTING.md      rule, provider and capability conventions
REHAB.md             rehab mode, governs when active
private/rehab-case.md
                     the active rehab case and rehab state. Gitignored
.claude/skills/training/SKILL.md
                     workflow and output format, invocable as a skill
.claude/commands/setup.md
                     /setup: builds DOSSIER.md from the template
.claude/agents/plan-reviewer.md
                     read-only reviewer for weekly-mode drafts
tools/lint_rules.py  rules and data-ownership lint, run in CI on PRs
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

Read via the intervals.icu MCP server and the athlete's own report, through
the capabilities in capabilities.md. Rules name capabilities in `requires:`,
never tools. Athlete id in DOSSIER.md.

Do not build a normalisation layer, a metrics engine, or an impulse response
model. intervals.icu computes CTL, ATL, TSB and ramp server side. Single
athlete, single source. The complexity is not earned.

Strength and climbing sessions may not be in intervals.icu. Where a rule needs
data that is absent, say so explicitly rather than inferring. Absent data is
absent, not zero.

## Data ownership

Separate from the evidence positions above, and binding on every file and
every output.

1. **Single source per value.** Platform-owned values are never written to
   DOSSIER.md, DOSSIER.template.md, SKILL.md, RULES.md or any other repo
   file. Platform-owned means: load metrics (CTL, ATL, TSB, ramp);
   activities and figures derived from them (e.g. longest run in 30 days);
   wellness (HRV, sleep, resting HR); thresholds and zones (FTP, CP, LTHR,
   max HR, pace and CSS thresholds); and profile values the platform holds
   (date of birth, sex, weight).
2. **Thresholds and zones come from `icu_get_sport_settings` only.** Never
   from the curve tools, and never from the threshold fields in
   `icu_get_athlete_profile`. The curve tools' zone blocks were built from
   hardcoded percentage tables rather than the athlete's configuration and
   were removed for that reason (intervals-icu-mcp CHANGELOG, curve-tool zone
   removal).
3. **The dossier stores only what the platform cannot know**, plus metadata
   about platform values: which test set a threshold, its date, its
   protocol. Never the value itself.
4. **Exception: `athlete_id` is stored in the dossier.** Every MCP call
   passes it explicitly, so a copy is pinned to its athlete rather than to
   whichever athlete the server is configured with by default; an account
   that coaches or follows others reaches several. `icu_list_athletes` can
   help find the id during `/setup`; it never chooses one.
5. **Values from memory, conversation history, prior sessions or chat
   project context are never used for decisions.** Every value an output
   relies on is fetched in the session that produces it, and the output says
   which tool supplied it.

## Validation

Run `python tools/lint_rules.py` after any change to RULES.md,
DOSSIER.template.md or tracked prose. It checks rule structure, activation
tags against the template, confidence labels, `requires:` against
capabilities.md, the version bump, and the data ownership rule. CI runs it on every pull request. A literature figure that
trips the ownership scan goes in `tools/lint_allowlist.txt` with its citation;
a platform value is removed, never allowlisted.

## Boundary

Rules and judgment live in this repo. If anything moves into
hhopke/intervals-icu-mcp later, it is derived metrics only, never coaching
positions. An MCP server serves data and tools. Making it opinionated makes it
useless to everyone else.

## Style

Concise and technically precise. No encouragement, no motivational framing, no
athlete addressed prose in reference files. State uncertainty plainly rather
than hedging around it.
