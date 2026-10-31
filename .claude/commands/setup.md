---
description: Build or update DOSSIER.md from DOSSIER.template.md by guided interview, using intervals.icu for what the platform knows
argument-hint: "[--section <name>]"
---

# /setup

Builds `DOSSIER.md` from `DOSSIER.template.md` as a guided flow of seven
sections. Read `CLAUDE.md` first — the data ownership section governs
everything below.

**This is the `intervals-icu` provider's setup.** Rules and the `training`
skill reach data only through capabilities (`capabilities.md`) and never
name tools. This command is the one place outside `capabilities.md` that
calls intervals.icu tools by name, because its job is to configure that
provider: resolve the athlete, confirm what the platform holds, and record
which capabilities the athlete supplies elsewhere. A fork that adds a
provider adds its own setup alongside this one.

Arguments: `$ARGUMENTS`

## Ground rules

- **Read-only on the platform.** Use only the read tools listed below. Never
  call a write tool — in particular never `icu_update_sport_settings`,
  `icu_create_sport_settings`, `icu_update_athlete_notes` or
  `icu_update_wellness`. A discrepancy is reported, not fixed.
- **Platform values are shown, never stored.** Thresholds, zones, load,
  volumes, wellness, and profile values the platform holds (date of birth,
  sex, weight) appear in the question that needs them and are then
  discarded. The only platform identifier written to the dossier is
  `athlete_id`.
- **Empty is a valid answer; never guess.** Do not fill a field from
  training data, memory, earlier sessions or project context. `Don't know`
  and `Skip` both leave the field empty. `none` is recorded only when the
  athlete says none.
- **Write only `DOSSIER.md`.** A current injury goes to
  `private/rehab-case.md` (format in `REHAB.md`), never to the dossier, and
  only if the athlete wants it recorded. Both are gitignored, so setup does
  not run `tools/lint_rules.py`.

## What gets asked

- **Only what something reads.** Every question below names its reader in
  brackets — a rule's activation, a rule's caveat, a capability, or weekly
  planning, which reads the dossier as context. The reader is for this
  spec; the athlete never sees it. Do not add a question without one.
- **Not what the platform shows.** A discipline with activities is logged in
  intervals.icu; rides with power have a power source; HRV and sleep with
  values sync. None of this is asked.
- **Not what was already said.** If an earlier typed answer contains the
  answer to a later question, confirm it (`Yes` / `Change`) instead of
  asking again.

## Interaction

- **Every question uses `AskUserQuestion`.** One decision per question.
  2–4 options, and `Don't know` and `Skip` are always two of them; the
  tool's automatic Other option takes a typed answer. Up to four
  independent questions of one section go in a single call; a follow-up
  waits for the answer it depends on.
- **Free text is the last resort** — only for descriptions, dates and exact
  numbers that no option covers. First ask the deciding question with
  options, then ask for the description in plain text only if the answer
  calls for it, one thing per prompt. Candidates seen in the fetched data
  (device names, activity names, dates) are offered as options first.
  Ranges are fine where an exact figure is not needed.
- **Questions stand alone.** The dialog may hide earlier text, so each
  question carries what it needs: the platform value it asks about and the
  tool it came from, or the recorded answer it asks to confirm. Platform
  values appear only inside the question that needs them.
- **Plain words.** A technical term is glossed in a few words on first use,
  e.g. "threshold heart rate (FTHR): the heart rate you can hold for about
  an hour". Never say which rule a field activates or why a question is
  asked.
- **Progress.** Every section, including section 1, opens with one line,
  `Section N of 7 — <name>`. Every question header starts with `N/7` (at
  most 12 characters, e.g. `3/7 Logging`).
- **Quiet between questions.** No recaps, no "Noted: …". One line only when
  an answer creates an action for the summary.
- **Recorded answers: one confirmation per section.** When a section's
  fields already hold answers, the first question lists them — `All
  correct` / `Change some` — and only the fields the athlete picks are
  asked. `Don't know` or `Skip` keeps them. When a new answer contradicts a
  recorded line (e.g. a roles note naming a discipline just answered `No`),
  that line is asked `Keep` / `Change` before saving.

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
| `icu_get_activities_by_date` | sports present, rough weekly volume, overlapping activities, over the last 12 weeks; test activities in a stated window |
| `icu_get_activity_details` | the recording device and data streams of a single activity (the list tool returns neither) |
| `icu_get_wellness_data` | whether sleep reaches the platform: nights with a value over the last 28 days. Counts only, never the values |
| `icu_get_calendar_events` | upcoming race events, if the athlete keeps events in intervals.icu — shown for confirmation, not stored |
| `icu_search_activities` | CP/FTP test activities by tag or name — shown for confirmation, not stored |

Pass `athlete_id` from the dossier on every call. Do not take thresholds from
the profile's FTP fields or from the curve tools (`CLAUDE.md`, data
ownership, item 2).

## Sections

| # | Flow section | Template sections |
| --- | --- | --- |
| 1 | Disciplines | `disciplines` (the list), `training_age` |
| 2 | Goal | `goal` |
| 3 | Logging | `disciplines` (where each is logged), `data_sources`, `sleep` |
| 4 | Thresholds | `thresholds` |
| 5 | Events | `events` |
| 6 | Health and injury | current injury, `injury_history`, `bsi_history`, `fuelling`, `health` |
| 7 | Preferences | `preferences`, `disciplines` (scheduling) |

`athlete_id` is resolved before section 1 and is not counted.

`--section <name>` resolves the athlete, then asks only the questions for
that template section (names as in the `Section name:` lines of the
template: `athlete_id`, `disciplines`, `goal`, `events`, `injury_history`,
`bsi_history`, `fuelling`, `sleep`, `training_age`, `thresholds`, `health`,
`data_sources`, `preferences`), saves, and ends with the summary. Progress
lines use the flow section number. An unknown name: list the valid ones and
stop.

## Saving and resuming

- **Create.** If `DOSSIER.md` does not exist, copy `DOSSIER.template.md` to
  it first.
- **Migrate.** If it exists but predates the current template, add the
  missing fields and sections at their template position. A section whose
  template key changed is replaced by the template's version, carrying over
  every answer whose field still exists. An answer whose field the template
  no longer has stays in the dossier as written; it is not asked about and
  not deleted.
- **Edit in place.** Change only the lines the athlete answers. A field they
  do not touch keeps its value; never rewrite the file wholesale.
- **Save after each section.** Write the section's answers to `DOSSIER.md`
  before the next section starts, and update the progress marker on the
  line after the `# DOSSIER` heading:

  `<!-- setup: done <comma-separated flow section numbers>; updated YYYY-MM-DD -->`

  The marker is the only setup state; it holds no answers.
- **Resume.** If the marker lists some sections but not all, the first
  question offers `Resume at section N` or `Start from section 1`, plus
  `Don't know` and `Skip` (both resume). Starting over keeps every recorded
  answer.
- **Platform values in the dossier.** If the existing dossier contains a
  platform-owned value (a threshold, a volume, a wellness figure), ask in
  the section it belongs to whether to remove it. Remove it only on
  confirmation.

## Flow

### Welcome

One short text message, no question: setup records what intervals.icu
cannot know; seven sections, roughly 10 minutes; every question can be
answered `Don't know` or `Skip`; progress is saved after each section. If
the dossier already has answers, say they are kept and shown for
confirmation.

### Athlete id and fetch

If the dossier has an `athlete_id`, call `icu_get_athlete_profile` with it.
If it resolves, name the athlete in one line and continue. If the dossier
has none, ask whether the athlete knows it (`I'll type it` / `Look it up`);
`Look it up` shows the athletes from `icu_list_athletes` as a question for
them to pick from. If no id resolves, say so and stop: every section after
this needs the platform. Record the id only once it resolves.

Then fetch once:

- `icu_get_sport_settings` — every sport the athlete has.
- `icu_get_activities_by_date` — `oldest` = 12 weeks ago, `newest` = today.
  Derive per activity type: sessions and rough weekly hours; activities
  whose start times overlap (duplicate candidates). Say if history is
  shorter than 12 weeks.
- `icu_get_wellness_data` — `days_back` = 28. Derive only how many nights
  have a sleep value.

Note the fetch time. Every question that shows a platform value names the
tool it came from.

### Section 1 of 7 — Disciplines

- **Trained regularly** [`discipline:` activation]: one question per
  discipline that the dossier lists or the activities show, plus climbing
  and strength always. `Yes` / `No`. The question shows what the activities
  show (sessions, rough hours per week, from `icu_get_activities_by_date`;
  one or two sessions are described as such, not as volume) and what the
  dossier records. For climbing and strength it says intervals.icu often
  does not see them.
  - Mapping: `Ride`, `VirtualRide`, `GravelRide`, `MountainBikeRide` →
    cycling; `Run`, `TrailRun`, `VirtualRun` → running; `Swim`,
    `OpenWaterSwim` → swimming; `RockClimbing` → climbing;
    `WeightTraining` → strength. Other types are uncovered: no rules
    (`README.md`, coverage), not asked about.
- **Resistance-training years** [caveats of
  `heavy_load_required_for_max_strength`,
  `load_magnitude_over_exercise_identity`, `strength_progression_is_load`]:
  ranges as options, Other for the exact figure.
- **Profile** [CLAUDE.md data ownership]: one question showing sex, date
  of birth and weight from `icu_get_athlete_profile` — `Correct` /
  `Something is wrong`. A wrong value becomes a summary action (correct it
  in intervals.icu); nothing is stored. If the tool returns no value for a
  field, ask whether the profile has it: if yes, it is a provider gap,
  listed in the summary, nothing stored; if no and the athlete gives it,
  record it and say why.

### Section 2 of 7 — Goal

- **Leading goal** [`goal` activation]: `Longevity` / `Performance`.

### Section 3 of 7 — Logging

- **Disciplines with no activities in the 12 weeks** [`strength_minutes`
  manual provider; weekly planning]: where they are logged — `Not logged`
  / `Another app` (named via Other). If not logged in intervals.icu: a
  fixed weekday (`Yes` / `Varies`, day typed) and typical duration
  (ranges). Disciplines with activities are not asked: they are logged in
  intervals.icu.
- **Duplicate candidates** [`activity_log`, `fitness_load`]: one question
  per overlapping pair. It shows date, names, durations, and which data
  each copy carries (power, HR) from `icu_get_activity_details` —
  `Duplicates` / `Not duplicates`. If duplicates, the summary action is to
  remove one copy in intervals.icu, naming the stream that copy would lose
  if the two carry different data. Recorded under Data sources: duplicate
  uploads occur, from which sources, date flagged.
- **Sleep source** [`sleep_logged` activation]: only if sleep has values on
  the platform. The question shows the night count from
  `icu_get_wellness_data` and offers the device seen in recent activities
  (from `icu_get_activity_details`) / `Another device or app`. Recorded as
  that source, synced to intervals.icu. If sleep has no values: no
  question, `sleep_logged` stays empty; data kept elsewhere reaches no rule
  (`sleep_duration` has no manual provider). Low coverage (under half the
  nights): one question — `Expected (not worn nightly)` / `Sync issue`; a
  sync issue becomes a summary action.

### Section 4 of 7 — Thresholds

Only for sports in the confirmed disciplines. For each threshold in
`icu_get_sport_settings` (FTP or CP and W′, threshold pace, CSS, threshold
HR, max HR), glossed on first use:

- **Matches** [`cp_protocol_fixity`; summary action]: the question shows
  the value and its tool — `Matches my last test` / `Differs` (the
  athlete's figure via Other). If it differs, show both and their sources,
  do not judge whether the difference matters, and make it a summary
  action: retest, or update the sport setting in intervals.icu. Record the
  open discrepancy without numbers (sport, threshold, date flagged).
- **Set by** [`cp_protocol_fixity`]: max HR — `Race or hard effort` /
  `Formula or estimate`; every other threshold — `Test` / `Estimate`. For a
  test or effort: date (ranges, or the date if the athlete gave one) and
  protocol. If the athlete does not recall the protocol, look for the
  activity in the stated window (`icu_search_activities` by name,
  `icu_get_activities_by_date` for the window) and offer the candidates
  with their durations. Record test type, date and protocol. Never the
  number.

Then:

- **Test tag** [`cp_test`]: whether CP/FTP tests are tagged in intervals.icu
  (`Yes`, tag via Other / `No`). If a tag is given, the next question shows
  the matching activities from `icu_search_activities` — `These are my
  tests` / `Not right`. Record the tag only with a recorded protocol.
- **LT1** [`lt1_boundary`]: whether a test established the first lactate
  threshold (`Yes` / `No`). If yes, a question showing the sport's zones
  from `icu_get_sport_settings` with two likely zone edges as options
  (Other for another), then test and date. Record sport, zone edge, test
  and date — never the value. If no test established it, leave the line
  empty: a default zone edge is not LT1.

### Section 5 of 7 — Events

- **Where events are kept** [`events` capability]: `intervals.icu` / `This
  dossier`. Record it as `events_provider`.
- `intervals.icu`: one question showing the race events for the next 8
  weeks from `icu_get_calendar_events` — `Complete` / `Something missing`.
  Missing becomes a summary action (add it in intervals.icu). Record no
  dates. If the dossier still holds event dates, ask whether to remove them
  (single source per value).
- `This dossier`: `None planned` / `I have one`; if one, date, name and
  discipline in plain text. Record `none` only on `None planned`.

### Section 6 of 7 — Health and injury

- **Current injury** [`rehab_mode_supersedes`]: `Yes` / `No`. If
  `private/rehab-case.md` exists, the question names its case and state.
  Setup does not edit or close it (the athlete's decision, `REHAB.md`). A
  new current injury is not recorded in the dossier: say it belongs in
  `private/rehab-case.md` and offer to record it there.
- **Injury history** [`previous_injury_weighting`]: any injury that
  recurred or cost more than two weeks (`Yes` / `None`). If yes, per
  injury: site, year, the load pattern that caused it, whether it recurred.
- **Bone stress injury** [`bsi_history_pathway`]: `Yes` / `None`. If yes,
  site, grade if known, year, management.
- **Fuelling** [`underfuelling_check`]: any history of restricting intake or
  training under-fuelled (`Yes` / `No`). If yes, a brief description.
- **Health flags** [weekly planning]: one question — any cardiac finding,
  medication affecting heart rate, or other reason for care with high
  intensity (`None` / `Yes`), described in plain text only on `Yes`. A
  current injury already given is not asked again here.

### Section 7 of 7 — Preferences

All read by weekly planning.

- **Fixed rest days**: `None fixed` / `Yes`, days typed.
- **Hard scheduling constraints** (fixed days, travel, family): `None` /
  `Yes`, typed. Confirm, don't re-ask, a fixed day given in section 3.
- **Sessions refused regardless of data**: `None` / `Yes`, typed.

### Summary

Once, at the end, written for the athlete. No rule ids unless asked.

1. **To do** — every action on the athlete's side, one line each: profile
   corrections, provider gaps, duplicates, threshold discrepancies, retests,
   events to add, sync issues.
2. **What the assistant can't do yet** — derived at run time from the
   `activation:` and `requires:` tags in `RULES.md` and the providers in
   `capabilities.md`, not from the template's lists. In plain words, one
   line each, with what would change it. Example: "Can't compare FTP tests
   over time — tag your test activities." A line that states what a rule
   says carries the rule's confidence label (CLAUDE.md position 7). A check
   whose data is asked in each training session (a manual provider) is not
   listed here.
3. **Recorded** — one line per section.
4. One closing line: the number of rules now active, and that the full list
   (ids, type, confidence labels) is available on request.

Thresholds, volumes and profile values were confirmed but not written; they
are fetched each session. Say so in one line only if the athlete asks what
was stored.
