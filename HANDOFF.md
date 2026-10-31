# HANDOFF — first Claude Code session

Delete this file once the build is running. It is a kickoff brief, not repo
documentation.

## Setup

```
mkdir training-assistant && cd training-assistant && git init
mkdir reviews
```

Drop in:

```
CLAUDE.md                    ready
RULES.md                     ready
REHAB.md                     ready
DOSSIER.template.md          rename to DOSSIER.md and fill in first
reviews/endurance.md         the sections 1 to 7 review
reviews/climbing.md          the climbing and resistance training review
```

Confirm the intervals.icu MCP server is connected before starting.

## Do this before the first session

Fill in DOSSIER.md by hand. It is the only source for goal, injury history,
training age, events and data source reliability, and roughly a third of the
rules do not activate without it. Two fields gate HARD rules and matter more
than the rest: bone stress injury history, and the fuelling question. Empty is
a valid answer; a guess is not.

## Build order

1. **Verify the rules load.** Before writing any workflow, have Claude Code
   read RULES.md and DOSSIER.md and report which rules are active, which are
   dormant, and which are dossier gated but unpopulated. This is a cheap check
   that the activation scheme actually works and that nothing is silently
   inert.

2. **Verify the data.** For each active rule, check whether the intervals.icu
   MCP can supply what it requires. Expect gaps around climbing load and
   strength sessions. Record the gaps rather than working around them.

3. **Write SKILL.md last.** The workflow depends on knowing what loads and
   what data exists. Writing it first means guessing at both.

## SKILL.md scope when you get there

Two modes, and they are different enough that conflating them produces a skill
that does neither well:

- **daily** — what should I do today, given current state. Reads recent load,
  wellness, and days since last hard finger session. Output is short.
- **weekly** — plan or review a week. Checks strength dose over a 28 day
  window, per axis load distribution, session ordering conflicts. Output is
  structured.

Both must check rehab state first and hand off to REHAB.md if active.

## Expect this failure mode

Every session will drift toward standard practice: ACWR gating, hardcoded
80/20, a weekly ramp cap, a single combined load number, a climbing
progression threshold. This is not Claude Code being careless, it is what the
training data contains. When it happens, point at the numbered positions in
CLAUDE.md rather than relitigating the evidence each time.

## Open items

- **Rule confidence review.** Two rules are typed HARD despite CONTESTED
  evidence: `run_single_session_spike_cap` and
  `bouldering_counts_asymmetrically`. Both are defensible, both are judgment
  calls rather than review findings. Revisit once the system has produced a
  few weeks of output.
- **Climbing load tracking.** No validated metric exists, so decide what to
  record manually. Session count, hard versus easy, and crimp heavy versus not
  is probably enough to run the finger spacing and stacking rules.
- **Strength logging.** If strength sessions are not in intervals.icu, the
  dose rule cannot be enforced automatically. Either log them as activities or
  accept self report and have the weekly mode ask.
