---
name: training
description: Training assistant for the one athlete declared in DOSSIER.md — disciplines and goal come from the dossier; rules exist for cycling, running, swimming, climbing and bouldering, and strength. Runs two separate modes. daily answers what to train today from recent load, wellness, and finger-session spacing. weekly plans or reviews a week — 28-day strength dose, per-axis load distribution, session ordering conflicts. Both check rehab state first and hand off to REHAB.md when it is active. Use when asked what to train today, to plan or review a training week, or to apply the rules layer in RULES.md.
---

# SKILL

Workflow and output format. Two modes, run separately. Read `CLAUDE.md` first;
this file describes how the rules layer is applied, not what it says.

Both modes are read-and-report. Neither writes to intervals.icu, and neither
resumes plan generation on its own.

Every file named here lives at the repo root — `CLAUDE.md`, `RULES.md`,
`REHAB.md`, `DOSSIER.md`, `private/rehab-case.md`, `reviews/` — not beside
this file. Read them there. `DOSSIER.md` and `private/` are gitignored and
exist only locally.
Invoke as `training daily` or `training weekly`; with no mode given, ask which
rather than guessing, because the two answer different questions.

## Modes

| Mode | Question | Output |
| --- | --- | --- |
| `daily` | What should I do today, given current state | Short — a recommendation, its binding constraint, and what was missing |
| `weekly` | Plan or review a week | Structured — per-axis, with the checks below run in order |

They are not interchangeable. Daily reads state and answers one question.
Weekly runs the dose and distribution checks that only make sense over a
window. Do not answer a weekly question by running daily seven times.

---

## PREFLIGHT

Runs before either mode. All steps, every time, in this order.

### 1. Rehab state

Read `REHAB.md`, then `private/rehab-case.md`. Rehab mode is active if that
file exists with `State: active`, if any ENTRY trigger in `REHAB.md` is met,
or if the athlete has declared it. A missing file means no case is declared,
not that the triggers were checked — check them.

**If active, `REHAB.md` governs and this file's flows do not run.** Hand off:
report the case from `private/rehab-case.md` (or, if a trigger fired and no
case is recorded yet, say so and ask for the details), what is restricted,
what is preserved under
`maintain_what_is_unaffected`, and what the exit condition is. Do not build a
loading progression for the affected structure, do not propose a timeline, and
do not state that criteria appear met as though that were a decision —
`no_silent_resumption` makes return an explicit athlete choice.

Rules tagged `NOT state:rehab` do not load. That is a load-time gate, not a
judgement to make in the moment: do not read them, do not reason from them, and
do not reconstruct their content from memory.

Rehab is a state, not an error. Both modes still have useful things to say
about unaffected disciplines — say those, inside `REHAB.md`'s constraints.

### 2. Dossier

Read `DOSSIER.md`. Establish the declared disciplines (`discipline:` rules)
and which `dossier:` rules activate. `DOSSIER.template.md` lists what each
field activates. If the file is missing, say so: it is created locally from
the template, and every `discipline:` and `dossier:` rule is inert until it
exists. The rules that load for every athlete still apply.

If `goal` is empty, `goal_type_branch` loads: ask for the goal before any
recommendation that depends on it, and do not default to longevity.

A discipline the athlete trains but the dossier does not list, or one outside
the covered set, gets no rules. Say so; do not supply them from general
knowledge.

Report any dossier-gated field that is empty **and gates a HARD rule** —
currently `bsi_history` (`bsi_history_pathway`) and `fuelling_flag`
(`underfuelling_check`). An empty field is not a negative finding. It means the
rule is inert, and the mode says so rather than proceeding as though the rule
had been checked and passed.

Empty is a valid answer to the dossier. A guess is not, and neither mode fills
a gap by inferring from training data.

### 3. Data availability

Establish, per axis, what data exists for this run:

| Axis | Source | Expect |
| --- | --- | --- |
| Systemic / cardiometabolic | intervals.icu | Present. Power-based cycling load is the most reliable — `bike_load_is_the_reliable_one` |
| Finger / upper-limb mechanical | Not in intervals.icu | Absent. Ask. |
| Lower-limb tendon / structural | Partial — cycling and running present, strength usually not | Ask for the strength part |

An axis no declared discipline feeds is not applicable for this athlete —
report it as such, not as zero load (`separate_load_axes`).

Fetch every platform value this run uses, in this run, with `athlete_id`
from the dossier passed explicitly on every call (`CLAUDE.md`, data
ownership). Tool names are as registered by the intervals.icu MCP server;
the client adds its own prefix. If the tools are unavailable, say the server
is not connected and stop — do not continue from memory.

| Value | Tool |
| --- | --- |
| CTL, ATL, TSB, ramp | `icu_get_fitness_summary`, or `icu_get_fitness_chart` for a window |
| Activities and anything derived from them (volumes, longest run, days since a session) | `icu_get_activities_by_date` |
| Wellness — HRV, sleep, resting HR, subjective scores | `icu_get_wellness_data` |
| Thresholds and zones | `icu_get_sport_settings` only — never the profile's FTP fields, never the curve tools |

Values from memory, conversation history, earlier sessions or project
context are never used, even when they look current. A value the dossier
appears to hold for a platform-owned quantity is not used either; report it
as a data-ownership violation.

Do not recompute CTL, ATL, TSB or ramp, do not build a normalisation layer,
and do not fit an impulse-response model. Single athlete, single source; the
complexity is not earned.

Where a rule needs data that is absent, **say so and ask**. Do not infer
climbing load from a gap in the calendar, do not treat an unlogged strength
session as zero minutes, and do not substitute a proxy. Absent data is absent,
not zero.

### 4. Provenance block

Every output of either mode opens with a data block. **An output without
it is invalid** and is not shown; build the block and then the output.

The block lists every value the output uses, the tool that supplied it, and
when it was fetched. Data the platform does not hold is listed too, as
`self-reported` (with what the athlete said, this session) or `absent`.
Absent is absent, not zero: an absent row is never filled with an estimate.

```
DATA — fetched <date> <time> <timezone>
value                          source                                     fetched
CTL / ATL / TSB / ramp         icu_get_fitness_summary                    <time>
activities <oldest>..<newest>  icu_get_activities_by_date                 <time>
<sport> threshold and zones    icu_get_sport_settings                     <time>
HRV, sleep, last 7 days        icu_get_wellness_data                      <time>
hard finger sessions           self-reported: "<athlete's words>"         this session
climbing load                  absent — not in intervals.icu              —
strength minutes, 28 days      absent — not logged, not asked yet         —
```

The block shows the values themselves inline where the output relies on
them. A number that appears in the output and not in the block is a
violation.

---

## MODE: daily

### Reads

1. Last 7-10 days of activities, plus CTL / ATL / TSB / ramp as reported.
2. Wellness where logged — sleep, HRV, subjective. `sleep_as_modifier` is a
   load-reduction signal, not a rest-day trigger on its own.
3. If climbing is declared: **days since the last hard finger session**,
   counting bouldering and
   hangboard as one category. Not in intervals.icu. Ask, and if the answer is
   unknown, say the finger-spacing check could not run rather than assuming it
   passed.
4. Pain or symptom report. Any positive answer routes to preflight step 1 —
   `climbing_in_pain_flag` makes climbing in pain a stop condition, not a
   tolerance to manage.

### Checks

In order. Stop conditions first, because a stop condition makes the rest moot.
A check whose rule is not active for this dossier — the finger checks without
climbing, for example — is reported as not applicable, which is distinct from
passed and from not run.

1. `climbing_in_pain_flag` — stop condition.
2. `underfuelling_check` — fires before any load increase, if the dossier field
   is populated. If it is empty, the check did not run; say that.
3. `finger_session_spacing` — at least 48 h between hard finger sessions.
4. `session_ordering` and `strength_cycling_same_day_order` — what today can
   follow, and what order today's sessions take if two are stacked.
5. `hangboard_displaces_never_adds` — if finger work is proposed, it displaces
   climbing finger volume rather than adding to it.
6. `bouldering_counts_asymmetrically` — bouldering counts toward finger and
   pulling load and toward nothing else.

### Output

Short. The provenance block, then three parts, no preamble. No reviewer
runs in daily mode (cost and latency), so the block is the only check that
every number has a source — it is mandatory.

- **Recommendation** — what to do today, or the choice between two options
  where a rule is SOFT and the call is genuinely the athlete's.
- **Binding constraint** — the one rule that determined it, named, with its
  confidence label. If nothing binds, say the day is unconstrained.
- **Not checked** — every check that could not run for want of data, named.

No encouragement, no motivational framing. If the honest answer is "nothing
here constrains today, do what you planned", that is the output.

---

## MODE: weekly

### Reads

Everything daily reads, plus:

1. A 28-day window of structured strength minutes. Usually not in
   intervals.icu — ask. `strength_dose_target` cannot be enforced on absent
   data, and an unlogged session is not a zero.
2. Session distribution across the three axes for the week under review.
3. Planned or completed sessions with their days, for ordering checks.

### Checks

Run all six. Report each, including the ones that pass and, as not
applicable, the ones whose rules are not active for this dossier.

1. **Strength dose, 28-day window.** `strength_dose_target` — operating band
   60-120 min/week; flag any 28-day window averaging under 60. Note that the
   60 floor is this repo's enforcement choice, not a review number: the rule
   carries a `judgment_call:` field saying so.
2. **Per-axis load distribution.** `separate_load_axes` — report the three axes
   separately. A combined figure may be shown for trend context only and must
   be labeled systemic-only. It never drives the recommendation.
3. **Bouldering accounting.** `bouldering_counts_asymmetrically` names two
   failure modes and requires both to be checked every week: over-loading
   (hangboard or heavy pulling stacked on hard bouldering) and under-prescribing
   (assuming climbing covers the upper body, leaving shoulder girdle, push,
   and posterior chain untrained).
4. **Ordering conflicts.** `session_ordering`, `finger_session_spacing`,
   `strength_cycling_same_day_order`. The last one resolves same-day order by
   which adaptation the current block protects; if the block phase is not
   established, ask rather than assigning an order.
5. **Intensity distribution**, for any endurance discipline. `tid_flexible` —
   pyramidal-leaning default, ~75-80% below LT1. Display it. Do not optimise toward it and do not report
   drift from it as an error; POL vs PYR meta-analyses are split.
6. **Interval and progression rules**, where a cycling quality session is in
   the week — `two_quality_sessions_default`, `anchor_short_intervals_to_power`,
   `sweet_spot_is_time_efficiency`. `two_quality_sessions_default` is gated
   `NOT state:rehab`; the other two are not.

### Review

After drafting and before output, the draft is reviewed by the
`plan-reviewer` agent (`.claude/agents/plan-reviewer.md`), spawned with fresh
context. It is read-only and has no MCP access, so it judges only what it is
handed. Pass it, verbatim:

1. the draft, including its provenance block;
2. the raw output of every tool call the block cites — not a summary;
3. every self-reported statement the block cites, in the athlete's words;
4. rehab state and the declared disciplines and goal, as read in preflight.

It reads `CLAUDE.md`, `RULES.md` and `DOSSIER.md` itself and checks the draft
against (a) the rules active for this dossier, (b) the seven `CLAUDE.md`
evidence positions, and (c) data ownership — every number traceable to a
tool output from this session or a self-report from this session. It returns
violations by rule id.

Revise the draft to resolve each violation, then run the reviewer once more
on the revision. Anything still unresolved after that goes into the output
under **Reviewer findings**, verbatim, with the rule id. Unresolved
violations are shown to the athlete, never hidden or softened.

### Output

Structured. The provenance block, then one block per axis, then the
cross-axis checks, then:

- **Dose** — 28-day strength average against the band, or the statement that
  the window is incomplete and by how much.
- **Conflicts** — ordering problems found, each naming the rule.
- **Absent** — every check that did not run, and what would let it run.
- **Displayed, not deciding** — ACWR if surfaced at all, the systemic-only
  combined figure if shown, and any trend the athlete asked to see.
- **Reviewer findings** — violations the reviewer reported that the revision
  did not resolve, or "none".

---

## What neither mode decides

These are boundaries, not omissions. Crossing one is the failure mode this
repo exists to prevent.

**Flat response.** Weekly mode does not define what counts as a flat response
over a review period. `plateau_order_of_operations` owns the order of
operations; its `reconciles_with:` field assigns the definition of a review
period, of typical measurement error for this athlete's CP/FTP protocol, and of
how long a plateau must persist, to review-checkpoint logic **which is not
built**. If weekly mode reaches a point where it needs that definition, it
states that the checkpoint logic is unbuilt and stops. It does not improvise a
threshold, and it does not substitute a number from a rule that was scoped to a
different question.

**Non-response.** Neither mode labels the athlete a non-responder.
`non_response_is_dose_dependent` makes that conditional on dose escalation
first, and dose escalation is a plan decision, not a report finding.

**Injury risk.** Neither mode produces an injury-risk score, a readiness
number, or a prediction. No validated model exists for endurance athletes.
ACWR may be displayed and may not gate, trigger, or modify anything.

**Progression rate.** Neither mode invents a ramp rate for intervals or for
climbing. `no_session_level_interval_ramp_rate` and
`no_climbing_ramp_threshold` are both HARD, and both say the literature is
silent rather than negative.

**Rehab dosage.** Neither mode builds a loading progression while rehab is
active, or once it has closed for the affected pattern beyond what
`previous_injury_weighting` permits.

---

## Output contract

Applies to both modes.

1. **Confidence labels survive.** CONSENSUS, CONTESTED and PRACTITIONER travel
   with the rule into the output. A rule quoted without its label is an
   assertion, and stripping labels when summarising is the specific failure
   this constraint blocks.
2. **Contested stays contested.** Where the evidence is split, expose the split
   and the moderating variable. Do not pick a winner and present it as settled.
   This applies to athlete-facing output, not only to internal reasoning.
3. **Name the rule.** Every constraint reported cites the rule id that produced
   it, so the position is checkable against `RULES.md` and from there against
   `reviews/`.
4. **Absent is stated, never filled.** A check that did not run is reported as
   not run. It is never silently dropped and never reported as passing.
5. **Every number has a source.** The provenance block opens the output, and
   every number in the output traces to a tool call in this session or a
   self-report in this session. No value from memory or an earlier session.
6. **Judgment calls are marked.** Where a rule carries a `judgment_call:`
   field, output derived from it says the position is this repo's, not a review
   finding.
7. **Style.** Concise and technically precise. No encouragement, no
   motivational framing. State uncertainty plainly rather than hedging around
   it.

## Expected drift

Every session drifts toward standard practice: ACWR gating, hardcoded 80/20, a
weekly ramp cap, a single combined load number, a climbing progression
threshold, sweet spot as a distinct stimulus, time near VO2max as a dose
achieved. This is not carelessness; it is what the training corpus contains.
When it happens, point at the numbered positions in `CLAUDE.md` and the rule
id, rather than relitigating the evidence.
