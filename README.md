# ai-fitness-coaching

A training rules layer for Claude Code that holds the positions an evidence
check supports, not the ones coaching convention repeats. Every rule carries
its confidence label and a citation back to the review it came from. The
system reads your training data from intervals.icu, asks you for what the
platform cannot know, and answers two questions: what to train today, and how
this week looks against the rules. It is built for one athlete per copy —
you, configured through a local dossier that never leaves your machine.

> **Not medical advice.** This is a rules layer an athlete configures for
> themselves. It does not diagnose, and anything injury-related defers to a
> clinician.
>
> **Not affiliated with Anthropic.** An independent project. Claude Code is
> named only because it is the tool this runs in.
>
> **Your data stays private only if you keep it that way.** `DOSSIER.md` and
> `private/` hold personal health information and are gitignored. Never
> force-add them (`git add -f`). A fork of a public repository is public:
> fill in your dossier in a clone, or in a private copy, not in a public fork.

## Status

What has been checked:

- **Primary sources.** Every numeric figure under a HARD rule and every
  absence claim was checked against the original papers: 15 claims, 13 held,
  one attribution resolved, one failed and was corrected
  (`strength_dose_target`). No fabricated citation was found. Review 04 was
  extracted from the full text of its source.
- **Structure.** `tools/lint_rules.py` checks every rule's provenance,
  confidence label, activation tags, data requirements and version bump, and
  scans tracked files for personal platform data. CI runs it on every pull
  request and every push to `main`.

What has not:

- **The research pass itself.** Reviews 01-03 come from a single research
  pass by a language model. They have been spot-checked, not re-derived.
  DISCLOSURE and SOFT material is unchecked. See the verification status in
  [reviews/README.md](reviews/README.md) before treating any rule as settled.
- **Use.** No real training block has been completed with this system yet.
  There are no outcome claims, and none should be inferred.
- **Unbuilt.** Review-checkpoint logic — what counts as a flat response, and
  the measurement error of a CP/FTP test — does not exist. Rules that need it
  say so instead of improvising a threshold.

## What makes this different

Seven positions hold in every copy, whatever the dossier says. They are the
point of the project, and they will feel wrong if you come from standard
coaching material:

1. **ACWR never decides anything.** It may be shown. The ratio is
   mathematically coupled to its own inputs, and a ratio against random data
   performs as well.
2. **No fixed intensity split.** Not 80/20, not polarized. The meta-analyses
   disagree, so a pyramidal-leaning default is shown and never optimised
   toward.
3. **No weekly 10% rule.** The trial that tested it found no effect.
4. **No single load number.** Systemic, finger and upper-limb, and lower-limb
   structural load are tracked separately; adding them together hides a
   spike in one.
5. **No climbing progression threshold.** None has been established, and
   running's cap does not transfer to finger tissue.
6. **No injury prediction.** No score, model or wearable output is presented
   as validated, because none is.
7. **Confidence labels survive.** Every rule is CONSENSUS, CONTESTED,
   PRACTITIONER, or NO EVIDENCE, and the label travels with the rule into
   every output. Where evidence is split, the output shows the split.

What the system refuses to do:

- produce a readiness number, an injury-risk score, or an ACWR gate;
- invent a ramp rate where the literature has none;
- pick a winner between contested findings and present it as settled;
- fill missing data with an estimate — absent is absent, not zero;
- build a loading progression for an injury no clinician has assessed;
- write a platform value (threshold, load, wellness) into any file, or use
  one remembered from an earlier session.

Each output opens with a data block naming where every number came from.
Weekly plans pass through a read-only reviewer that checks them against the
active rules, the seven positions and the data sources before you see them.

## Quick start

You need Claude Code, an intervals.icu account, and the
[intervals.icu MCP server](https://github.com/hhopke/intervals-icu-mcp)
configured with your API key.

1. Clone this repository. Read the private-data note above before forking.
2. Connect the intervals.icu MCP server to Claude Code, following its README.
3. Open the repository in Claude Code.
4. Run `/setup`. It finds your athlete id, reads what intervals.icu already
   holds, and interviews you for what it cannot know: goal, events, injury
   history, where you log climbing and strength. Thresholds are shown for
   confirmation, not stored. Empty answers are fine; guesses are not.
5. Run `/training daily`. The output is a data block, a recommendation, the
   rule that bound it, and what could not be checked.

## Workflow

`/setup` once → `/training daily` most days → `/training weekly` to plan or
review → rehab handoff whenever an injury is in play.

| Command | What it does | Output |
| --- | --- | --- |
| `/setup` | Builds `DOSSIER.md` from the template by interview; re-running updates only what you change | Rules now active, rules still gated and what would unlock them, open threshold discrepancies |
| `/setup --section <name>` | Redoes one section, e.g. `events` or `thresholds` | Same summary |
| `/training daily` | What to train today, from recent load, sleep, finger-session spacing and any pain report | Data block, recommendation, binding rule with its label, checks not run |
| `/training weekly` | Plans or reviews a week: 28-day strength dose, per-axis load, ordering conflicts, intensity distribution | Data block, per-axis review, conflicts, absent data, reviewer findings |
| Rehab handoff | Not a command. Pain that meets a trigger, or an active case in `private/rehab-case.md`, hands both modes to `REHAB.md` | What is restricted, what is maintained, how rehab ends — never a timeline |

## Coverage

**Covered.** Cycling, running and swimming, combined multisport load, and
taper (reviews 01, 03); climbing and bouldering (02); resistance training
(02, 03, 04). Triathletes are reasonably served.

**Covered unevenly.**

- Swimming has one rule of its own; the rest is shared endurance rules.
- Interval prescription, progression and plateau logic is written for
  cycling only.
- Goal-specific defaults exist for a longevity goal. A performance goal gets
  the discipline rules and nothing goal-specific.

**Not covered.** Rowing, team sports, pure strength or powerlifting goals,
youth athletes. These get no rules, and the assistant says so rather than
filling the gap from general knowledge.

## Extending

Rules never name a data source. Each rule lists the capabilities it reads —
`activity_log`, `sport_thresholds`, `finger_sessions` and so on — and
[capabilities.md](capabilities.md) defines what each one means, its units,
how fresh it must be, and which provider supplies it. Two providers ship
here: `intervals-icu` and `manual` (your own answers, asked with fixed
prompts).

- **Another platform:** sync it into intervals.icu. Most device platforms
  import there, and then nothing here needs to change.
- **A new provider:** build it in a fork. This repository carries no
  adapters for other platforms.
- **A new metric:** if it means something different from an existing
  capability — a sleep score is not sleep duration, a watch's VO2max
  estimate is not a measured VO2max — it becomes a new capability, never a
  mapping onto an old one.

Rule changes need a source in `reviews/` or an explicit `judgment_call:`,
and must pass `python tools/lint_rules.py`. Conventions are in
[CONTRIBUTING.md](CONTRIBUTING.md); the project constitution is
[CLAUDE.md](CLAUDE.md).

## Staying up to date

[CHANGELOG.md](CHANGELOG.md) records every `RULES.md` version and names each
rule added, removed or changed, so a change in advice traces to a change in a
rule. Each version is also published as a
[GitHub release](https://github.com/hhopke/ai-fitness-coaching/releases),
tagged with the `RULES.md` version; the first is v0.7. To be notified, watch
the repository with Custom → Releases.

After pulling, run `/setup` again if `DOSSIER.template.md` changed. It adds
new fields and leaves your answers alone.

## License

[MIT](LICENSE). Quoted and cited third-party material in `reviews/` remains
under its original terms and is not relicensed.
