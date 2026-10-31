# Changelog

Versions are `RULES.md` versions. Dates are commit dates. Each entry names
the rules added, removed or changed, so a change in advice can be traced to
a change in a rule.

History before v0.4 was squashed when the repository was published. The
v0.3 and v0.3.1 entries are reconstructed from that earlier history; their
commits are not in this repository.

## v0.7 — 2026-10-31

Rules:
- `non_response_is_dose_dependent` — `requires:` now accepts
  `any_of: [vo2max, cp_test]`. New caveat: the dose-dependence finding was
  measured in VO2max; CP is accepted on the strength of the review's
  planning recommendation, not of the dose-response data.
- `plateau_order_of_operations` — `requires:` now accepts
  `any_of: [vo2max, cp_test]`, matching the review's "VO2max/CP" wording.
- `taper_when_event_present`, `no_taper_by_default` — activation reads the
  `events` capability (`capability:events within 21d`) instead of the
  dossier field. An unreadable event list leaves both unloaded and the gate
  reported, rather than counting as no event.

Other:
- `capabilities.md`: added `cp_test` and `events`; `lt1_boundary` is now
  supplied by a dossier declaration (zone edge, test, date — never the
  value).
- `/setup` records the LT1 declaration, the CP/FTP test tag, and where
  events are kept; it is labelled as the intervals-icu provider's setup.
- Lint: `any_of:` entries and `capability:` activation tags.
- Licence: the whole repository is MIT. The CC BY 4.0 split is removed.

## v0.6 — 2026-10-31

Rules:
- `requires:` added to 32 rules, naming the capabilities each reads. No
  rule names a tool.

Other:
- `capabilities.md`: the contract between rules and data. Two providers,
  `intervals-icu` and `manual`; the manual provider's prompts replace the
  scattered "ask the athlete" instructions in the skill. Three capabilities
  had no provider: `vo2max`, `lt1_boundary`, `measurement_error`.
- Provenance block and plan reviewer work by capability, provider and fetch
  time.
- `CONTRIBUTING.md`: providers live in forks; a metric with different
  semantics is a new capability.

## v0.5.1 — 2026-10-31

Rules (confidence labels only):
- `what_survives_a_cut_session` — `evidence-informed` → PRACTITIONER. The
  source wording is kept in `source_label:`; a `judgment_call:` explains the
  mapping.
- `no_overhead_selection_evidence` — `no evidence exists` → NO EVIDENCE.
- `goal_type_branch`, `rehab_mode_supersedes` — confidence
  `N/A (architectural)`, valid only with `judgment_call:`.

Other:
- Data ownership rule in `CLAUDE.md`: platform values are fetched each
  session and never written to a repo file.
- `/setup`, the read-only `plan-reviewer` agent, the provenance block,
  `tools/lint_rules.py`, and CI.

## v0.5 — 2026-10-31

Generalised from one named athlete to one athlete per copy. Disciplines,
goal and events moved from `CLAUDE.md` into the dossier.

Rules:
- Added `goal_type_branch` (BRANCH): with no goal declared, ask; never
  default to longevity.
- Activation changed:
  - `crf_is_the_lever_not_the_method`, `zone2_not_privileged`,
    `no_extreme_volume_push` — `always` → `dossier:goal=longevity`.
  - `no_taper_by_default` — `always` → longevity goal and no event within
    21 days.
  - `taper_when_event_present` — keyed to the dossier event date.
  - `strength_priority_order` — `always` → cycling and climbing both
    declared.
  - `interference_is_smaller_than_assumed` — `always` → cycling or running.
  - `tid_flexible` — cycling only → any endurance discipline, so the
    intensity-distribution position loads for runners and swimmers.
  - `swim_load_unvalidated` — `dormant` → `discipline:swimming`.
- Wording generalised: `separate_load_axes` (an axis no discipline feeds is
  not applicable), `session_ordering` (each item applies only to declared
  disciplines), `concurrent_endurance_frequency_cap`,
  `interval_family_not_determinative`, `minimum_effective_interval_dose`.

Other:
- `DOSSIER.template.md` became the setup guide: each field lists the rules
  it activates.

## v0.4 — 2026-10-31

First version in the published history. Integrates the ACSM 2026
resistance-training position stand (`reviews/04-acsm-rt.md`, extracted from
the full text, retrieved 2026-09-11).

Rules:
- Refined against ACSM 2026: `load_magnitude_over_exercise_identity`
  (failure not required; full range of motion matters),
  `heavy_load_required_for_max_strength` (threshold narrowed to ≥80% 1RM),
  `minimum_effective_strength_dose`, `what_survives_a_cut_session`
  (heavy compound first).
- Removed `progress_effort_not_a_fixed_percentage`, split into:
  - `strength_progression_is_load` — the old wording had carried a
    hypertrophy finding over to strength.
  - `hypertrophy_progression_is_volume_and_effort` — failure not required;
    no exact RIR target is derivable.
  - `no_fixed_percentage_progression` — unchanged, HARD.
- `tendon_needs_high_strain`, `strength_cycling_same_day_order` — wording
  no longer names a specific athlete's injury.

Other:
- `DOSSIER.md` untracked; the active rehab case moved to the gitignored
  `private/rehab-case.md`.

## v0.3.1 — 2026-08-12

Rules:
- `strength_dose_target` — corrected after a primary-source check. The
  previous figures ("max ~27% reduction at ~60 min/wk, RR 0.74" and
  benefit flattening or reversing above ~140 min/wk) were not supported by
  the cited meta-analysis, which reports ~10-20% maximum risk reduction at
  ~30-60 min/week and an unclear effect above that. The 120 min upper bound
  now rests on a 30-year cohort. `correction:` field added.

Other:
- Every HARD-rule numeric and every absence claim checked against primary
  sources: 15 claims, 13 held, one attribution resolved, one failed (the
  figure above). Recorded in `reviews/README.md`.

## v0.3 — 2026-08-11

Rules:
- Integrated `reviews/03-session-prescription.md`: 33 rules added (38 → 71)
  covering cycling interval prescription, strength session content and
  progression logic. `prohibited_claims` extended.

Changed on 2026-08-12 without a version bump (the lint now blocks this):
- `source:` provenance backfilled on 70 rules; every rule carries
  `source:` or `judgment_call:`.
- `strength_before_hiit_conflict` removed, replaced by
  `strength_cycling_same_day_order`, which resolves same-day order by the
  adaptation the current block protects.
