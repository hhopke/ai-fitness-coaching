---
description: Build or update DOSSIER.md from DOSSIER.template.md by interview, using intervals.icu for what the platform knows
argument-hint: "[--section <name>]"
---

# /setup

Builds `DOSSIER.md` from `DOSSIER.template.md`. Read `CLAUDE.md` first —
the data ownership section governs everything below.

Arguments: `$ARGUMENTS`

## Ground rules

- **Read-only on the platform.** Use only the read tools listed below. Never
  call a write tool — in particular never `icu_update_sport_settings`,
  `icu_create_sport_settings`, `icu_update_athlete_notes` or
  `icu_update_wellness`. A discrepancy is reported, not fixed.
- **Platform values are shown, never stored.** Thresholds, zones, load,
  volumes, wellness, and profile values the platform holds (date of birth,
  sex, weight) appear in the conversation for confirmation and are then
  discarded. The only platform identifier written to the dossier is
  `athlete_id`.
- **Empty is a valid answer; never guess.** Do not fill a field from
  training data, memory, earlier sessions or project context. If the athlete
  does not answer, leave it empty. `none` is recorded only when they say
  none.
- **Write only `DOSSIER.md`.** A current injury goes to
  `private/rehab-case.md` (format in `REHAB.md`), never to the dossier, and
  only if the athlete wants it recorded.

## MCP tools

Names as registered by the intervals.icu MCP server
(hhopke/intervals-icu-mcp). In Claude Code they carry the client's prefix,
e.g. `mcp__<server>__icu_get_sport_settings`. If they are not available,
stop and say the server is not connected; do not continue from memory.

| Tool | Used for |
| --- | --- |
| `icu_get_athlete_profile` | confirm `athlete_id` resolves; profile values (sex, date of birth, weight) for confirmation |
| `icu_list_athletes` | only if the athlete does not know their id: list reachable athletes so they can pick. Never pick for them |
| `icu_get_sport_settings` | thresholds and zones per sport — the only source for them |
| `icu_get_activities_by_date` | sports present and rough weekly volume over the last 12 weeks |

Pass `athlete_id` from the dossier on every call. Do not take thresholds from
the profile's FTP fields or from the curve tools (`CLAUDE.md`, data
ownership, item 2).

## Sections

`--section <name>` runs step 1 (to resolve the athlete) and then only the
named section, followed by the summary. Names match the `Section name:`
lines in the template:

`athlete_id`, `disciplines`, `goal`, `events`, `injury_history`,
`bsi_history`, `fuelling`, `sleep`, `training_age`, `thresholds`, `health`,
`data_sources`, `preferences`.

An unknown name: list the valid ones and stop.

## Idempotence

- If `DOSSIER.md` does not exist, copy `DOSSIER.template.md` to it first.
- If it exists, read it. For each section, show what is recorded and ask
  whether it changed. Edit only the lines the athlete changes. A field they
  do not touch keeps its value; never rewrite the file wholesale.
- If the existing dossier contains a platform-owned value (a threshold, a
  volume, a wellness figure), point it out and offer to remove it. Remove it
  only on confirmation.

## Flow

### 1. Athlete id

If the dossier has no `athlete_id`, ask for it. If the athlete does not know
it, `icu_list_athletes` may be shown to help them find it. Call
`icu_get_athlete_profile` with the id. If it does not resolve, say so and
stop. Record the id only once it resolves.

### 2. Fetch

- `icu_get_athlete_profile` — profile.
- `icu_get_sport_settings` — settings for every sport the athlete has.
- `icu_get_activities_by_date` — `oldest` = 12 weeks ago, `newest` = today.
  Summarise: sports present, and rough weekly volume per sport (sessions and
  hours). Twelve weeks; say so if history is shorter.

Note the fetch time. Everything below that shows a platform value names the
tool it came from.

### 3. Thresholds — `thresholds`

Present each threshold and zone set from `icu_get_sport_settings` for
confirmation only. For each threshold ask: how was it set (test type), when,
under what protocol? Record that provenance in the Threshold provenance
section. Do not record the number.

### 4. Discrepancies

If the athlete states a threshold that differs from the platform value, say
so plainly, showing both and their sources. Do not judge whether the
difference is material on the athlete's behalf, and do not resolve it
silently. Recommend either a retest or updating the sport setting in
intervals.icu themselves. Record the open discrepancy in the dossier without
numbers (sport, which threshold, date flagged, recommendation). Never write
to sport settings.

### 5. Disciplines — `disciplines`

Map activity types from step 2 to the template's disciplines: `Ride`,
`VirtualRide`, `GravelRide`, `MountainBikeRide` → cycling; `Run`,
`TrailRun`, `VirtualRun` → running; `Swim`, `OpenWaterSwim` → swimming;
`RockClimbing` → climbing; `WeightTraining` → strength. List any activity
type that maps to none of them as uncovered — it gets no rules (`README.md`,
coverage).

Propose the derived list, then confirm it with the athlete. Ask explicitly
about disciplines intervals.icu usually does not see — climbing and
strength — and record where each is logged, or that it is self-reported.
The volumes from step 2 are shown, not stored.

### 6. Interview — platform-unknowable fields

One section at a time, in template order:

- `goal` — longevity, performance, or both. If both, which leads: the
  leading one is the `goal` value, the other goes under secondary goal.
- `events` — next event date, name, discipline.
- `injury_history` — every injury that recurred or cost more than two
  weeks.
- `bsi_history` — bone stress injuries.
- `fuelling` — any history of restricting intake or training under-fuelled.
- `sleep` — sleep source and logging reliability.
- `training_age` — years per discipline, years of resistance training.
  Age, sex and weight: confirm the profile values from step 2; record them
  only if the profile lacks them.
- `health`, `data_sources`, `preferences`, and scheduling constraints.

If the athlete mentions a current injury, say it belongs in
`private/rehab-case.md` and offer to record it there.

### 7. What each field activates

For each activating field, state which rules it switches on. Derive this
at run time from the `activation:` tags in `RULES.md` — do not rely on the
lists in the template, which can lag. Name each rule with its type and
confidence label.

### 8. Summary

End with:

- **Active** — rules now active, grouped by the field or discipline that
  activates them, plus the rules that load for every athlete.
- **Gated** — rules still inert, each with the field that would unlock it.
  Empty HARD-rule gates (`bsi_history`, `fuelling_flag`) first.
- **Discrepancies** — unresolved threshold discrepancies, with the
  recommendation made.
- **Not stored** — a one-line reminder that thresholds, volumes and profile
  values were confirmed but not written, and are fetched each session.
