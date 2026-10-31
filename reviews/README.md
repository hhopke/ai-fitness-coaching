# reviews

Source evidence reviews. Rules in `RULES.md` cite section numbers back to these
files via their `source:` field; a rule whose provenance is unverifiable is not
usable.

## Naming

`NN-topic.md`, numbered in the order the reviews were produced. A new review
takes the next free number and keeps its topic slug. Numbers are never reused
or reordered — `source:` fields cite the filename, so renaming a review breaks
every rule that cites it.

## Contents

| File | Covers | Cite sections as |
| --- | --- | --- |
| `01-endurance.md` | Load–adaptation framework, intensity distribution and periodization, sport-specific deviations, multisport combination, taper, longevity, injury prevention | `1.1` … `7.7` |
| `02-climbing.md` | Climbing and bouldering load and injury; resistance training for injury prevention in this discipline combination | `A`, `B` and their subsections |
| `03-session-prescription.md` | Session-level prescription: cycling intervals, strength session content, progression logic | `A1` … `D2`, `recommendation N` |
| `04-acsm-rt.md` | ACSM 2026 Position Stand (Currier et al.): resistance training prescription variables for strength, hypertrophy, power, physical function. Single-source extraction, not a research pass | `A1` … `F3` |

`04-acsm-rt.md` extracts a CC BY-NC-ND source. It is kept to citations,
numeric findings and short marked quotations; the source's licence applies to
the quoted material.

`01-endurance.md` was assembled from two artifacts — sections 1-6 and section 7
(injury prevention) were produced separately. They are concatenated so that
"sections 1 to 7" is one file, as `CLAUDE.md` specifies. Section 7's heading
levels were demoted one step to nest under the document; no text was altered.
The assembly note at the top of the file records this.

## Integration status

`01`-`03` are integrated into `RULES.md` from v0.3; `04` from v0.4. Every
rule carries `source:` back to a section here, or `judgment_call:` stating
the position is the repo's rather than a review finding.

`04-acsm-rt.md` was diffed against every strength rule on 2026-09-11. Four
rules were refined against it (`load_magnitude_over_exercise_identity`,
`heavy_load_required_for_max_strength`, `minimum_effective_strength_dose`,
`what_survives_a_cut_session`). One contradiction was recorded against
`progress_effort_not_a_fixed_percentage` and resolved on 2026-10-31 by
splitting that rule in three: `strength_progression_is_load`,
`hypertrophy_progression_is_volume_and_effort`, and
`no_fixed_percentage_progression`. Each carries a `resolution:` field. The
underlying defect was in `03-session-prescription.md` D1, which labels a
hypertrophy finding (Plotkin 2022) "Strength progression"; the review body is
left unaltered as the historical record. The remaining strength rules were
SILENT — the position stand has no tendon, bone, injury-outcome,
mortality-dose or exercise-selection outcome, and states that "the available
evidence did not compare distinct body regions or muscle groups".

## Verification status

**Read this before treating any rule as settled.**

Reviews `01`-`03` are the output of a single deep-research pass by one model.
They have not been independently re-derived. The provenance chain therefore
runs rule → review section → *a model's account of the literature*, and it is
that last link, not the first two, that is weak. `CLAUDE.md` holds that a rule
whose provenance is unverifiable is not usable; until a claim is checked, that
standard is met only partially.

The risk is not uniform. It concentrates in three places, which is what makes
checking tractable:

1. **Recent citations** (2025-2026). Least represented in any training corpus,
   most likely to be confabulated or misattributed at volume/page/DOI level.
2. **Precise numerics under HARD rules.** A wrong effect size in a DISCLOSURE
   is cosmetic; under a HARD rule it changes behaviour.
3. **Absence claims.** A search pass cannot establish that no evidence exists.
   It can only establish that none was found. Three HARD rules rest on this
   distinction: `no_climbing_ramp_threshold`,
   `no_session_level_interval_ramp_rate`, `no_overhead_selection_evidence`.

### Checked so far

Spot-check by leverage, not a random sample — HARD-rule citations first.
Checked 2026-08-12 against primary sources.

| Claim | Rule | Result |
| --- | --- | --- |
| Schuster/Frandsen 2025, BJSM, single-session distance spikes | `run_single_session_spike_cap` | **Verified.** DOI bjsports-2024-109380, p.1203. 5205 runners; HRR 1.64 (1.31-2.05) and 1.52 (1.16-2.00); 110% of 30-day longest run. |
| Buist 2008 GRONORUN, AJSM | `no_ten_percent_week_rule` | **Verified exactly**, including the statistic: 20.8% vs 20.3%, chi2=0.016, df=1, P=.90, N=532. |
| Schoenfeld 2017, JSCR 31(12):3508-3523 | `heavy_load_required_for_max_strength` | **Citation and findings verified** — 21 studies; 1RM favours high load, isometric no difference, hypertrophy similar. The ES 0.58 (0.28-0.89) is not in the abstract; needs full text. |
| Bohm/Mersmann/Arampatzis 2015, Sports Med Open | `tendon_needs_high_strain` | **Verified to the decimal.** 27 studies / 37 interventions / 264 participants; stiffness SMD 0.70 (0.51-0.88), Young's modulus 0.69 (0.36-1.03), CSA 0.24 (0.07-0.42); intensity over contraction type; >12 weeks. |
| Montero & Lundby 2017, J Physiol 595:3377-3387 | `non_response_is_dose_dependent` | **Verified.** 60/120/180/240/300 min/wk; non-response universally abolished by +120 min/wk over a further 6 weeks; attributed to haemoglobin mass. The 69/40/29/0/0% split and r_partial=0.49 need full text. |
| No climbing ramp-rate or ACWR threshold exists | `no_climbing_ramp_threshold` | **Not found on an independent pass either.** An independent systematic review corroborates that climbing risk-factor evidence is inconclusive and contradictory. Absence still not provable. |
| No session-level interval ramp-rate evidence exists | `no_session_level_interval_ramp_rate` | **Not found on an independent pass either.** What surfaces is coaching and practitioner content, which is precisely the review's claim. |
| Impellizzeri 2020, IJSPP 15(6):907 | `acwr_never_gates` | **Verified verbatim.** "No evidence supporting the use of ACWR in training-load-management systems"; acute-to-random ratio as associated with injury as the actual ACWR. |
| Vigotsky 2022, Sports Med | `emg_does_not_select_exercises` | **Verified.** "Acutely Measured Surface EMG Amplitude is not a Validated Predictor of Muscle Hypertrophy" — the claim is the paper's title. |
| Crimp forces and pulley failure load | `crimp_exposure` | **Verified.** A2 x31.5 and A4 x3.9 versus open hand (Vigouroux); 407 N cadaver A2 failure load; recreational finger-flexor force can exceed 400 N. |
| Lauersen 2018 vs 2014 — the seam | `strength_dose_target` | **Resolved.** RR 0.338 from **six RCTs** belongs to Lauersen 2018 (BJSM 52(24):1557-1563), not to 2014. The 25-RCT / 26,610-participant figures are 2014's broader scope. `01-endurance.md` 7.1 attaches RR 0.338 to 2014; that attribution is wrong. The rule is unaffected — it cites the dose-dependent RR, which is 2018's. |
| **Momma 2022, BJSM 56(13):755-763** | `strength_dose_target` | **FAILED — two defects.** See below. |
| 30-year cohort, n=147,374, RT and mortality | `strength_dose_target` | **Verified exactly.** 147,374 participants, 35,798 deaths; 90-119 min/wk all-cause HR 0.87 (0.81-0.95), CVD 0.81 (0.67-0.97); risk plateaus at ~>=120 min/wk with no further benefit. This, not Momma, is what supports the band's upper edge. |
| sRPE validity in climbing, by discipline | `climbing_load_is_unquantified` | **Verified exactly.** vs Edwards TRIMP: bouldering r=0.40 (p<0.01), lead r=0.61, training r=0.66; with local forearm RPE, lead r=0.91 and training r=0.81. |
| No healthy-adult overhead exercise-selection evidence | `no_overhead_selection_evidence` | **Not found on an independent pass either** — and see below. Independently corroborated 2026-09-11: the ACSM 2026 Position Stand, across 137 systematic reviews, states "the available evidence did not compare distinct body regions or muscle groups". The absence is now confirmed by a review-tier source and is broader than the shoulder. |
| Currier 2026, MSSE 58(4):851-872, ACSM Position Stand | strength rules in RULES.md sections 3 and 9 | **Verified against full text**, not abstract. PMID 41843416, PMCID PMC12965823, doi 10.1249/MSS.0000000000003897, open access CC BY-NC-ND. All figures in `04-acsm-rt.md` extracted from the Europe PMC full-text XML. This is the one source in the repo whose provenance chain does not pass through a model's account of the literature. |

### The one failure

`02-climbing.md` B4 states of Momma 2022: "max ~27% reduction at ~60 min/wk
(RR 0.74, 95% CI 0.64-0.86)" and "benefit diminishes and may reverse above
~130-140 min/wk".

The paper (16 cohort studies) reports **"J-shaped associations with the maximum
risk reduction (approximately 10-20%) at approximately 30-60 min/week"**, and
concludes that **"the influence of a higher volume of muscle-strengthening
activities on all-cause mortality, CVD and total cancer is unclear"**.

So the review overstates the peak effect (~27% vs ~10-20%), attaches an RR and
CI the abstract does not support, and converts an explicit *unclear* into
*diminishes and may reverse*. The rest of the same paragraph is sound — the
RR 0.85 / 0.81 / 0.86 figures are consistent with the paper's "10-17% lower
risk".

This propagated into `strength_dose_target`, a HARD rule, which has been
corrected in `RULES.md` v0.3.1 and carries a `correction:` field recording what
it previously said. The review body is deliberately **not** edited — it is the
historical record of what the research pass produced, and editing it would
destroy the evidence that this failure happened.

The rule's operative position is unchanged: the binding number was always the
injury-prevention RR, which verified. What changed is the upper bound's
rationale — see the rule's `judgment_call:`.

### What the overhead search actually returned

Worth recording, because it makes two rules interlock rather than merely
coexist. Searching for healthy-adult overhead exercise-selection evidence
returns coaching content and **EMG activation studies** — "the overhead press
activates the deltoids more than the bench press" and similar. No randomised
training trial with a strength or hypertrophy outcome surfaced.

That is `no_overhead_selection_evidence` and `emg_does_not_select_exercises`
meeting. The reason no selection evidence exists is that the field substituted
acute EMG amplitude for longitudinal outcomes — which is precisely the
inference Vigotsky 2022 says is unvalidated. Anyone re-researching this
question will hit the EMG literature first and will be tempted to treat it as
the answer. It is not.

### Tally

Fifteen claims checked. **Thirteen held** — ten citations verified against
primary sources, three absence claims independently not found. One attribution
seam resolved. **One failed.**

No fabricated citation was found: every paper checked exists, at the journal,
volume and page cited. The single failure was *misreported numbers from a real
paper*. That is the harder error to catch — confirming that a reference exists
would have passed it — and it is why a spot-check has to reach the abstract
rather than stopping at the citation.

(An earlier revision of this file said "eleven of thirteen". That was a
miscount of its own table, corrected here.)

### Still to check

Every HARD-rule numeric, all three absence claims, and both figures propping up
the strength operating band are now checked. What remains is lower-stakes by
construction:

- **DISCLOSURE and SOFT material**, where a wrong number is cosmetic rather
  than behavioural — the hangboard effect sizes, the climbing incidence rates,
  the taper and detraining figures, the intensity-distribution trials.
- **Two partial verifications** needing full text rather than abstract: the
  ES 0.58 (0.28-0.89) inside Schoenfeld 2017, and the 69/40/29/0/0%
  non-response split plus r_partial=0.49 inside Montero & Lundby 2017. Both
  papers and both headline findings are confirmed; only the interior numbers
  are unread.
- **The possible miss**: "A Finger in the Game: Sport-Specific Finger Strength
  Training and Onset of Injury", against `02-climbing.md` A5's claim that no
  RCT on hangboarding injury outcomes exists.
- **The 01-endurance.md 7.1 attribution error** — RR 0.338 credited to Lauersen
  2014 when it belongs to 2018. Logged, not yet reflected anywhere but here.

None of these can change a HARD rule, because none of them is cited by one.
- Full text for the two partial verifications above.
- **A possible miss.** A paper titled "A Finger in the Game: Sport-Specific
  Finger Strength Training and Onset of Injury" surfaced during the climbing
  search. `02-climbing.md` A5 states no RCT on hangboarding injury outcomes
  exists. Whether that paper is an RCT, and whether it bears on
  `hangboard_displaces_never_adds`, is unchecked.
- A seam worth resolving: `01-endurance.md` 7.1 and `02-climbing.md` B4 both
  describe Lauersen 2018 but with different study counts and sample sizes.
  Possibly two distinct analyses, possibly an error.

The strongest check is not re-reading a review with better search — a pass
primed with the existing numbers tends to confirm them. It is an independent
re-derivation, blind to the claims it is checking, then compared.
