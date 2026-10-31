# Contributing

Read [CLAUDE.md](CLAUDE.md) first. The seven evidence positions are not open
to change through a pull request that adds a setting, a flag or a dossier
field to switch them off. A position changes only through new evidence, cited
in a review under `reviews/`.

## Rules

- Every rule carries `source:` back to a review section, or `judgment_call:`
  naming the position as this repo's.
- Confidence labels come from the closed set documented at the top of
  `RULES.md`. A source label outside the set goes in `source_label:`,
  verbatim, with a `judgment_call:` explaining the mapping.
- A rule that reads data lists the capabilities it needs in `requires:`. It
  never names a data source or a tool.
- Any change to rule content bumps the version on the first line of
  `RULES.md`.

Run `python tools/lint_rules.py` before opening a pull request. CI runs it on
every pull request and on every push to `main`.

## Data sources

Rules read data through capabilities, defined in
[capabilities.md](capabilities.md). Two providers ship with this repo:
`intervals-icu` (the intervals.icu MCP server) and `manual` (the athlete's
own report).

**The recommended path for another platform is to sync it into
intervals.icu.** intervals.icu imports from most device and training
platforms (e.g. Garmin Connect, Wahoo, Polar, Suunto, COROS). Once the data
is there, the `intervals-icu` provider covers it with no change to this repo.

**New providers live in forks.** This repository does not carry adapters for
other platforms. In a fork, a new provider:

1. is added under `providers:` on each capability it supplies, with the
   calls it makes;
2. is added to `PROVIDERS` in `tools/lint_rules.py`;
3. supplies only the capabilities whose `semantics:` its data actually
   meets.

**A metric with different semantics is a new capability, never a mapping
onto an existing one.** A device's sleep score is not `sleep_duration`. A
watch's VO2max estimate is not `vo2max`, which is a measured value. A
platform's readiness score is not any capability here, and no rule may gate
on it (`CLAUDE.md`, position 6). If the metric is worth having, add a new
capability with its own meaning and semantics. No existing rule reads a new
capability until a rule is written for it, with a source.

**Data ownership holds for every provider.** Values a provider owns are
fetched in the session that uses them and never written to a repo file,
the dossier included (`CLAUDE.md`, data ownership).

## Commits

Short, single-line conventional commits, e.g. `feat(rules): ...`,
`fix(lint): ...`, `docs(reviews): ...`.
