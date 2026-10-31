# DOSSIER

Setup guide and template. Copy this file to `DOSSIER.md` and fill it in by
hand. `DOSSIER.md` is gitignored: it holds personal health information and is
never committed.

The rules layer reads the dossier instead of asking. Every field here is
something no training platform API can supply. Update it when something
changes; otherwise it is static.

## How to fill it in

- **Empty is a valid answer. A guess is not.** An empty field keeps its rules
  inert, and the `training` skill reports them as not run. It never fills a
  gap by inferring from training data.
- **Write `none` when the answer is none.** Empty means "not answered", which
  is different from "answered: none". For the fields that gate HARD rules
  (`bsi_history`, `fuelling_flag`), this distinction is what lets the skill
  tell a checked negative from a missing answer.
- **Activating fields** carry a key in backticks. Each says which rules in
  `RULES.md` it switches on. **Context fields** activate nothing; rules read
  them as context or as the data they need to run.
- **What the dossier cannot do.** It configures the athlete, never the
  evidence stance. The seven positions in `CLAUDE.md` load for every athlete
  they concern, and no field here switches one off.

Rules that load for every athlete regardless of what is written here:
`load_metrics_are_bookkeeping`, `acwr_never_gates`, `separate_load_axes`,
`strength_dose_target`, `no_ten_percent_week_rule`, `session_ordering`,
`detraining_curve`, `prohibited_claims`, `rehab_mode_supersedes`.

---

## Disciplines — `disciplines`

List every discipline trained regularly, from: `cycling`, `running`,
`swimming`, `climbing`, `strength`. Each one activates `discipline:<name>`.
Disciplines outside this list have no rules; see the coverage section of
`README.md`.

- disciplines:

What each activates. Rules marked *(with X)* also need discipline X.

- **cycling** — `bike_load_is_the_reliable_one`,
  `cycling_knee_is_the_overuse_site`, `bike_fit_framing`,
  `cp_protocol_fixity`, `short_interval_default`,
  `interval_family_not_determinative`, `time_near_vo2max_is_a_convention`,
  `time_near_vo2max_manipulations`, `two_quality_sessions_default`,
  `minimum_effective_interval_dose`, `anchor_short_intervals_to_power`,
  `w_prime_balance_is_supplementary`, `sweet_spot_is_time_efficiency`,
  `polarized_evidence_is_distribution_level`,
  `sustainable_power_moves_by_several_routes`,
  `no_session_level_interval_ramp_rate`, `progress_something_not_nothing`,
  `response_heterogeneity_is_real`, `non_response_is_dose_dependent`,
  `plateau_order_of_operations`, `block_length_is_convention`,
  `tid_flexible`, `interference_is_smaller_than_assumed`;
  `heavy_strength_improves_cycling_without_vo2max`,
  `concurrent_endurance_frequency_cap`, `strength_cycling_same_day_order`
  *(with strength)*; `strength_priority_order` *(with climbing)*.
- **running** — `run_single_session_spike_cap`, `structural_lag_lower_limb`,
  `tid_flexible`, `interference_is_smaller_than_assumed`.
- **swimming** — `swim_load_unvalidated`, `tid_flexible`.
- **climbing** — `climbing_load_is_unquantified`,
  `no_climbing_ramp_threshold`, `antagonist_work_is_rationale_based`,
  `finger_session_spacing`, `hangboard_displaces_never_adds`,
  `structural_lag_fingers`, `crimp_exposure`, `climbing_in_pain_flag`,
  `bouldering_acute_risk`; `bouldering_counts_asymmetrically` *(with
  strength)*; `strength_priority_order` *(with cycling)*.
- **strength** — `load_magnitude_over_exercise_identity`,
  `region_specific_hypertrophy`, `strength_transfer_is_exercise_specific`,
  `emg_does_not_select_exercises`, `exercise_variation_is_systematic`,
  `heavy_load_required_for_max_strength`, `tendon_needs_high_strain`,
  `isometrics_are_analgesia_not_stiffness`, `nordic_hamstring_dose_is_low`,
  `no_overhead_selection_evidence`, `minimum_effective_strength_dose`,
  `what_survives_a_cut_session`, `strength_progression_is_load`,
  `hypertrophy_progression_is_volume_and_effort`,
  `no_fixed_percentage_progression`; plus the *(with strength)* rules above.
  `strength_dose_target` applies whether or not strength is listed: leaving
  it out means the dose flag fires, not that the rule is off.

Typical week per discipline (context — sessions/week, hours or distance,
longest session in the last 30 days for running):

- 
- Total weekly hours available:
- Hard scheduling constraints (fixed days, travel, family):

## Goal — `goal`

One of `longevity` or `performance`.

- goal:

- **longevity** — activates `crf_is_the_lever_not_the_method`,
  `zone2_not_privileged`, `no_extreme_volume_push`, and
  `no_taper_by_default` outside an event window.
- **performance** — activates none of the above. No performance-specific
  rules exist; see the coverage section of `README.md`.
- **empty** — activates `goal_type_branch`: the assistant asks before any
  recommendation that depends on goal, and does not default to longevity.

Context: secondary goal, and explicit non-goals (e.g. no racing, no volume
PRs, no weight targets):

- 

## Events — `event_date`

Next event: date (YYYY-MM-DD), name, discipline. Leave empty if none.

- event_date:

Within 21 days of the date, activates `taper_when_event_present` and
suppresses `no_taper_by_default`. Outside that window, activates nothing.

## Injury history — `injury_history`

Every injury that recurred or lost more than two weeks: site, year, the load
pattern that caused it, whether it recurred. Write `none` if none.

- 

Activates `previous_injury_weighting`: each listed site caps progression on
the loading pattern that caused it, with no expiry.

A current injury is not recorded here. It goes in `private/rehab-case.md`;
see `REHAB.md`.

## Bone stress injury history — `bsi_history`

Site, grade if known, year, management. Write `none` if none.

- 

Activates `bsi_history_pathway` (HARD). Empty is reported by the skill as an
unanswered HARD-rule gate.

## Fuelling — `fuelling_flag`

Any history of restricting intake or training under-fuelled: `yes` or `no`.
If yes, describe briefly.

- fuelling_flag:

Activates `underfuelling_check` (HARD), which otherwise runs only before a
load increase. Empty is reported as an unanswered HARD-rule gate.

## Sleep — `sleep_logged`

Sleep source and how reliably it is logged. Leave empty if not logged.

- sleep_logged:

Activates `sleep_as_modifier`.

---

## Context fields

These activate nothing. Rules read them as context, and some cannot run
without them.

### Identity and baseline

- Age:
- Sex:
- Years of consistent endurance training:
- Years of consistent resistance training: (read by the caveats of
  `heavy_load_required_for_max_strength`,
  `load_magnitude_over_exercise_identity` and `strength_progression_is_load`,
  whose evidence base is mostly novices)
- intervals.icu athlete id:

### Thresholds

Record the protocol with every value: `cp_protocol_fixity` only compares
values from an identical protocol.

- FTP (date, protocol):
- CP / W' (date, protocol):
- Run threshold pace or LTHR (date):
- Swim CSS (date, stroke, course):
- Last threshold test of any kind:

### Health flags

- Known cardiac findings:
- Medications affecting HR or HRV:
- Anything a coach should know before prescribing high intensity:

### Data sources and their reliability

- Cycling power: yes/no, meter type (`anchor_short_intervals_to_power`
  substitutes RPE and terrain, not HR, without one)
- Running: GPS only / footpod / power
- Swimming: manual entry / watch
- HRV: source, morning protocol, consistency
- Strength: logged where? If not in intervals.icu, `strength_dose_target`
  cannot be enforced automatically and weekly mode asks.
- Climbing: logged where? No validated metric exists
  (`climbing_load_is_unquantified`); finger-session spacing needs at least
  the date and whether each session was hard.

### Standing preferences

- Days that are always rest:
- Sessions I will not do regardless of what the data says:
- How direct the coaching tone should be:
