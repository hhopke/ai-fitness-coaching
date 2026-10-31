# RULES v0.6

Full rules layer. Nothing is deleted; rules activate by tag.

```
activation:
  always              — loads every session
  discipline:<name>   — loads when that discipline is in the dossier
  state:rehab         — loads only in rehab mode (see REHAB.md)
  dossier:<field>     — loads only when that dossier field is populated
  dossier:<field>=<v> — loads only when that dossier field holds value v
  dossier:<field> within <N>d
                      — loads only when the date in that dossier field is
                        between today and N days from today
  dormant             — retained, not currently reachable; reason stated
  AND / OR / NOT      — combine the above; NOT state:rehab means the rule
                        does not load while rehab mode is active
```

`NOT state:rehab` is a load-time gate, not a substitute for
`rehab_mode_supersedes`. It carries no authority of its own: it keeps
prescriptive rules from being read at all in rehab, so that subordination
never has to be argued. Removing it does not make a rule apply in rehab.

Disciplines, goal and events are read from `DOSSIER.md`. Nothing in this file
assumes a particular athlete: a rule that depends on the athlete's profile is
gated on the dossier field that declares it. `DOSSIER.template.md` lists which
rules each field activates.

Activation configures the athlete, never the evidence stance. The rules that
encode the seven `CLAUDE.md` positions load for every athlete they concern —
`activation: always`, or gated only by the discipline the position is about.
No dossier field switches a position off, and no rule may be gated on a
setting whose purpose is to do so.

`type:` HARD (do not override) · SOFT (default, overridable) ·
BRANCH (do not decide, ask) · DISCLOSURE (state when relevant)

`confidence:` uses a closed set of labels; lowercase qualifiers may follow
one. `tools/lint_rules.py` enforces it.
  CONSENSUS, CONTESTED, PRACTITIONER — inherited from the reviews.
  NO EVIDENCE — the literature was checked and is silent on the question.
    An evidential finding: the absence is the result.
  N/A (architectural) — the rule makes no evidential claim at all; it routes,
    gates or asks. Valid only together with `judgment_call:`, which says why.
Where a source uses a label outside this set, the rule carries the nearest
label in `confidence:`, the source's wording verbatim in `source_label:`, and
a `judgment_call:` explaining the mapping.

Confidence labels are inherited from the source reviews and must not be
stripped when a rule is quoted, summarised or acted on.

`source:` cites the review and section each rule derives from — the whole
chain, where a rule synthesises across sections. Cite `NN-name.md` plus the
section number; `7-recommendation N` means a recommendation inside section 7
of the endurance review, `cross-cutting recommendation N` the document-level
list. Every rule carries `source:` or `judgment_call:`.

`correction:` records a claim that failed verification against a primary
source, what it said before, and what the source actually says. The review body
is never edited to match — it is the historical record, and the defect is
logged in `reviews/README.md`.

`judgment_call:` marks a position this repo takes that the reviews do not
supply: a type promoted beyond its evidence, a threshold chosen for
enforcement, or a taxonomy built on top of the findings. It names what is
system decision and what is review finding, so the two never blur.

`requires:` lists the capabilities a rule reads, by name from
`capabilities.md`, which defines each one and the provider that supplies it.
A rule never names a data source or a tool. A rule with no `requires:` reads
no data: it frames, prohibits or routes. Where a required capability is
absent in a run, the rule's check is reported as not run.

`resolution:` records a conflict between sources that was decided: which
rule the conflict was in, what each source said, and what changed. A
`contradicted_by:` field marks a conflict that is recorded but not yet
decided; it is removed when a `resolution:` replaces it.

---

## 1. LOAD ACCOUNTING

```yaml
- id: load_metrics_are_bookkeeping
  activation: always
  type: DISCLOSURE
  confidence: CONSENSUS
  statement: >
    TSS, CTL, ATL, TSB and sRPE are dose indices, not stress-response
    measures. Equal-load sessions are not physiologically equivalent.
  source: 01-endurance.md 1.3, cross-cutting recommendation 1

- id: acwr_never_gates
  activation: always
  type: HARD
  confidence: CONSENSUS
  statement: >
    ACWR may be displayed, never used to gate or trigger a decision.
    Mathematical coupling; an acute-to-random ratio performs equivalently;
    no causal estimate exists.
  source: 01-endurance.md 1.4, cross-cutting recommendation 1

- id: separate_load_axes
  activation: always
  type: HARD
  confidence: CONSENSUS
  requires: [fitness_load, activity_log, finger_sessions, strength_minutes]
  statement: >
    Three axes are tracked separately and never collapsed into one number
    for decision purposes:
      1. systemic/cardiometabolic  (cycling, running, swimming)
      2. finger/upper-limb mechanical  (climbing, hangboard, pulling)
      3. lower-limb tendon/structural  (cycling volume, strength, running)
    A combined figure may be shown for trend context only, labeled
    systemic-only. An axis with no declared discipline feeding it is empty,
    and is reported as not applicable rather than as zero load.
  source: 01-endurance.md SECTION 4, 3.2, cross-cutting recommendations 3, 4; 02-climbing.md A1, recommendation 1
  judgment_call: >
    The three-axis taxonomy is a system design. The reviews establish that
    climbing load cannot be summed into endurance load (02-climbing.md A1)
    and that combining disciplines masks single-discipline spikes
    (01-endurance.md SECTION 4); naming exactly these three axes is the
    synthesis this repo adds.

- id: climbing_load_is_unquantified
  activation: discipline:climbing
  type: DISCLOSURE
  confidence: CONSENSUS
  statement: >
    No validated external-load metric exists for climbing. sRPE x duration
    is the only validated internal measure and captures bouldering worst of
    all climbing disciplines (r=0.40 vs lead 0.61, training 0.66), because
    bouldering strain is local rather than systemic. The facet that matters
    most is the facet the metric tracks least well. Treat any climbing load
    number as low-confidence.
  source: 02-climbing.md A1, recommendation 1

- id: no_climbing_ramp_threshold
  activation: discipline:climbing
  type: HARD
  confidence: CONSENSUS (absence of evidence)
  statement: >
    No validated ramp-rate, ACWR or progression threshold exists for
    climbing or finger load. Do not invent one and do not import running's
    spike cap. Use conservative progression plus the risk markers below.
  revisit_if: prospective climbing ramp-rate study published
  source: 02-climbing.md A3, recommendation 5

- id: swim_load_unvalidated
  activation: discipline:swimming
  type: DISCLOSURE
  confidence: CONSENSUS
  statement: Swim TSS largely unvalidated; anchor to CSS pace.
  source: 01-endurance.md 3.3, cross-cutting recommendation 3
```

## 2. STRENGTH — DOSE AND ALLOCATION

```yaml
- id: strength_dose_target
  activation: always
  type: HARD
  confidence: CONSENSUS
  requires: [strength_minutes]
  statement: >
    Dose to the injury-prevention target, not the mortality minimum.
    ~30-60 min/week captures most of the mortality benefit: J-shaped
    association, maximum risk reduction ~10-20%, across all-cause mortality,
    CVD and total cancer. Injury prevention is the larger and differently
    shaped effect — dose-dependent, no observed harm ceiling, RR 0.338
    (~66% reduction). Operating band 60-120 min/week structured strength.
    Above that band the mortality evidence does not show benefit reversing;
    it shows the influence of higher volume is unclear. That is the
    divergence point — mortality evidence goes quiet while injury and
    performance benefit may continue — and it is not a hard cap.
  enforcement: flag any 28-day window averaging under 60 min/week
  source: 02-climbing.md B4, recommendation 6; 01-endurance.md 6.3
  correction: >
    Corrected 2026-08-12 against primary sources. The previous statement read
    "max ~27% reduction at ~60 min/wk, RR 0.74, 95% CI 0.64-0.86" and "above
    ~140 min/wk mortality benefit flattens or reverses". Neither is supported
    by Momma et al. 2022 (BJSM 56(13):755-763, 16 cohort studies), which
    reports maximum risk reduction of approximately 10-20% at approximately
    30-60 min/week and concludes that the influence of a higher volume "is
    unclear". The review body of 02-climbing.md B4 still carries the original
    figures and is left unaltered as the historical record; the defect is
    logged in reviews/README.md.
  judgment_call: >
    The 60 min/week enforcement floor is a system decision — no source sets a
    floor for an injury-prevention-led athlete. The 120 upper bound does not
    rest on the Momma reversal claim, which failed checking; it rests on the
    30-year cohort in 02-climbing.md B4 (n=147,374, 35,798 deaths), where
    all-cause mortality risk plateaued at around >=120 min/wk with no further
    benefit beyond it, and 90-119 min/wk carried HR 0.87 (0.81-0.95).
    Verified 2026-08-13 against the primary source. Plateau, not reversal:
    the band's upper edge marks where the mortality evidence stops adding,
    not where it turns against.

- id: bouldering_counts_asymmetrically
  activation: discipline:climbing AND discipline:strength
  type: HARD
  confidence: CONTESTED (novel synthesis, no quantifying study)
  requires: [finger_sessions, strength_content]
  statement: >
    Hard bouldering is a near-maximal finger and pulling stimulus.
      COUNT IT toward: finger load, pulling/upper-limb pull strength.
      COUNT IT AS ZERO toward: lower body, push/antagonist, shoulder
      girdle, posterior chain, systemic strength dose.
    Two failure modes follow and both must be checked every week:
      over-loading — stacking hangboard or heavy pulling on top of hard
        bouldering, which is the documented finger-injury mechanism
      under-prescribing — assuming climbing covers upper body, leaving
        exactly the tissues with prevention rationale untrained
  source: 02-climbing.md B3, recommendation 2; contributing A3, A5, B2
  judgment_call: >
    Typed HARD on CONTESTED evidence. 02-climbing.md B3 labels the
    double-counting problem CONTESTED/NOVEL and states no study quantifies
    bouldering's strength-training equivalent. The asymmetric counting rule
    is a defensible synthesis, not a measured finding. Flagged in HANDOFF.md
    for revisit.

- id: strength_priority_order
  activation: discipline:cycling AND discipline:climbing
  type: SOFT
  confidence: CONSENSUS on rationale, CONTESTED on prevention magnitude
  requires: [strength_content]
  statement: >
    Prioritise what climbing does not train and what cycling loads
    repetitively:
      1. lower body / knee and quad tendon
      2. shoulder girdle and push
      3. posterior chain
      4. finger and pulling — only to the extent bouldering has not
         already supplied it
    Cycling and lower-body strength are synergistic, not competing
    (concurrent +8.4% mean power vs +3.7% endurance-only).
    The order is derived for the cycling-plus-climbing combination and does
    not load without both. For other combinations no priority order is
    supplied; strength_dose_target still applies.
  source: 02-climbing.md recommendation 7, B1, B2, B3

- id: antagonist_work_is_rationale_based
  activation: discipline:climbing
  type: DISCLOSURE
  confidence: PRACTITIONER
  statement: >
    Include shoulder-girdle and antagonist work — low cost, mechanistic
    support — but do not present it as outcome-proven. The only
    injury-outcome evidence is a single cohort of 18-19 year old male
    students, and the intervention tested was closed-chain plus eccentric
    plus proprioceptive work, not antagonist isolation.
  source: 02-climbing.md B2, recommendation 9
```

## 3. STRENGTH — SESSION CONTENT

Section 2 sets how much strength work and which tissues get priority. This
section sets what goes in the session. It does not restate the dose target.

```yaml
- id: load_magnitude_over_exercise_identity
  activation: discipline:strength
  type: SOFT
  confidence: CONSENSUS
  statement: >
    For maximal strength and for tendon adaptation, load magnitude drives the
    outcome more than which exercise delivers it. Whole-muscle hypertrophy is
    load-flexible and achievable by many exercises provided sets approach
    failure. This does not license free substitution: see
    region_specific_hypertrophy and strength_transfer_is_exercise_specific
    for the two places identity does matter.
    Refined by ACSM 2026 on two points. First, the failure qualifier: reaching
    momentary muscular failure is not required for either outcome — strength
    not affected (3 reviews, n=1,371, QoE 83%), hypertrophy not affected
    (4 reviews, n=800, QoE 69%). Read "approach failure" as near-failure, not
    to failure. Second, full range of motion is a second execution variable
    that does affect strength independently of which exercise delivers the
    load (2 reviews, n=1,262, QoE 50%) — identity-independent does not mean
    execution-independent.
  caveat: >
    ACSM 2026 could not quantify exact RIR or perceived-exertion targets; its
    2-3 RIR figure is the authors' own proposal, not a synthesised threshold,
    and is labelled PRACTITIONER in the source. Its evidence base is
    predominantly novice trainees by the authors' own statement, and
    DOSSIER.md records no resistance-training age, so the near-failure
    framing is not calibrated to a known training status here.
  source: 03-session-prescription.md C1, C2; 04-acsm-rt.md A1, A2, B2, C1

- id: region_specific_hypertrophy
  activation: discipline:strength
  type: SOFT
  confidence: CONSENSUS
  statement: >
    Regional and architectural growth is exercise-specific even where whole
    muscle growth is not. Leg extension grew rectus femoris +8.8-19.7% across
    regions where back squat did not (-2.2 to +3.0%) at matched volume and
    intensity — 5 weeks, resistance-profile-confounded by the authors' own
    caveat. Deep squats grew glute max 7% vs 2% and adductors 6% vs 3% versus
    half squats. Squat and hip thrust grew glutes similarly, but squat was
    superior for quads (delta 3.6 cm2, CI 0.7-6.4) and adductors (2.5, CI
    1.2-3.9). Only preacher curl, at long muscle length, grew distal biceps
    significantly.
  source: 03-session-prescription.md C1

- id: strength_transfer_is_exercise_specific
  activation: discipline:strength
  type: SOFT
  confidence: CONSENSUS
  statement: >
    Strength transfer is highly specific to the trained movement: squat 3RM
    favoured the squat group by 14+/-2 kg, hip thrust 3RM favoured the hip
    thrust group by 26+/-5 kg. "Any progressive loading" does not suffice to
    maximise a named strength outcome. Where a rule targets a specific
    capacity, the exercise is part of the prescription, not a detail.
  source: 03-session-prescription.md C1

- id: emg_does_not_select_exercises
  activation: discipline:strength
  type: HARD
  confidence: CONSENSUS
  statement: >
    Acute surface EMG is not a validated predictor of longitudinal
    hypertrophic adaptation. Do not select, rank or justify an exercise on
    activation data, and do not repeat activation claims sourced from
    elsewhere.
  source: 03-session-prescription.md C1

- id: exercise_variation_is_systematic
  activation: discipline:strength
  type: SOFT
  confidence: CONSENSUS
  statement: >
    Vary exercises on anatomical or biomechanical grounds — a region or
    function not otherwise loaded — not for novelty. Redundant or excessive
    rotation adds no hypertrophy benefit.
  source: 03-session-prescription.md C1

- id: heavy_load_required_for_max_strength
  activation: discipline:strength
  type: HARD
  confidence: CONSENSUS
  statement: >
    Maximal strength requires heavy load; hypertrophy does not. Meta-analysis
    of 21 studies, all sets to failure: 1RM favoured high load (>60% 1RM)
    ES=0.58 (95% CI 0.28-0.89, p=0.002); isometric strength no difference;
    hypertrophy no difference (ES diff 0.03, 95% CI -0.16 to 0.22).
    Heterogeneity for the strength outcome was high (I2 ~80%). Strength
    retention and tendon are the reasons heavy load is non-negotiable in the
    key lifts; hypertrophy volume is the part that can flex.
    ACSM 2026 narrows the load threshold to >=80% 1RM with a stated
    dose-response (6 reviews, n=6,574, QoE 79%); the previous figure carried
    here was >60% 1RM from Schoenfeld 2017. It also widens the hypertrophy
    load-indifference finding to the full 30%-100% 1RM range (8 reviews,
    n=5,340, QoE 66%), where the previous basis was a null difference within
    the Schoenfeld comparison. Direction unchanged, both bounds better
    supported.
  caveat: >
    The >=80% 1RM figure comes from an evidence base the ACSM authors state is
    predominantly inexperienced trainees. DOSSIER.md records no
    resistance-training age, so it is not established that this athlete is the
    population the number was derived in. Treat >=80% as the better-supported
    threshold for the key lifts, not as a reason to raise a working load that
    is already producing strength gains.
  source: 03-session-prescription.md C2; 04-acsm-rt.md A1, B2, B3

- id: tendon_needs_high_strain
  activation: discipline:strength AND NOT state:rehab
  type: HARD
  confidence: CONSENSUS
  statement: >
    Tendon adaptation depends on loading magnitude, not contraction type.
    Meta-analysis, 27 studies / 37 interventions / 264 participants:
    stiffness SMD=0.70 (95% CI 0.51-0.88), Young's modulus 0.69 (0.36-1.03),
    CSA 0.24 (0.07-0.42). The characterised stimulus is ~90% MVC, 4.5-6.5%
    tendon strain, 3-s contractions, ~5x4 reps, sustained beyond 12 weeks;
    ~3% strain does not adapt tendon at all. Most stiffness change occurs in
    the first ~8 weeks. Low-load high-rep work maintains muscle and does not
    maintain tendon.
    Loads the lower-limb structural axis — see separate_load_axes; it is not
    free alongside cycling volume.
  caveat: >
    Parameters derive largely from one group's intervention series
    (Arampatzis/Bohm); trials rarely exceed 14 weeks.
  gated_because: >
    A rehab case may involve a lower-limb tendon and may not be
    clinician-assessed. A 90% MVC prescription is exactly what
    clinician_sets_dosage forbids the assistant from inventing. Do not read
    this rule in rehab.
  source: 03-session-prescription.md C2

- id: isometrics_are_analgesia_not_stiffness
  activation: discipline:strength
  type: DISCLOSURE
  confidence: CONSENSUS
  statement: >
    The isometric-holds evidence is tendinopathy pain relief (~45 min
    post-exercise), not healthy-state tendon adaptation. It does not
    replicate at the Achilles and failed to show analgesia in some patellar
    samples. For healthy-state stiffness, isometric versus dynamic does not
    matter — load magnitude does. Do not import rehab loading protocols into
    healthy-state prescription, and do not present isometrics as a stiffness
    intervention.
  source: 03-session-prescription.md C1, C2

- id: nordic_hamstring_dose_is_low
  activation: discipline:strength
  type: SOFT
  confidence: CONSENSUS
  statement: >
    Nordic hamstring work lengthens biceps femoris long-head fascicles
    distally and raises eccentric strength at low volumes: +28%+/-20%
    (d=1.55) high-volume versus +34%+/-14% (d=2.09) low-volume over 6 weeks,
    with meta-analytic support that low volumes suffice. Architectural gains
    detrain within ~2 weeks; strength persists >=4 weeks. Prescribe the low
    dose and keep it continuous rather than prescribing a large dose
    intermittently.
  source: 03-session-prescription.md C1

- id: no_overhead_selection_evidence
  activation: discipline:strength
  type: DISCLOSURE
  confidence: NO EVIDENCE (no healthy-adult selection study exists)
  statement: >
    No healthy-adult exercise-selection evidence exists for the shoulder
    girdle or overhead press. Any progressive overhead or push loading is
    defensible by general principle only. Say that rather than presenting a
    selection as evidence-led. This is the tissue strength_priority_order
    ranks second and bouldering_counts_asymmetrically counts as zero, so it
    must be prescribed — the absence is in the choice of exercise, not in
    whether to train it.
  source: 03-session-prescription.md C1

- id: minimum_effective_strength_dose
  activation: discipline:strength
  type: SOFT
  confidence: CONSENSUS
  requires: [lift_loads, strength_minutes]
  statement: >
    Low volume preserves and can still build strength. Minimum effective
    training dose for 1RM in trained lifters is ~3-6 working sets per week
    per lift, 1-5 reps, >80% 1RM, RPE 7.5-9.5, over 6-12 weeks; a single set
    of 6-12 reps at 70-85% 1RM twice or three times weekly produces
    sub-optimal but statistically significant 1RM gains. Twice weekly beats
    once weekly. Hypertrophy maintenance runs ~6-10 sets per muscle per week.
    This is a floor for constrained weeks, not a target — it does not replace
    strength_dose_target's 60-120 min/week operating band.
    ACSM 2026 refines three of these numbers. Frequency: >=2 sessions/wk
    confirmed (4 reviews, n=3,531, QoE 69%), with the upper limit explicitly
    undeterminable and the frequency effect diminishing when volume is
    equated. Strength volume: 2-3 sets/session, with a meta-regression
    plateau and diminishing returns beyond ~2-3 sets/exercise (7 reviews,
    n=5,633, QoE 71%) — compatible with and narrower than the ~3-6 sets/week
    per lift carried here. Hypertrophy: growth is dose-responsive at >=10
    sets/muscle/week with diminishing returns beyond ~18-20 weekly sets;
    the ~6-10 sets/muscle/week figure here is a maintenance floor and sits
    below that growth threshold, which is consistent, not contradictory.
  caveat: >
    METD studies are dominated by young male powerlifters; women and masters
    athletes are under-studied.
    Two limits on the ACSM 2026 numbers. Its evidence base is predominantly
    novice trainees by the authors' own statement, while this rule is
    explicitly scoped to trained lifters — the set counts are therefore not
    a like-for-like replacement for the METD figures and are recorded
    alongside them, not over them. And ACSM 2026 states there was
    "insufficient evidence to form recommendations on emerging RTx
    strategies", naming minimal-dose programmes specifically: it does not
    validate a minimum effective dose protocol. It also could not quantify
    exact RIR or RPE targets, so the RPE 7.5-9.5 band here remains the
    METD source's, unconfirmed by the position stand.
  source: 03-session-prescription.md C3; 04-acsm-rt.md A1, A3, B1, C1

- id: what_survives_a_cut_session
  activation: discipline:strength
  type: SOFT
  confidence: PRACTITIONER
  source_label: "evidence-informed (03 C3, verbatim)"
  statement: >
    When a session is cut short, in order: keep the heavy compound at target
    load, because strength and tendon depend on load magnitude and few sets
    suffice; drop accessory and isolation volume first, because hypertrophy
    tolerates volume reduction; preserve at least one high-strain exposure
    per target tendon. The high-strain exposure is what survives cutting
    last, not first.
    ACSM 2026 adds ordering and quantifies the asymmetry. Ordering: strength
    is enhanced when the exercise is performed at the beginning of the
    session rather than the end (4 reviews, n=941, QoE 88% — the highest-QoE
    strength finding in the position stand), while hypertrophy is unaffected
    by exercise order (4 reviews, n=759, QoE 81%). So the heavy compound goes
    first by default, not merely survives the cut. Asymmetry: strength
    saturates on volume at ~2-3 sets/exercise, whereas hypertrophy is
    dose-responsive to ~18-20 weekly sets — which is why accessory volume is
    the correct thing to drop first and why doing so costs hypertrophy rather
    than strength.
  caveat: >
    ACSM 2026 has no tendon outcome of any kind, so the high-strain clause
    is unaffected by it and continues to rest on 03-session-prescription.md
    C2. Its evidence base is predominantly novice trainees.
  judgment_call: >
    The prioritisation is this repo's synthesis. Its components are
    CONSENSUS findings — strength and tendon adaptation depend on load
    magnitude, hypertrophy tolerates volume reduction
    (03-session-prescription.md C2, C3) — but no study tests the order of
    what to drop from a cut session. The source labels it "evidence-informed", outside the label
    vocabulary; PRACTITIONER is the label for an ordering assembled from
    findings rather than tested as one. source_label: keeps the source's own
    wording.
  source: 03-session-prescription.md C3; 04-acsm-rt.md A1, A3, B1, B2, B3
```

## 4. CLIMBING

```yaml
- id: finger_session_spacing
  activation: discipline:climbing
  type: HARD
  confidence: PRACTITIONER (mechanistically grounded)
  requires: [finger_sessions]
  statement: >
    At least 48 h between hard finger sessions, counting bouldering and
    hangboard as the same category. Collagen synthesis stays elevated ~72 h
    with a net-catabolic window in the first ~24-36 h. The 48 h number is
    extrapolated from collagen turnover, not from a climbing trial.
  source: 02-climbing.md A6, A4, recommendation 3

- id: hangboard_displaces_never_adds
  activation: discipline:climbing
  type: HARD
  confidence: CONTESTED
  requires: [finger_sessions, planned_sessions]
  statement: >
    Structured finger training is added by displacing climbing finger
    volume, never by stacking on top of it. The dominant injury mechanism is
    the total finger-loading frequency spike (2-3 to 5-6 sessions/week), not
    the tool itself. Effectiveness is established (max hangs +34% grip
    endurance; repeaters +45%; low-intensity and max hangs roughly additive,
    combined d=0.79); protocol specifics — set counts, 7/3 repeaters, 20 mm
    edge — are convention, not validated.
  source: 02-climbing.md A5, recommendation 4

- id: structural_lag_fingers
  activation: discipline:climbing
  type: HARD
  confidence: CONSENSUS
  statement: >
    Finger strength can outrun connective-tissue readiness over weeks to a
    few months. Neural gains bank in ~4 weeks; pulley and tendon structural
    adaptation runs months to years (A2 pulleys 62-69% thicker only after
    15+ years). Never pace finger-load progression by how strong the fingers
    feel.
  source: 02-climbing.md A4

- id: crimp_exposure
  activation: discipline:climbing
  type: SOFT
  confidence: CONSENSUS
  requires: [finger_sessions]
  statement: >
    Crimp grip is an identified risk factor. Force on A2 rises ~31.5x and
    A4 ~3.9x versus open-hand. Recreational finger-flexor force can exceed
    the ~407 N cadaver failure load of A2. Treat sustained crimp-heavy
    blocks as elevated exposure, not neutral volume.
  source: 02-climbing.md A2, A3

- id: climbing_in_pain_flag
  activation: discipline:climbing
  type: HARD
  confidence: CONSENSUS
  requires: [pain_report]
  statement: >
    Previous injury and climbing while in pain are the strongest modifiable
    risk markers in the climbing literature. Climbing in pain is a stop
    condition, not a tolerance to be managed.
  source: 02-climbing.md A3, recommendation 5

- id: bouldering_acute_risk
  activation: discipline:climbing
  type: DISCLOSURE
  confidence: CONSENSUS
  statement: >
    Bouldering carries roughly 5x the injury incidence of roped climbing
    (1.47 vs 0.29 per 1000 h). Acute mechanism is falls to the mat — ankle
    and knee. This is exposure, not something load management addresses.
  source: 02-climbing.md A2
```

## 5. CYCLING

```yaml
- id: bike_load_is_the_reliable_one
  activation: discipline:cycling
  type: SOFT
  confidence: CONSENSUS
  requires: [activity_log, fitness_load]
  statement: >
    Power-based cycling load is the most trustworthy dose index available.
    Weight it highest for systemic load; weight climbing and running data
    higher for injury risk.
  source: 01-endurance.md 3.1, cross-cutting recommendation 3

- id: cycling_knee_is_the_overuse_site
  activation: discipline:cycling
  type: SOFT
  confidence: CONSENSUS
  requires: [activity_log]
  statement: >
    Anterior knee pain and patellar/quadriceps tendinopathy dominate cycling
    overuse and cause the greatest time loss. Volume spikes are a named
    trigger. Cadence above ~80-90 rpm and avoiding sustained big-gear work
    have the strongest cycling-specific support.
  source: 02-climbing.md B1; 01-endurance.md 7.3

- id: bike_fit_framing
  activation: discipline:cycling
  type: DISCLOSURE
  confidence: CONTESTED
  statement: >
    Do not present bike fit as evidence-based injury prevention — moderate
    evidence of no association for seat height, knee angle and
    knee-over-pedal-spindle. This does NOT extend to troubleshooting: a
    position change that preceded symptom onset is a suspected cause and
    reverting it is ordinary diagnosis, a different claim entirely.
  source: 01-endurance.md 7.3, 7-recommendation 8

- id: cp_protocol_fixity
  activation: discipline:cycling
  type: DISCLOSURE
  confidence: CONSENSUS
  requires: [sport_thresholds]
  statement: Only compare CP/W' values obtained under an identical protocol.
  source: 01-endurance.md 3.1
```

## 6. CYCLING — INTERVAL PRESCRIPTION

Session-level intensity prescription. The distribution question is `tid_flexible`
in section 10 and is not reopened here — these rules govern the content of a
quality session, not how many of the week's hours are hard.

```yaml
- id: short_interval_default
  activation: discipline:cycling AND NOT state:rehab
  type: SOFT
  confidence: CONTESTED
  requires: [sport_thresholds]
  statement: >
    Default to short on-off intervals (30/15 or 40/20, series format) over
    effort-matched long intervals for a VO2max block. In well-trained
    cyclists short intervals gave +8.7% VO2max versus +2.6% for 4x5 min at
    matched total effort. State the limit when using it: in elite cyclists
    the same comparison produced superior peak power and 20-min power but no
    significant VO2max difference, so the advantage expressed as performance,
    not as measured VO2max. Blocks run 4-6 weeks.
  caveat: >
    Findings come from 3-10 week blocks from one research group; durability
    and generalisation are unconfirmed.
  revisit_if: >
    within-athlete A/B shows long intervals give at least equal VO2max/PPO
    gain at lower session RPE
  source: 03-session-prescription.md A1, recommendation 1

- id: interval_family_not_determinative
  activation: discipline:cycling
  type: DISCLOSURE
  confidence: CONSENSUS
  statement: >
    Interval prescription cannot be explained by interval type or work-bout
    duration alone. In endurance-trained cyclists both HIIT and SIT are
    effective, with effects versus control ranging from trivial (relative
    VO2max g=0.10, 95% CI -0.34 to 0.54) through small (absolute VO2max
    g=0.28, 0.15-0.40; MAP/PPO g=0.38, 0.15-0.61) to large but very imprecise
    (TT/TTE g=0.96, 95% CI -0.81 to 2.73). Sprint repetition count per
    session did not moderate VO2max change across 93 trials (n=1188) —
    more reps is not more adaptation. Do not present a chosen protocol as
    the correct one; it is a defensible default.
  caveat: >
    Much SIT and HIIT effect-size data rests on 2-10 week studies in
    sedentary or recreationally active subjects. Transfer to a trained
    cyclist, and to masters athletes in particular, is assumed, not
    demonstrated.
  source: 03-session-prescription.md A1

- id: time_near_vo2max_is_a_convention
  activation: discipline:cycling
  type: DISCLOSURE
  confidence: CONTESTED
  statement: >
    Time at or above 90% VO2max is an organising convention for designing
    sessions, not a validated dose metric that predicts adaptation magnitude.
    The within-athlete test is weak and split: one study found a higher
    fraction of VO2max during intervals correlated with performance gains
    across 21 power-matched sessions over 9 weeks; earlier work found time
    >=90% VO2max did not correlate with improvements in maximal velocity or
    power at 4 mmol/L. Reviews call the evidence ambiguous. Use it to reason
    about session structure; never report it as a dose achieved.
  source: 03-session-prescription.md A2

- id: time_near_vo2max_manipulations
  activation: discipline:cycling AND NOT state:rehab
  type: SOFT
  confidence: CONSENSUS on the manipulations, CONTESTED on set-structure interaction
  statement: >
    What raises time near VO2max: shorter recoveries relative to work (30/15
    accumulates more than 4x5 min); a fast-start first bout (90 s hard, then
    lower power) versus constant pacing; adequate but incomplete recovery.
    The interaction is non-monotonic — intensified 30-s intervals were
    inferior to traditional 3-min intervals for time >90% VO2max because the
    higher intensity cut total repetitions (11 versus 24, ~65% less time
    >90%). Raising intensity is not a reliable way to raise time near VO2max.
  source: 03-session-prescription.md A2

- id: two_quality_sessions_default
  activation: discipline:cycling AND NOT state:rehab
  type: SOFT
  confidence: CONSENSUS
  requires: [activity_log, planned_sessions, time_in_zone]
  statement: >
    Two quality sessions per week is the default. A third gives no clear
    additional VO2max benefit in recreational athletes, with the largest
    effects (d>0.5) in the two- and three-times groups of a 6-week
    once/twice/thrice design. Cyclist series used 2-3 per week. A third
    session is an available dose escalation under plateau_order_of_operations,
    not a starting prescription.
  source: 03-session-prescription.md A3, recommendation 1

- id: minimum_effective_interval_dose
  activation: discipline:cycling
  type: DISCLOSURE
  confidence: CONSENSUS
  statement: >
    A single 4-min bout at 90% HRmax three times weekly raised VO2max ~10%
    (~5.0 mL/kg/min) versus ~13% (~6.5) for 4x4-min, between-group p=0.08.
    Useful as the floor in a compressed week, and as the honest answer to
    "what is the least that works". Subjects were inactive overweight men
    over 10 weeks — the gap to a trained cyclist is large.
  source: 03-session-prescription.md A3

- id: anchor_short_intervals_to_power
  activation: discipline:cycling
  type: HARD
  confidence: CONSENSUS
  requires: [sport_thresholds]
  statement: >
    Anchor efforts shorter than ~2-3 min to power with RPE as live override.
    Never anchor them to heart rate: HR takes 30-60 s to stabilise and is a
    lagging indicator over that duration. Working ranges: VO2max intervals
    ~106-120% FTP, threshold ~95-105%, sweet spot ~84-94%. Above ~3 min HR is
    usable once stabilised, and for lactate-threshold intervals specifically
    HR- and power-anchored training produced statistically indistinguishable
    gains — the prohibition is duration-scoped, not a claim that power is
    always superior. Where power is unavailable, substitute RPE and terrain,
    not HR.
  caveat: >
    FTP is not a valid maximal-metabolic-steady-state marker;
    time-to-exhaustion at FTP averages ~33 min, not 60. It is an anchor of
    convenience. See cp_protocol_fixity before comparing values across dates.
  source: 03-session-prescription.md A4, recommendation 2

- id: w_prime_balance_is_supplementary
  activation: discipline:cycling
  type: SOFT
  confidence: CONSENSUS for exhaustion prediction under tested conditions
  requires: [sport_thresholds]
  statement: >
    W'-balance is validated for predicting exhaustion in intermittent efforts
    and has been used to build sessions that fully deplete W' (+5% CP over 4
    weeks, +9%/+4%/+5% at 12/7/3-min power). Use it as a supplementary pacing
    check, not as primary prescription. The model's own authors warn it can
    predict recovery where none should occur outside tested conditions;
    reconstitution kinetics are curvilinear and highly individual. Do not
    extrapolate it to novel work-to-recovery structures.
  source: 03-session-prescription.md A4

- id: sweet_spot_is_time_efficiency
  activation: discipline:cycling
  type: HARD
  confidence: CONSENSUS
  statement: >
    Threshold and sweet-spot work is a time-efficiency tool: high stimulus
    per hour, lower fatigue cost than VO2max work, repeatable 2-3x/week, and
    it drives power at fixed lactate concentrations. There is no strong
    evidence it produces a unique adaptation unobtainable from high easy
    volume plus true VO2max work. Prescribe it for constrained weeks and say
    that is why. Do not present it as a distinct adaptive stimulus — the
    coaching claim of a special adaptive window has outrun the controlled
    literature.
  revisit_if: >
    matched-load session-level trial demonstrates a unique sweet-spot
    adaptation
  source: 03-session-prescription.md B1, recommendation 7

- id: polarized_evidence_is_distribution_level
  activation: discipline:cycling
  type: DISCLOSURE
  confidence: CONTESTED
  statement: >
    The trials used to argue sweet spot is grey-zone compared distributions,
    not sessions: ~8% peak-power gain polarized versus ~3% threshold, and
    ~11.7% VO2peak for polarized over threshold, HIIT and high-volume groups
    in well-trained athletes. The comparison arms used threshold volumes no
    competent coach prescribes alone, and subjects already carried
    substantial base volume. Real but contextual. This does not license
    reopening the distribution question — see tid_flexible.
  source: 03-session-prescription.md B1

- id: sustainable_power_moves_by_several_routes
  activation: discipline:cycling
  type: DISCLOSURE
  confidence: CONSENSUS
  statement: >
    No single session type owns FTP/CP improvement. W'-depleting mixed
    intervals gave +5% CP in 4 weeks; 4x8-min threshold intervals twice
    weekly moved power at OBLA (222 to 239 W in one arm), with TTE change
    correlating with change in power at 4 mmol/L (r=0.66, p<0.001);
    HR- and power-anchored LT intervals both gave +9.8% LT power (~17 W) and
    -7.8% 20-km TT over ~5 weeks with no anchor-method difference. No
    session-level RCT isolates sweet-spot versus threshold versus Z2-plus-HIIT
    at matched load, and FTP's construct validity confounds the estimates.
  source: 03-session-prescription.md B2

- id: heavy_strength_improves_cycling_without_vo2max
  activation: discipline:cycling AND discipline:strength
  type: DISCLOSURE
  confidence: CONSENSUS (low certainty of evidence)
  statement: >
    Heavy strength training improves cycling performance through efficiency
    (ES=0.353, p=0.012) and anaerobic power (ES=0.560, p=0.024), performance
    ES=0.463 (p=0.016), without changing VO2max, pVO2max or MLSS. The route
    is distinct from the concurrent mean-power finding in
    strength_priority_order. Consequence for review periods: strength work
    can pay off in performance while every aerobic marker sits flat — do not
    read that as non-response.
  source: 03-session-prescription.md B2

- id: concurrent_endurance_frequency_cap
  activation: discipline:cycling AND discipline:strength
  type: SOFT
  confidence: CONSENSUS
  requires: [activity_log, planned_sessions, lift_loads]
  statement: >
    Strength and hypertrophy are largely preserved when endurance is <=3
    sessions/week and sessions are separated. Interference was found with
    running but not cycling, so an athlete whose endurance volume is
    cycling is comparatively protected. Sequence is not the leading
    driver of interference over blocks of 8 weeks or more. If strength
    stalls despite separation, reduce concurrent endurance frequency before
    reducing the strength dose — see interference_is_smaller_than_assumed.
    Scheduling within the day is governed by session_ordering and
    strength_cycling_same_day_order.
  source: 03-session-prescription.md A3, recommendation 6

- id: strength_cycling_same_day_order
  activation: discipline:cycling AND discipline:strength
  type: SOFT
  confidence: CONSENSUS that separation matters, CONTESTED on order
  requires: [planned_sessions, block_focus]
  statement: >
    Separation beats either order — both reviews agree, and intra-session
    sequence is not the leading driver of interference over blocks of 8 weeks
    or more. Default to separate days; failing that, at least 3 h apart.
    Where same-day stacking is unavoidable, order by the adaptation the
    current block is protecting:
      strength-focused phase — strength first
      cycling build phase — cycling first
    Phase context is the legitimate moderator because the two source rules
    answer different questions. session_ordering is about knee and quad load
    accumulated under fatigue; this review is about molecular interference
    (AMPK returns to baseline ~3 h, mTORC1 stays elevated ~18 h). Neither
    answer generalises to the other's question, so neither is simply wrong.
    Moot while rehab mode governs and the case involves the knee or quad
    tendon: rehab_mode_supersedes controls, and that is the tissue both
    orderings are arguing about.
  source: >
    02-climbing.md B5, recommendation 8 (via session_ordering);
    03-session-prescription.md A3, recommendation 6 (via
    concurrent_endurance_frequency_cap)
```

## 7. RUNNING

```yaml
- id: run_single_session_spike_cap
  activation: discipline:running
  type: HARD
  confidence: CONTESTED (strongest running injury datapoint)
  requires: [activity_log]
  statement: >
    No single run above 110% of the longest run in the prior 30 days.
    >10-30% HRR 1.64; >30-100% HRR 1.52; >100% HRR 2.28.
  source: 01-endurance.md 3.2, cross-cutting recommendation 3
  judgment_call: >
    Typed HARD on CONTESTED evidence. The 110% threshold and the hazard
    ratios trace to 01-endurance.md 3.2; promoting the strongest available
    running datapoint to a hard cap is a system decision, not a review
    finding. Flagged in HANDOFF.md for revisit.

- id: no_ten_percent_week_rule
  activation: always
  type: HARD
  confidence: CONSENSUS
  statement: >
    The weekly 10% rule is not evidence-based (GRONORUN null, 20.8% vs
    20.3%). Do not apply it to running or import it to climbing.
  source: 01-endurance.md 7.2, 3.2, 7-recommendation 4

- id: structural_lag_lower_limb
  activation: discipline:running
  type: SOFT
  confidence: CONSENSUS
  requires: [activity_log]
  statement: >
    Bone remodels over months; tendon stiffness adapts over 2-8 weeks with
    matrix maturation over months to years. Largely dormant at low run
    volume, reactivates immediately if run volume grows.
  source: 01-endurance.md 3.2
```

## 8. SCHEDULING

```yaml
- id: session_ordering
  activation: always
  type: SOFT
  confidence: PRACTITIONER (mechanistic extrapolation, no injury-outcome data)
  requires: [planned_sessions, activity_log, finger_sessions, strength_content]
  statement: >
    Each item applies only when the disciplines it names are in the dossier.
    - Never precede hard bouldering or max finger work with fatiguing
      pulling or hangboard work.
    - At least 48 h between hard finger sessions.
    - Do not stack heavy lower-body strength and hard cycling on the same
      day; if unavoidable, keep them at least 3 h apart and take the order
      from strength_cycling_same_day_order, which resolves it by block phase.
    - Keep occasional running away from heavy-leg and hard-cycling days —
      eccentric load adds to cumulative knee and tendon exposure.
    - At least 3 h between hard endurance and strength clears most molecular
      interference (AMPK returns to baseline ~3 h).
  source: 02-climbing.md B5, recommendation 8

- id: interference_is_smaller_than_assumed
  activation: discipline:cycling OR discipline:running
  type: DISCLOSURE
  confidence: CONSENSUS
  statement: >
    Concurrent training interference is body-part specific and modest;
    cycling interferes with strength far less than running does. Do not use
    interference as a reason to cut the strength dose.
  source: 02-climbing.md B3
```

## 9. PROGRESSION LOGIC

How a session changes over a block, and what to do when it stops working.
Progression of running volume is governed by section 7 and of climbing by
section 4; neither is reopened here.

```yaml
- id: no_session_level_interval_ramp_rate
  activation: discipline:cycling
  type: HARD
  confidence: CONTESTED/absent
  statement: >
    No session-level ramp-rate evidence exists for interval work. The
    conventions — 4x6 to 4x8 to 24 min at equal power, or repeating a session
    and raising average power — are folklore without controlled support, and
    published progression guidelines are acknowledged in the literature as
    vague and not supported by strong evidence. Do not invent a rate, do not
    import one from endurance load, and do not present a chosen progression
    as evidence-based. Same posture as no_climbing_ramp_threshold: progress
    conservatively and say the rate is a judgement call.
  revisit_if: controlled interval ramp-rate evidence published
  source: 03-session-prescription.md D1, recommendation 8

- id: progress_something_not_nothing
  activation: discipline:cycling AND NOT state:rehab
  type: SOFT
  confidence: CONTESTED/absent
  statement: >
    The absence of a validated rate is not an argument for holding a session
    constant. Progressively increasing intensity produced greater VO2peak and
    lactate-inflection gains than holding intensity constant over 6 weeks in
    previously sedentary subjects. That supports progressing, and says
    nothing about how fast. Direction is supported; rate is not.
  source: 03-session-prescription.md D1

- id: strength_progression_is_load
  activation: discipline:strength
  type: SOFT
  confidence: >
    CONSENSUS on load as the strength driver; CONTESTED on whether
    progression is needed at all
  requires: [lift_loads]
  statement: >
    Where continued strength gains are the aim, the lever is load, progressed
    within the >=80% 1RM range. Strength is enhanced by load >=80% 1RM with a
    dose-response (6 reviews, n=6,574, QoE 79%) [CONSENSUS]; it saturates on
    volume at ~2-3 sets/exercise [CONSENSUS]; and training to failure does
    not enhance it (3 reviews, n=1,371, QoE 83%) [CONSENSUS]. Adding reps,
    sets beyond that plateau, or proximity to failure is not the strength
    lever. See heavy_load_required_for_max_strength for why heavy load is
    held in the key lifts at all.
    Whether progression is needed is a separate question and is CONTESTED:
    ACSM 2026 states "progression is not necessary to achieve beneficial
    outcomes", and that increasing the stimulus is likely required only for
    continued longer-term progress [CONTESTED]; the authors frame continued
    progression as a personal decision [PRACTITIONER]. This rule says which
    lever, not that it must be pulled, and not how fast — see
    no_fixed_percentage_progression.
  caveat: >
    The >=80% 1RM evidence base is predominantly novice trainees by the
    ACSM authors' own statement, and DOSSIER.md records no
    resistance-training age. Do not raise a working load that is already
    producing strength gains on the strength of this rule alone.
  resolution: >
    Split from progress_effort_not_a_fixed_percentage on 2026-10-31,
    resolving the contradiction recorded against it from ACSM 2026. That rule
    said what progresses is "effort and proximity to failure and total
    volume — not necessarily absolute load", resting on Plotkin 2022 (load
    vs repetition progression equivalent at matched effort and volume).
    Plotkin 2022 is a hypertrophy result; 03-session-prescription.md D1
    labels it "Strength progression", and the old wording carried that
    across to strength. That generalisation was an error. ACSM 2026 finds
    strength load-driven (04-acsm-rt.md A1, B3) and failure not a driver
    (A2, C1). The review body of 03-session-prescription.md D1 is left
    unaltered as the historical record.
  source: 04-acsm-rt.md A1, A2, A3, B3, C1, C2; 03-session-prescription.md C2 (via heavy_load_required_for_max_strength)

- id: hypertrophy_progression_is_volume_and_effort
  activation: discipline:strength
  type: SOFT
  confidence: >
    CONSENSUS on load indifference and on failure not being required;
    CONTESTED on the volume threshold; no evidence for any exact RIR or RPE
    target
  requires: [lift_loads]
  statement: >
    For hypertrophy, what progresses is volume and sufficient effort, not
    load. Load progression and repetition progression produce equivalent
    hypertrophy when effort and volume are matched (Plotkin 2022)
    [CONSENSUS]. Hypertrophy is unaffected by load across 30%-100% 1RM
    (8 reviews, n=5,340, QoE 66%) [CONSENSUS]. Volume is the lever: >=10
    sets/muscle/week, dose-responsive (5 reviews, n=2,267, QoE 50%, one
    contributing review contrary) [CONTESTED], with diminishing returns
    beyond ~18-20 weekly sets [CONSENSUS].
    Failure is not required: hypertrophy is not affected by training to
    momentary muscular failure (4 reviews, n=800, QoE 69%) [CONSENSUS].
    Effort must be sufficient, but no exact RIR or perceived-exertion target
    is derivable from the evidence — ACSM 2026 states there is "insufficient
    evidence to quantify exact RIR and perceived exertion targets" [NO
    EVIDENCE]. Its 2-3 RIR figure is the authors' proposal [PRACTITIONER].
    Any RIR or RPE band used in a prescription is a convention and is
    presented as one.
  caveat: >
    ACSM 2026's evidence base is predominantly novice trainees. The volume
    threshold carries the weakest QoE of the hypertrophy findings.
  resolution: >
    Split from progress_effort_not_a_fixed_percentage on 2026-10-31. The
    hypertrophy finding that rule rested on (Plotkin 2022) stands and is
    corroborated by ACSM 2026 across 30%-100% 1RM. What changed: "proximity
    to failure" is no longer named as a thing that progresses. ACSM 2026
    finds failure is not a driver (04-acsm-rt.md B2, C1), that exact RIR
    targets cannot be quantified (C1), and its list of what progression acts
    on — load, volume, frequency, exercise selection, duration — omits
    proximity to failure (C2).
  source: 03-session-prescription.md D1; 04-acsm-rt.md B1, B2, B3, C1, C2

- id: no_fixed_percentage_progression
  activation: discipline:strength
  type: HARD
  confidence: CONSENSUS
  statement: >
    Never progress by a fixed weekly percentage. The 10%/week convention is
    practitioner folklore with no RCT derivation; no_ten_percent_week_rule
    already bars it for running volume, and this rule bars the general form
    for any tissue or discipline. ACSM 2026 prescribes no progression rate
    and states progression is not necessary to achieve beneficial outcomes
    [CONTESTED] — it corroborates the absence of a rate and supplies none.
  resolution: >
    The third part of progress_effort_not_a_fixed_percentage, split out on
    2026-10-31 with its content and type unchanged. ACSM 2026 did not
    contradict it (04-acsm-rt.md C2).
  source: 03-session-prescription.md D1, recommendation 8; 04-acsm-rt.md C2

- id: response_heterogeneity_is_real
  activation: discipline:cycling
  type: DISCLOSURE
  confidence: CONSENSUS
  statement: >
    Response to a standardised programme varies enormously between people.
    Across 481 sedentary adults over 20 weeks, VO2max response ranged from
    ~0 to >1.0 L/min around a mean of ~400 mL/min, with 2.5x more
    between-family than within-family variance; heritability of the response
    reached ~47% with ~28% maternal transmission. Non-responders appeared at
    all ages, sexes and ethnicities. A flat block is not evidence of an error
    in the plan, and a good block is not proof the plan was right.
  source: 03-session-prescription.md A5

- id: non_response_is_dose_dependent
  activation: discipline:cycling AND NOT state:rehab
  type: HARD
  confidence: CONSENSUS
  requires: [activity_log, vo2max]
  statement: >
    Non-response to a given dose is largely a dosing artefact. Prevalence
    fell 69% to 40% to 29% to 0% to 0% across 60/120/180/240/300 min/week,
    and adding 120 min/week for a further 6 weeks abolished non-response
    universally, driven largely by haemoglobin-mass gains (total Hb mass the
    strongest independent VO2max determinant, r_partial=0.49). Individuals
    non-responsive to one modality often respond to another, but dose is the
    more robust lever. Never label the athlete a non-responder, to a session
    type or in general, without having escalated dose first — and never
    present non-response as a fixed trait.
  source: 03-session-prescription.md A5, recommendation 3

- id: plateau_order_of_operations
  activation: discipline:cycling AND NOT state:rehab
  type: HARD
  confidence: CONSENSUS on dose increase, CONTESTED on protocol switch, PRACTITIONER on deload
  requires: [activity_log, planned_sessions, time_in_zone, mean_max_power, sport_thresholds, vo2max, measurement_error]
  statement: >
    On a flat response over a review period, work in this order and do not
    skip ahead:
      1. verify execution — easy days actually easy, sessions actually
         completed at target. A plan not followed is not a plan that failed.
      2. increase density or volume [CONSENSUS, best-supported]. Added weekly
         volume abolishes non-response; block-concentrated density raised
         VO2max where the same number of evenly-spaced sessions did not.
      3. switch protocol family, only after two successive dose escalations
         (~+120 min/week equivalent each) fail to move VO2max/CP beyond
         typical measurement error [CONTESTED] — a weaker lever than dose.
      4. deload, only if fatigue markers indicate fitness is being masked
         [PRACTITIONER]. Widely used and physiologically reasonable, with no
         direct RCT support for breaking a plateau. It is last because it is
         the least evidenced, not because it is the most drastic.
    Raising intensity at constant volume is [PRACTITIONER/limited evidence]
    and confounded with dose; it is not a separate step.
    Before step 2, check heavy_strength_improves_cycling_without_vo2max —
    aerobic markers can sit flat while performance moves.
  reconciles_with: >
    Review-checkpoint logic, when built. The checkpoint owns what counts as a
    review period, what "typical measurement error" is for this athlete's
    CP/FTP protocol, and how many blocks a plateau must persist. This rule
    owns only the order. If the checkpoint ever defines a shorter trigger
    than two escalations, the escalation count here wins.
  source: 03-session-prescription.md D2, A5, recommendation 3

- id: block_length_is_convention
  activation: discipline:cycling
  type: DISCLOSURE
  confidence: PRACTITIONER
  statement: >
    The 4-8 week block length for concentrating VO2max work is practitioner
    convention, not a tested optimum. Deload efficacy for breaking a plateau
    is untested. Say so when proposing a block structure.
  source: 03-session-prescription.md D2
```

## 10. GOAL AND EVENT DEFAULTS

Longevity defaults load on `dossier:goal=longevity`; taper rules on
`dossier:event_date`. With no goal declared, none of the goal-gated rules
load and `goal_type_branch` asks instead. `tid_flexible` encodes `CLAUDE.md`
position 2 and is gated only by endurance discipline, never by goal.
`detraining_curve` is physiology and loads for every athlete.

```yaml
- id: crf_is_the_lever_not_the_method
  activation: dossier:goal=longevity
  type: DISCLOSURE
  confidence: CONSENSUS
  statement: >
    Mortality benefit runs through achieving and holding high CRF (elite vs
    low aHR 0.20, no observed upper limit), largely independent of method.
    Do not argue for a specific intensity distribution on longevity grounds.
  source: 01-endurance.md 6.1, cross-cutting recommendation 6

- id: zone2_not_privileged
  activation: dossier:goal=longevity
  type: DISCLOSURE
  confidence: PRACTITIONER
  statement: >
    Zone 2 is not uniquely optimal for longevity. High intensity also drives
    mitochondrial adaptation. Use Zone 2 because it builds CRF cheaply.
  source: 01-endurance.md 6.2

- id: tid_flexible
  activation: discipline:cycling OR discipline:running OR discipline:swimming
  type: SOFT
  confidence: CONTESTED
  requires: [time_in_zone, sport_thresholds, lt1_boundary]
  statement: >
    Pyramidal-leaning default, ~75-80% below LT1. Do not optimise this axis;
    POL vs PYR meta-analyses are split.
  source: 01-endurance.md 2.1, 2.2, 2.4, cross-cutting recommendation 2

- id: no_extreme_volume_push
  activation: dossier:goal=longevity
  type: SOFT
  confidence: CONTESTED
  requires: [activity_log]
  statement: >
    Do not ramp toward very high lifelong endurance volume (AF OR ~2.34;
    elevated CAC in older male masters athletes). State the counterweight:
    the two largest CRF-mortality cohorts found no excess mortality at
    extreme fitness. A reason not to chase volume, not to fear training.
  source: 01-endurance.md 6.5, 6.6

- id: no_taper_by_default
  activation: dossier:goal=longevity AND NOT dossier:event_date within 21d
  type: SOFT
  confidence: CONSENSUS
  statement: Longevity-led training needs no taper or peak.
  source: 01-endurance.md 6.6

- id: taper_when_event_present
  activation: dossier:event_date within 21d
  type: SOFT
  confidence: CONSENSUS
  requires: [activity_log]
  statement: >
    2 weeks, exponential fast-decay, volume cut 41-60%, intensity and
    frequency held. Expected gain ~2-3%.
  source: 01-endurance.md SECTION 5, cross-cutting recommendation 5

- id: detraining_curve
  activation: always
  type: SOFT
  confidence: CONSENSUS
  requires: [activity_log]
  statement: >
    After a break assume near-linear VO2max loss from within days, up to
    -20% by 12 weeks. Rebuild against structural rules, not remembered
    fitness.
  source: 01-endurance.md 6.4
```

## 11. PROHIBITIONS

```yaml
- id: prohibited_claims
  activation: always
  type: HARD
  confidence: CONSENSUS
  never_present_as_evidence_based:
    - static stretching, foam rolling, compression as injury prevention
    - the weekly 10% rule
    - ACWR as an injury predictor
    - bike fit as injury prevention (troubleshooting excepted, see rule)
    - dryland shoulder programs as swim injury prevention
    - antagonist training as proven climbing injury prevention
    - any specific climbing load-progression threshold
    - any wearable or ML injury-prediction output as validated
    - sweet spot as a distinct adaptive stimulus
    - time near VO2max as a validated dose metric
    - EMG activation as an exercise-selection criterion
    - any fixed weekly progression percentage, for any tissue or discipline
  permitted_framing: >
    Offer as preference-based recovery or comfort measures, labeled as such.
    The four session-prescription entries have a narrower permitted framing:
    sweet spot may be prescribed as a time-efficiency tool, time near VO2max
    may be used to reason about session structure, and progression may be
    proposed as an explicit judgement call. Each is permitted as a stated
    convention and prohibited as a validated finding. EMG has no permitted
    framing — it does not predict the outcome it is cited for.
  source: 01-endurance.md 1.4, 3.2, 7.1, 7.2, 7.3, 7.4, 7.7, 7-recommendations 2, 4, 7, 8; 02-climbing.md A3, B2, recommendation 9; 03-session-prescription.md A2, B1, C1, D1
```

## 12. DOSSIER-GATED

```yaml
- id: previous_injury_weighting
  activation: dossier:injury_history
  type: HARD
  confidence: CONSENSUS
  requires: [activity_log]
  statement: >
    Previous injury is the dominant predictor of recurrence in both running
    and climbing. Any listed site caps progression on the loading pattern
    that caused it.
  source: 01-endurance.md 7.2, 7-recommendation 3; 02-climbing.md A3

- id: bsi_history_pathway
  activation: dossier:bsi_history
  type: HARD
  confidence: CONSENSUS
  statement: >
    High-risk sites (femoral neck, anterior tibial shaft, tarsal navicular,
    5th metatarsal) require conservative site-specific timelines.
  source: 01-endurance.md 7.6, 7-recommendation 6

- id: underfuelling_check
  activation: dossier:fuelling_flag OR before load increase
  type: HARD
  confidence: CONSENSUS
  requires: [fuelling_status, fitness_load]
  statement: >
    Low energy availability affects both sexes and substantially elevates
    bone stress injury risk. If intake is not keeping pace with rising load,
    the load does not rise. Stop condition, not an optimisation.
  source: 01-endurance.md 7.6, 7-recommendation 6

- id: goal_type_branch
  activation: NOT dossier:goal
  type: BRANCH
  confidence: N/A (architectural)
  statement: >
    No goal is declared in the dossier. The goal-gated rules —
    crf_is_the_lever_not_the_method, zone2_not_privileged,
    no_extreme_volume_push, no_taper_by_default — do not load. Ask the
    athlete for their goal before any recommendation that depends on it. Do
    not infer the goal from training data, and do not default to longevity:
    an unanswered field is unanswered, not longevity.
    Recommendations that do not depend on goal proceed; the rules encoding
    the CLAUDE.md positions load regardless.
  judgment_call: >
    Architectural, not derived from any review. Goal moved from CLAUDE.md
    to the dossier when the repo was generalised; this rule keeps an empty
    goal field from being silently read as any particular goal.

- id: sleep_as_modifier
  activation: dossier:sleep_logged
  type: SOFT
  confidence: CONSENSUS in adolescents, thin in adults
  requires: [sleep_duration]
  statement: >
    Sustained sleep below ~7-8 h is a load-reduction signal, not a rest-day
    trigger on its own.
  source: 01-endurance.md 7.6, 7-recommendation 6
```

## 13. STATE HANDOFF

```yaml
- id: rehab_mode_supersedes
  activation: always
  type: HARD
  confidence: N/A (architectural)
  statement: >
    When rehab mode is active, REHAB.md governs and the progression rules in
    this file are subordinate to it. Plan generation does not resume on its
    own — see REHAB.md exit conditions.
  judgment_call: >
    Architectural, not derived from any review. REHAB.md defines the state
    and its constraints; this rule only routes to it. No review section
    covers state handoff, so there is nothing to cite.
```
