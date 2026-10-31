# CAPABILITIES

The contract between rules and data sources. A rule never names a data
source or a tool: it lists the capabilities it needs in `requires:`. This
file defines each capability — what it means, its units and semantics, how
fresh it must be — and which provider supplies it.

Two providers:

- **`intervals-icu`** — the intervals.icu MCP server
  (hhopke/intervals-icu-mcp). Tool names as registered by the server; the
  client adds its own prefix. Every call passes `athlete_id` from the
  dossier. Everything it supplies is platform-owned (`CLAUDE.md`, data
  ownership): fetched in the session that uses it, never written down.
- **`manual`** — the athlete's own report, asked in the session that uses
  it, with the prompts in [Manual provider](#manual-provider). Self-reports
  are not stored either: the dossier is static context, not a log.

## Contract

1. **Semantics are fixed.** A capability means exactly what its entry says.
   A source whose metric means something different — a different
   measurement, a different scale, a different definition — gets a new
   capability. It is never mapped onto an existing one, however close it
   looks.
2. **No provider, no value.** A capability that no provider supplies in this
   run is absent. Absent is reported as absent, never estimated, never zero,
   and never substituted from another capability.
3. **Freshness is a requirement.** A value older than its capability's
   freshness requirement is absent for this run.
4. **Provenance names the capability.** Every value in an output is listed
   in the provenance block as capability, provider, and fetch time (or "this
   session" for a self-report, with the athlete's words).
5. **Where two providers are listed**, they are alternatives with the same
   semantics, not a blend: `intervals-icu` covers what is logged there;
   `manual` covers what is not. The provenance block lists each part with its
   own provider.
6. **`providers: {}`** marks a capability a rule needs and nothing currently
   supplies. Rules requiring it report the need as unmet. Listing it here
   keeps the gap visible instead of letting a nearby metric stand in.

```yaml
- id: fitness_load
  meaning: Server-computed training-load state — CTL, ATL, TSB, ramp rate.
  semantics: >
    intervals.icu's own impulse-response values, built from per-activity
    training load. Dimensionless load units, as of the fetch date. Not
    recomputed, not normalised, not combined with any other axis
    (separate_load_axes). ACWR derived from these may be displayed and never
    gates (acwr_never_gates).
  freshness: as of today, fetched this session
  providers:
    intervals-icu: [icu_get_fitness_summary, icu_get_fitness_chart]

- id: activity_log
  meaning: Completed sessions recorded on the platform over a date window.
  semantics: >
    Per session: date, sport type, moving time (s), distance (m), training
    load, average and normalised power (W), average HR (bpm), average
    cadence. As recorded; a session not recorded is absent from the log, not
    a zero. Derived figures (weekly volume, longest run in 30 days, days
    since a session, gaps) are computed from this window in the session.
  freshness: window ending today, covering the rule's lookback, fetched this session
  providers:
    intervals-icu: [icu_get_activities_by_date, icu_get_recent_activities]

- id: time_in_zone
  meaning: Time per configured intensity zone, per activity.
  semantics: >
    Seconds in each zone of the athlete's configured zone model (power, HR
    or pace), from per-activity histograms binned against the zones in
    sport_thresholds. The zones are the athlete's configuration; they carry
    no physiological meaning beyond it. See lt1_boundary.
  freshness: activities in the rule's window, fetched this session
  providers:
    intervals-icu: [icu_get_power_histogram, icu_get_hr_histogram, icu_get_pace_histogram, icu_get_sport_settings]

- id: sport_thresholds
  meaning: Configured thresholds and zones per sport.
  semantics: >
    FTP (outdoor and indoor, W), FTHR/LTHR (bpm), max HR (bpm), threshold
    pace, CSS, and zone bounds, as configured in intervals.icu sport
    settings. The configured value, not an estimate: never from the curve
    tools' estimates, never from the profile's FTP fields. How each was set
    (test, date, protocol) is dossier metadata, read for cp_protocol_fixity.
  freshness: fetched this session
  providers:
    intervals-icu: [icu_get_sport_settings]

- id: mean_max_power
  meaning: Best average power per duration over a date window.
  semantics: >
    Mean-maximal power (W) by duration from the power curve for the window.
    A performance marker, not a threshold: the curve tool's FTP estimate and
    zones are not part of this capability (sport_thresholds owns those).
  freshness: windows covering the review period, fetched this session
  providers:
    intervals-icu: [icu_get_power_curves]

- id: sleep_duration
  meaning: Nightly sleep duration from the athlete's sleep source.
  semantics: >
    Hours per night as recorded by the device or app synced to
    intervals.icu. A remembered or estimated figure is a different
    measurement and is not this capability.
  freshness: last 7 nights, fetched this session
  providers:
    intervals-icu: [icu_get_wellness_data]

- id: hrv
  meaning: Nightly or morning HRV from the athlete's HRV source.
  semantics: >
    rMSSD as recorded on the platform. Display only: no rule requires it,
    and nothing may gate on it (CLAUDE.md position 6).
  freshness: last 7 days, fetched this session
  display_only: true
  providers:
    intervals-icu: [icu_get_wellness_data]

- id: planned_sessions
  meaning: Sessions planned for the window under review.
  semantics: >
    Per planned session: date, sport, intended intensity (easy, quality,
    strength, finger). From calendar workout events where the athlete plans
    there; from the athlete otherwise.
  freshness: the week under review, fetched or asked this session
  providers:
    intervals-icu: [icu_get_calendar_events, icu_get_upcoming_workouts]
    manual: true

- id: finger_sessions
  meaning: Hard finger-loading sessions — hard bouldering, limit climbing, max hangboard.
  semantics: >
    Per session: date, type (bouldering, route, hangboard), and whether it
    was crimp-heavy. Bouldering and hangboard count as one category
    (finger_session_spacing). A logged climbing activity records that a
    session happened, not that it was hard; it may prompt recall but does
    not supply this capability.
  freshness: last 7 days for daily mode, last 28 days for weekly mode, asked this session
  providers:
    manual: true

- id: strength_minutes
  meaning: Minutes of structured resistance training per session.
  semantics: >
    Session date and duration in minutes. From the activity log where
    strength is logged in intervals.icu; from the athlete for sessions that
    are not. An unlogged, unreported session is absent, not zero.
  freshness: last 28 days, fetched or asked this session
  providers:
    intervals-icu: [icu_get_activities_by_date]
    manual: true

- id: strength_content
  meaning: What each strength session trained.
  semantics: >
    Per session: main content — heavy lower body, upper push, pull,
    posterior chain, finger or grip, other.
  freshness: sessions in the window, asked this session
  providers:
    manual: true

- id: lift_loads
  meaning: Current working sets on key lifts.
  semantics: >
    Per lift: load, reps, sets per week, and a tested or estimated 1RM with
    how it was obtained. Athlete-reported.
  freshness: current block, asked this session
  providers:
    manual: true

- id: pain_report
  meaning: Current pain or symptoms.
  semantics: >
    Site; whether during a session, the morning after, or present for more
    than 7 days; whether it changed how a session was performed. The inputs
    to REHAB.md ENTRY triggers and climbing_in_pain_flag.
  freshness: asked this session, every session
  providers:
    manual: true

- id: fuelling_status
  meaning: Whether intake is keeping pace with training.
  semantics: >
    The athlete's own account: keeping pace, not keeping pace, or unsure,
    with context. Not a measured energy availability. Logged calorie intake
    is a different measurement and is not this capability.
  freshness: asked this session, before any load increase
  providers:
    manual: true

- id: block_focus
  meaning: Which adaptation the current block protects.
  semantics: >
    strength-focused, cycling build, or neither. Not a calendar phase label:
    intervals.icu training-plan phases name periods, not the adaptation
    being protected, and are not this capability.
  freshness: current block, asked this session
  providers:
    manual: true

- id: vo2max
  meaning: Measured maximal oxygen uptake.
  semantics: >
    mL/kg/min from a laboratory or field test designed to measure it.
    Mean-maximal power and FTP are different measurements and do not supply
    it.
  freshness: test within the review period
  providers: {}

- id: lt1_boundary
  meaning: The intensity at the first lactate or ventilatory threshold.
  semantics: >
    The boundary below which tid_flexible counts "below LT1". A configured
    zone edge is this capability only if the athlete has established that
    edge as LT1 by test; no provider records that today.
  freshness: test or determination within the current season
  providers: {}

- id: measurement_error
  meaning: Typical measurement error of the athlete's CP/FTP protocol.
  semantics: >
    The test-retest noise against which a change counts as real. Owned by
    review-checkpoint logic, which is not built
    (plateau_order_of_operations, reconciles_with).
  freshness: per protocol
  providers: {}
```

---

## Manual provider

How the athlete is asked. This section replaces the per-check "ask the
athlete" instructions that used to sit in `SKILL.md`; the skill asks through
it.

### Protocol

- Ask only for capabilities that an active rule requires in this run, plus
  `pain_report` every session.
- Ask once per session, in one message where possible, before drafting.
- Record the answer in the provenance block as `manual`, "this session",
  with the athlete's words quoted.
- "Don't know" and no answer are absent. The check that needed it is
  reported as not run, never as passed.
- Never infer a manual capability from training data: a gap in the
  calendar is not a rest day for the fingers, and an unlogged strength
  session is not zero minutes.
- Never store a self-report in the dossier or carry it to a later session.

### Prompts

#### planned_sessions
Used when the week's plan is not in the intervals.icu calendar. "Which
sessions are planned this week, on which days, and which are hard?"

#### finger_sessions
Daily: "When was your last hard finger session — hard bouldering, limit
climbing or max hangboard? Was it crimp-heavy?" Weekly: "List your hard
finger sessions in the last 28 days, with dates, and which were
crimp-heavy." Climbing activities in the activity log may be shown to help
recall; the athlete says which were hard.

#### strength_minutes
"Any structured strength sessions in the last 28 days that are not in
intervals.icu? Date and minutes for each." Asked only for sessions the
activity log does not show.

#### strength_content
"For each strength session this week: was it heavy lower body, upper push,
pull, posterior chain, grip, or other?"

#### lift_loads
"Current working sets on your key lifts — load, reps, sets per week — and a
1RM if you have one, with how you got it (tested or estimated, and how)."

#### pain_report
Every session: "Any pain or symptoms — during your last session, the
morning after, or present for more than 7 days? Did it change how you
trained?" Any positive answer routes to the rehab check before anything
else (`REHAB.md` ENTRY; `climbing_in_pain_flag`).

#### fuelling_status
Before any load increase: "Has your intake kept pace with your training
recently — yes, no, or not sure?"

#### block_focus
When two sessions stack on one day: "Is this block protecting strength,
building cycling, or neither?" If unknown, the same-day order is not
assigned (`strength_cycling_same_day_order`).
