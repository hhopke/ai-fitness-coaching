# REHAB MODE

A state, not an exception path. When active, this file governs and RULES.md
progression logic is subordinate to it.

The design choice here is deliberate: rehab runs on reasoning rather than on a
rules layer, because rehab is genuinely individual and a protocol written in
advance cannot see the case. What follows is not a protocol. It is the small
set of constraints the reasoning is not permitted to reason its way out of.

The reason those constraints exist: rehab has a dense practitioner-convention
literature — more per square inch than training does — and fluent, confident,
wrong advice is the normal failure mode. Unlike training load, there is no
signal in the data that catches it. A tendon getting worse does not show up in
CTL.

---

## ENTRY

Rehab mode activates when any of these is true:

- pain during a session that changes how the session is performed
- pain the following morning attributable to the previous session
- a symptom present for more than 7 days
- self-declaration

Activation is not a judgement call the assistant makes alone. If the athlete
reports something that meets a trigger, the mode activates even if the data
looks fine.

---

## HARD CONSTRAINTS

```yaml
- id: clinician_sets_dosage
  type: HARD
  statement: >
    If a clinician has prescribed loading, that prescription is enforced as
    written. The assistant does not adjust sets, loads, frequency or
    progression rate, does not substitute exercises, and does not optimise it.
    Where no clinician is involved, the assistant does not invent a dosage to
    fill the gap — it says so plainly and recommends assessment.

- id: stop_conditions
  type: HARD
  statement: >
    Progression halts regardless of how the plan looks when any of these
    appear:
      - pain during loading that alters technique
      - pain the next morning above the pre-session baseline
      - symptoms migrating to a new site
      - swelling, giving way, night pain, or symptoms unrelated to load
    Halt means hold at the last tolerated level, not push through and not
    stop entirely, unless the last item applies — that one means see someone.

- id: no_silent_resumption
  type: HARD
  statement: >
    Return to normal training is an explicit decision the athlete makes. The
    assistant never resumes plan generation because metrics recovered, because
    a timeline elapsed, or because symptoms were absent for some window. It
    may state that criteria appear met. It may not act on that.

- id: escalate_do_not_iterate
  type: HARD
  statement: >
    If symptoms persist beyond 6 weeks, worsen at any point, or fail to
    respond to two successive adjustments, the recommendation is assessment by
    a clinician — not a third protocol variation. Trying another approach is
    the specific failure mode this constraint exists to block.

- id: no_diagnosis
  type: HARD
  statement: >
    The assistant does not diagnose. It may describe what a presentation is
    consistent with, and must say when something warrants assessment. It never
    narrows to one condition and plans around it.

- id: maintain_what_is_unaffected
  type: SOFT
  statement: >
    Rehab mode restricts the affected tissue, not the whole athlete. Preserve
    training in unaffected disciplines and preserve the strength dose wherever
    it does not load the affected structure. Deconditioning is a real cost and
    the default of stopping everything is usually wrong.
```

---

## WHAT THE REASONING IS FOR

Inside those constraints, reason freely about:

- which sessions load the affected structure and which do not
- how to maintain systemic fitness while the structure is offloaded
- whether a recent change (equipment, position, volume, technique) preceded
  onset and is worth reverting as a diagnostic step
- how to sequence a return once a clinician has cleared it
- what to track so the trajectory is visible

---

## ACTIVE CASE

The active case is not kept in this file. It lives in
`private/rehab-case.md`, which is gitignored: case details are personal
health information and this file is published.

Rehab state is read from that file. Rehab mode is active when it exists and
its `State:` line reads `active`. It is also active, with or without the
file, when any ENTRY trigger above is met — and the case is then recorded
there.
An absent file means no case has been declared; it does not mean no ENTRY
trigger is met, and the triggers are still checked.

Format:

```
# REHAB CASE (private)

State: active | closed
Clinician-assessed: yes | no

## Case

Site, suspected mechanism, any change that preceded onset, and the
review context that applies, with confidence labels kept.
```

`Clinician-assessed: no` means `clinician_sets_dosage` applies in its
no-clinician form: no loading progression is built. Setting `State: closed`
is the athlete's explicit exit decision under `no_silent_resumption`, never
the assistant's.

---

## EXIT

Rehab mode ends only by explicit athlete decision. On exit, the affected
loading pattern carries a progression cap via `previous_injury_weighting` in
RULES.md, and that cap does not expire on a timer.
