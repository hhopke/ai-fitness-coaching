# Endurance Training Science: State-of-the-Art Evidence Review (Knowledge Layer)

Reference material for an automated periodized-planning system. Each substantive claim is labeled **[CONSENSUS]**, **[CONTESTED]**, or **[PRACTITIONER]** (practitioner convention with thin evidential support). Machine-readable structure: one section per scope item; short declarative statements with numeric ranges; "open questions" list closes each section. Current as of August 2026.

**Assembly note.** Sections 1-6 and section 7 were produced as two separate
artifacts and are concatenated here so that `sections 1 to 7` is one file, as
CLAUDE.md specifies. Section 7's heading levels were demoted one step to nest
under this document; no text was altered, added or removed. Section 7's own
open questions and recommendations stay inside section 7; the cross-cutting
recommendations and global caveats at the end apply to sections 1-6 as
originally written.

---

## SECTION 1 — SHARED LOAD–ADAPTATION FRAMEWORK

### 1.1 Banister Fitness-Fatigue Impulse-Response Model
- FORM: P(t) = P0 + k1·Σw(i)e^(−(n−i)/τ1) − k2·Σw(i)e^(−(n−i)/τ2). Five parameters: P0, k1 (fitness gain), k2 (fatigue gain), τ1 (fitness decay), τ2 (fatigue decay). [CONSENSUS]
- PARAMETER RANGES: τ1 (fitness) ~40–50 days; τ2 (fatigue) ~7–15 days; typically τ1 > τ2 and k2 > k1 (fatigue larger per unit of load but decays faster). Busso 2003 reported τ1 ≈ 30.8–40.8 d and τ2 ≈ 7–16.8 d depending on model/phase. [CONSENSUS]
- PREDICTS WELL: dynamics of performance under known training when fit to an individual's maximal performance data; unlike TSB, a steady training state yields improving performance. It is the most experimentally validated impulse-response model. [CONSENSUS]
- FAILURE MODES: parameters are subject- and regimen-specific and reverse-engineered from performance, so the model is descriptive/retrospective rather than predictive; Banister himself recommended re-fitting every 60–90 days. TRIMP input has intrinsic limits (HR misrepresents intensity in short, very long, and intermittent efforts). A single daily impulse cannot disambiguate intensity from duration. Linear form cannot capture nonlinear overtraining. [CONTESTED]

### 1.2 Busso Variable Dose-Response Model
- SOURCE: Busso T, "Variable Dose-Response Relationship between Exercise Training and Performance," Med Sci Sports Exerc 2003;35(7):1188–1195.
- INNOVATION: the fatigue gain k2 is NOT a constant (as in Banister) but a time-varying state that grows with cumulative training dose via a third first-order filter (gain k3, time constant τ3 ≈ 2.3 d). This makes the model nonlinear and produces an inverted-U dose-response that captures overreaching/overtraining. [CONSENSUS on mechanism within the modeling literature]
- PARAMETERS (n=6 previously untrained men, 15-wk cycling): τ1 = 30.8 ± 1.6 d, τ2 = 16.8 ± 3.3 d, τ3 = 2.3 ± 1.0 d; k1 = 0.031, k3 = 0.000035. Net fatigue dominates only when k2 > k1, which occurred when subjects trained 5 consecutive days. Derived optimal ≈322 ± 70 training units/day. Training produced 30 ± 7% performance gain. [as reported]
- FIT: adjusted R² ≈ 0.944 (VDR) vs ≈ 0.885 (standard 2-component); significantly better fit in 5/6 subjects; SEE dropped from 9.22 W to 6.47 W. [as reported]
- FAILURE MODES: tiny untrained sample; parameter identifiability problems; not prospectively validated as a planning tool. [CONTESTED]

### 1.3 CTL/ATL/TSB — Performance Management Chart
- CTL (Chronic Training Load, "Fitness") = exponentially weighted moving average of daily TSS, default time constant 42 days. ATL (Acute Training Load, "Fatigue") default 7 days. TSB (Training Stress Balance, "Form") = CTL − ATL (prior-day values). This is a simplified Banister model (fitness EWMA), commercialized in TrainingPeaks. [CONSENSUS on derivation]
- PREDICTS WELL: tracks accumulated load and freshness trends; useful to visualize ramp and taper. [PRACTITIONER]
- FAILURE MODES: TSS is a dose index, not a stress-response measure (per Impellizzeri); equal-TSS sessions are not physiologically equivalent; the fixed 42/7 constants are population defaults, not individualized; there is no validated TSB target for peaking (the practitioner convention of ~+5 to +25 at race is a heuristic). [PRACTITIONER/CONTESTED]

### 1.4 ACWR (Acute:Chronic Workload Ratio)
- DEFINITION: acute load (usually 1 wk) ÷ chronic load (usually 4-wk rolling average, or an EWMA variant). Proposed "sweet spot" 0.8–1.3; elevated risk >1.5. [CONTESTED]
- EVIDENCE FOR: Gabbett's training-injury-prevention-paradox framing; an IOC consensus statement endorsed the 0.8–1.3 sweet spot. Qin et al. (2025), BMC Sports Sci Med Rehabil 17:285, pooled 22 cohort studies (16 rated high-quality, NOS ≥7) and concluded that "although ACWR is associated with sports injury risk... it is necessary to use it with caution as a tool for measuring workload." [CONTESTED]
- IMPELLIZZERI CRITIQUES (Impellizzeri et al. 2020, Int J Sports Physiol Perform 15(6):907): (a) the ratio has adverse statistical properties (mathematical coupling, artefacts, added noise); (b) discretizing continuous data into buckets creates artificial thresholds — when treated as continuous with outliers removed the association disappears (Wang et al.); (c) an "acute-to-random workload ratio" is as associated with injury as the actual ACWR — indicating no added value; (d) no study has estimated causal effects, so manipulating ACWR to reduce injury is conjecture; (e) they requested retraction/correction of the BJSM "sweet spot" figure. Their conclusion: "There is no evidence supporting the use of ACWR in training-load-management systems." [CONSENSUS that the methodology is flawed]
- STATUS: ACWR is not a validated injury predictor. Defensible only as a descriptive load-monitoring/visualization tool, not a causal prescription. [CONSENSUS emerging]

### 1.5 Monotony and Strain (Foster)
- MONOTONY = weekly mean daily load ÷ SD of daily load. STRAIN = weekly load × monotony. [CONSENSUS on definition]
- THRESHOLDS: monotony >2.0 is flagged as elevated illness/overreaching risk when combined with high load; the preferred range ~1.0–1.5 is a practitioner heuristic. Foster's original work (N=25 experienced athletes) found that illnesses spiked when individuals exceeded individually identifiable strain thresholds. [PRACTITIONER — small original sample; threshold values are heuristics]
- STATUS: endorsed in the joint ECSS/ACSM overtraining consensus (Meeusen et al. 2013) as a risk marker. Correlational, sRPE-based, athlete-specific — a monitoring flag, not a quantitatively validated predictor. [CONSENSUS as risk marker / CONTESTED as predictor]

### 1.6 HRV-Guided Training
- PROTOCOLS: daily morning lnRMSSD (e.g., HRV4Training); train harder when HRV sits within/above the individual smallest-worthwhile-change band (mean ± 0.5 SD from a familiarization period), and substitute easy/rest when HRV drops. Kiviniemi (originator), Vesterinen, Javaloyes, Nuuttila protocols. [CONSENSUS on method]
- OUTCOMES (meta-analyses): small-to-medium positive effect on submaximal physiological parameters (g ≈ 0.30, 95% CI 0.03–0.56, p=0.028); effects on performance (g ≈ 0.08–0.20) and VO2peak (g ≈ 0.17–0.20) small and non-significant; superior for maintaining vagal-related HRV (SMD ≈ 0.50, 95% CI 0.09–0.91); fewer non-responders and more positive responders. HRV-guided groups typically complete fewer moderate/high-intensity sessions for equal or better outcomes. [CONSENSUS — modest benefit, primarily via better session timing and reduced non-response, not large performance gains]
- FAILURE MODES: methodology unsettled (index selection, recording position, baseline vs rolling averages); most studies small; Javaloyes found no VO2max improvement in professional cyclists. [CONTESTED]

**Open questions (Section 1):**
- Can IR-model parameters be estimated reliably enough for individual prospective prescription rather than retrospective fitting?
- What individualized CTL/ATL time constants outperform the 42/7 defaults?
- Is there any load-based metric with a demonstrated causal (not correlational) link to injury?
- What is the optimal HRV decision rule (single-day vs 7-day rolling; SWC bandwidth)?

---

## SECTION 2 — INTENSITY DISTRIBUTION AND PERIODIZATION

Zones (3-zone Seiler model): Z1 below first lactate/ventilatory threshold (LT1/VT1); Z2 between thresholds; Z3 above LT2/VT2.
- POLARIZED (POL): Z1 > Z3 > Z2. PYRAMIDAL (PYR): Z1 > Z2 > Z3. THRESHOLD (THR): work concentrated at/near Z2. SWEET-SPOT: work just below FTP/LT2 (~88–94% FTP), a practitioner cycling construct. [PRACTITIONER for sweet-spot]

### 2.1 What is convergent
- Both elite and well-trained endurance athletes accumulate the large majority (~75–80%+) of training volume in Z1 (low intensity). A high-volume low-intensity base is near-universal. [CONSENSUS]
- Some concentration of high-intensity work is required for maximal gains in well-trained athletes; pure high-volume or pure threshold approaches underperform in well-trained cohorts. [CONSENSUS]

### 2.2 Genuinely contested: POL vs PYR
- Stöggl & Sperlich 2014 (Front Physiol 5:33; n=48 well-trained runners/cyclists/triathletes/skiers, baseline VO2peak 62.6 mL/kg/min; 9 wk; POL vs THR vs HVT vs HIIT): POL produced the greatest gains — VO2peak +11.7% (+6.8 mL/kg/min, p<0.001), time-to-exhaustion +17.4% (p<0.001), peak velocity/power +5.1% (p<0.01); THR and HVT produced no significant further gains. Foundational pro-POL result but single, short, well-trained. Achieved TIDs: HVT 83/16/1, THR 46/54/0, HIIT 43/0/57, POL 68/6/26. [CONTESTED]
- Rosenblat, Perrotta & Vicenzino 2019 (J Strength Cond Res 33(12):3491–3500) meta-analysis, POL vs THR: pooled ES = −0.66 (95% CI −1.17 to −0.15), a moderate effect favoring POL on time-trial performance; only 3 RCTs pooled (n=64), 4 in the review (n=112), PEDro quality 4–5/10, durations 6 wk–5 months. Small, low-quality evidence base. [CONTESTED]
- Silva Oliveira, Boppre & Fonseca 2024 (Sports Med 54(8):2071–2095; 17 studies, n=437) found NO superiority of POL over other TIDs including PYR, explicitly attributing the reversal versus Rosenblat to the larger sample and inclusion of PYR/VO2peak/TTE outcomes. [CONTESTED — direct disagreement with Rosenblat]
- Filipas et al. 2022 (Scand J Med Sci Sports; n=60 well-trained runners, 16 wk): a PYR→POL sequence gave the largest gains (relative VO2peak ~3.0%, 5-km TT ~1.5%), supporting a periodized shift rather than one fixed model. [CONTESTED]
- Treff, Winkert, Sareban, Steinacker, Becker & Sperlich 2017 (Front Physiol 8:515; n=14 national-elite rowers, 11 wk): POL not superior to PYR. [CONTESTED]
- Casado/Foster/Seiler framing: POL and PYR are not competing prescriptions but phases of a yearly plan — PYR in base, shift toward POL near competition; classification is sensitive to whether sessions are counted by session-goal or by time-in-zone. A 2025 Rosenblat-and-colleagues review nuance: POL appears marginally more effective in elite athletes, whereas the relationship reverses toward pyramidal/flexible in recreational athletes. [CONSENSUS among these authors as framing]

### 2.3 Critiques of the polarized framing
- Burnley/Bishop/Halson-type critiques: the mitochondrial-signaling rationale (Ca²⁺ pathway from high-volume training and AMPK from high-intensity training converging on PGC-1α) is mechanistically plausible but does NOT establish POL superiority; TID classification is arbitrary and label-sensitive; "polarized" is frequently applied post hoc to describe what elite athletes already do. [CONTESTED]

### 2.4 Moderators (should drive the decision)
- TRAINING STATUS: In recreational/lower-level athletes almost any well-applied distribution improves fitness (more flexibility); in elite athletes only PYR and POL consistently drive improvement, plausibly because higher-level athletes tolerate greater high-intensity loads. [CONTESTED but converging]
- WEEKLY HOURS/VOLUME: higher volume tolerates and benefits from more Z1 base (pyramidal-leaning); time-constrained athletes may need proportionally more intensity. [PRACTITIONER]
- EVENT DURATION: longer events weight toward volume/durability (pyramidal/base emphasis); shorter or championship-focus periods weight toward polarized sharpening. [PRACTITIONER]

### 2.5 Periodization structure
- BLOCK vs TRADITIONAL: Mølmen, Øfsteng & Rønnestad 2019 meta-analysis (OAJSM) — block periodization shows small favorable effects vs traditional: VO2max SMD 0.40 (95% CI 0.02–0.79), Wmax SMD 0.28 (95% CI 0.01–0.54), with moderate-to-large effects for some threshold/performance indices. BUT low methodological quality (mean PEDro 3.7/10), and some matched-load studies (Almquist et al. 2022; McGawley et al. 2017) find no benefit — physiological gains do not always translate to performance under strictly matched load. [CONTESTED — promising, weak evidence]
- LINEAR vs REVERSE: sparse direct evidence; reverse periodization (intensity early, volume later) is mainly relevant when peaking for shorter/high-intensity events or under off-season constraints. [PRACTITIONER]

**Open questions (Section 2):**
- Does POL beat PYR when total load is strictly matched in elite athletes?
- Optimal timing/sequence of a PYR→POL transition?
- Do block-periodization physiological gains translate to competition performance under matched load?
- How should a planning system auto-classify TID (session-goal vs time-in-zone)?

---

## SECTION 3 — SPORT-SPECIFIC DEVIATIONS (do NOT generalize across)

### 3.1 CYCLING
- LOAD QUANTIFICATION: power-based; TSS derived from normalized power and FTP; well-validated as a dose index, with demonstrated agreement with TRIMP for cycling. Power is the most objective external-load metric in endurance sport. [CONSENSUS as dose index]
- CRITICAL POWER / W′: CP = power asymptote separating the heavy and severe intensity domains (sustainable ~30–45 min); W′ = finite work capacity above CP (kJ). Models: 2-parameter hyperbolic, 3-parameter hyperbolic, linear, linear-1/time, exponential. [CONSENSUS on concept]
- PARAMETER-ESTIMATION ISSUES: CP/W′ estimates vary systematically with model and trial selection; the 3-parameter model yields lower CP and questionably high W′; short trials bias estimates; protocol design (trial durations ~1–20 min, ideally 2–15 min with ≥5-min spread) materially changes values; longitudinal tracking requires a fixed protocol and model. [CONSENSUS that estimates are protocol-dependent]
- 3-MIN ALL-OUT TEST: field and lab yield similar CP and W′; Pmax is more sensitive to test environment. [as reported, small samples]
- DURABILITY / FATIGUE RESISTANCE (Maunder et al. 2021): "the time of onset and magnitude of deterioration in physiological-profiling characteristics during prolonged exercise" — proposed as a 4th endurance parameter alongside VO2max, thresholds, and economy. Assessed via drifts (HR, VO2, RPE, gross efficiency) or by performance/CP measured after accumulated work (e.g., after ~1000+ kJ or 2+ h). Fresh-state profiling overestimates late-race capacity; ~88% of variance in a 30-min TT after 2 h of cycling is explained by post-fatigue physiological profile. Durability is improved by both low- and high-intensity training. [CONSENSUS as emerging concept; measurement standards not yet fixed]
- REPEATABILITY: W′ reconstitution rate correlates with aerobic fitness (CP, VO2max); trained cyclists reconstitute W′ faster. [as reported, small samples]

### 3.2 RUNNING
- BINDING CONSTRAINT: mechanical/structural tissue tolerance (bone, tendon), not just cardiometabolic capacity — this is what distinguishes running from cycling/swimming for planning. [CONSENSUS]
- BONE: remodeling operates on months-long cycles; bone stress injuries arise when repetitive loading outpaces remodeling. Skeletal adaptation lags cardiovascular fitness gains, so aerobic capacity can outrun bone readiness. [CONSENSUS on principle]
- TENDON: collagen turnover is slow; meaningful stiffness/strength adaptation occurs over ~2–8 weeks of consistent loading, but full matrix remodeling and maturation (cross-linking into load-bearing architecture) runs months to ~1–2 years; tendon responds to loading more slowly than muscle. A tendon can appear repaired on imaging well before it can take full load. [CONSENSUS on timescales]
- RAMP-RATE EVIDENCE (running injury): single-session distance spikes are the clearest signal. Schuster/Brandt/Frandsen et al. 2025 (Br J Sports Med 59:1203–1210; 5205 runners, mean age 45.8, 22% female, 1820 [35%] injured across 588,071 sessions): a single-session distance >10% above the longest run in the prior 30 days raised injury rate — small spike (>10–30%) HRR 1.64 (95% CI 1.31–2.05), moderate (>30–100%) HRR 1.52 (1.16–2.00), large (>100%) HRR 2.28 (1.50–3.48). The week-to-week ratio showed no relationship; ACWR showed a negative/inconsistent dose-response. An ultramarathon cohort found ACWR had no significant effect on injury (weak U-shape). The "10% per week" rule is a heuristic, not validated. [CONTESTED overall — single-session spikes have support; ACWR does not]
- rTSS and GAP (grade-adjusted pace): convenience metrics. GAP models a flat-equivalent pace, but the grade–economy relationship is individual and nonlinear (especially steep downhill and technical terrain), so GAP degrades on trails and does not capture eccentric/impact load. rTSS does not capture the mechanical/impact cost that actually drives running injury; it treats metabolic and structural load as equivalent when they are not. [PRACTITIONER/CONTESTED]

### 3.3 SWIMMING
- CRITICAL SWIM SPEED (CSS): slope of the distance–time line, classically from 400 m and 50 m (or 200/400) time trials; CSS = (400−50)/(T400−T50). A field proxy for critical/threshold speed (~1500 m TT pace). Origin: Wakayoshi et al. 1992; simplified by Ginn 1993. [CONSENSUS as field proxy]
- VALIDITY: a scientifically rigorous critical-speed estimate needs 3–7 trials lasting ~2–15 min with ~5-min duration spread; the practical 2-point (200/400) test trades rigour for feasibility. CSS is stroke-specific (freestyle CSS does not transfer to other strokes) and course-specific (SCY/SCM/LCM not interchangeable). [CONSENSUS on limits]
- TECHNIQUE-LIMITED PACE: swimming velocity is dominated by technique/drag economy, not just metabolic capacity — a key reason metabolic dose-response transfers poorly. Small technique changes shift the pace–power relationship. [CONSENSUS]
- WHY DOSE-RESPONSE MODELS TRANSFER POORLY: intensity is hard to quantify in water — HR is unreliable (affected by temperature, immersion, hydrostatic pressure) and power is not routinely measured; technique confounds velocity-as-output; drills and kick sets are not comparable. TrainingPeaks itself calls swim TSS "nebulous," to be set athlete-specifically. [CONSENSUS that swimming load quantification is weakly validated]
- WHAT IS VALIDATED: CSS as a pacing/threshold anchor has reasonable reliability; beyond that, swimming load quantification (swim TSS, sTRIMP) is largely unvalidated. [CONSENSUS]

**Open questions (Section 3):**
- Best standardized field durability test for amateur cyclists/runners?
- Can a validated mechanical/impact-load metric for running be built (e.g., accelerometry-based)?
- Is there any validated internal-load model for swimming?

---

## SECTION 4 — MULTISPORT LOAD COMBINATION (Triathlon)

- PRACTICE: summing TSS (sTSS + bTSS + rTSS) into a single Performance Management Chart is the dominant commercial convention (TrainingPeaks). [PRACTITIONER]
- IS SUMMING DEFENSIBLE? Weakly, and this is genuinely unresolved. Acknowledged problems: (a) "1 point of CTL is not equal among the three disciplines" (TrainingPeaks' own statement); (b) swim TSS is poorly validated (see 3.3); (c) equal TSS across modalities produces unequal systemic AND unequal mechanical stress — running TSS carries far higher structural/injury cost per unit than cycling or swimming; (d) the three modalities share a common recovery/systemic-stress pool but load tissues differently, so a single summed scalar discards the information needed for injury management. [CONTESTED / largely UNRESOLVED]
- EVIDENCE: triathlon load research is descriptive. A 95-athlete, 6-month age-group cohort (Frontiers in Sports and Active Living, 2026) explicitly treats TSS strictly as a dose index (per Impellizzeri), not a stress-response, and does not validate cross-modal summation. A coach pilot study (Sports 2024;12(9):261) found that combining disciplines masks single-discipline spikes (22 single-discipline ACWR spikes vs 14 when combined) and that most injury-associated lost training followed running-based load spikes (>30%). This argues AGAINST collapsing to a single combined number for injury purposes. [CONTESTED]
- ALTERNATIVES IN LITERATURE/PRACTICE: (a) maintain discipline-specific PMCs (swim, bike, run, bike+run, and combined — in that priority) rather than one summed chart; (b) monitor per-discipline ACWR/ramp separately, especially running mechanical load; (c) use sRPE-based session load as a common systemic-stress currency across modalities (one usable number, but with the same statistical-coupling caveats); (d) the 3-dimensional impulse-response approach for evaluating cross-sport transfer. [PRACTITIONER + emerging]
- BOTTOM LINE: summing TSS across swim/bike/run is a practical convenience, NOT a validated model. For systemic/cardiometabolic tracking it is a rough guide; for injury/structural-load management it is not defensible, because running's mechanical load and swimming's poor quantification break the equivalence assumption. State this explicitly to any downstream user. [CONTESTED / UNRESOLVED]

**Open questions (Section 4):**
- Is there a defensible non-1:1 weighting for cross-modal load summation?
- Can systemic vs mechanical load be tracked as two parallel currencies in a planner?

---

## SECTION 5 — TAPER AND PEAKING

- BOSQUET et al. 2007 META-ANALYSIS (Med Sci Sports Exerc 39(8):1358–1367; 27 studies): optimal strategy — a 2-week taper in which training VOLUME is exponentially reduced by 41–60% (overall effect 0.72 ± 0.36), WITHOUT changing intensity (effect of reducing intensity alone only 0.33 ± 0.14) or frequency (0.35 ± 0.17). Volume is the primary lever; intensity and frequency should be maintained. [CONSENSUS]
- EXPECTED EFFECT SIZE: typical performance improvement ~2–3% (Mujika's body of work); Bosquet's overall performance effect ~0.59 ± 0.33 (p<0.001). [CONSENSUS]
- TAPER PATTERN: a progressive/exponential fast-decay taper is superior to step or linear tapers; volume is cut most at the start, then levels off (fast-decay to ~20–30% of normal). [CONSENSUS]
- DURATION: ~2 weeks optimal on average; broader range 4–28 days. A 2023 endurance meta-analysis (PLOS ONE, 14 studies) found significant time-trial gains across ≤7-day, 8–14-day, and 15–21-day windows with a 41–60% volume cut (largest SMD −0.77, 95% CI −1.23 to −0.30). [CONSENSUS]
- INTENSITY MAINTENANCE: maintain (or emphasize) high intensity; low-volume/high-intensity tapers outperform combined volume-and-intensity cuts. [CONSENSUS]
- FREQUENCY MAINTENANCE: maintain. For low-technical events (running, cycling) frequency may drop ~20%; for high-technical events (swimming, XC skiing, kayaking) maintain frequency to preserve technical efficiency ("feel"). [CONSENSUS with per-sport nuance]
- PRE-TAPER OVERLOAD: a taper preceded by an overload block produces larger time-trial gains than a conventional taper (2023 meta-analysis subgroup). [CONTESTED — promising]
- PER-SPORT: swimming is most sensitive to frequency/technique loss; running tolerates the largest frequency reduction; strength/power sports more often use step tapers. [CONSENSUS/PRACTITIONER]

**Open questions (Section 5):**
- Individualization of taper length by an athlete's CTL/fatigue kinetics?
- Optimal pre-taper overload magnitude without leaving residual fatigue?

---

## SECTION 6 — LONGEVITY AND EXERCISE (a separate literature from performance training)

### 6.1 Cardiorespiratory fitness (VO2max/CRF) as a mortality predictor
- Mandsager et al. 2018 (JAMA Netw Open 1(6):e183605; 122,007 patients on treadmill testing, median 8.4-y follow-up): all-cause mortality was inversely proportional to CRF with NO observed upper limit of benefit. Elite (≥97.7th percentile) vs low aHR 0.20 (95% CI 0.16–0.24); elite vs high aHR 0.77 (0.63–0.95); low vs elite aHR 5.04 (4.10–6.20); below- vs above-average aHR 1.41 (1.34–1.49). Being unfit carried risk comparable to or exceeding major clinical risk factors. [CONSENSUS — CRF is among the strongest modifiable mortality predictors]
- Corroborated by the Kokkinos (veterans cohorts) and Blair (Aerobics Center Longitudinal Study) traditions; the gradient holds across age, sex, and race. [CONSENSUS]
- IMPLICATION: the CRF–mortality association is far stronger and better established than any specific training-method claim. The single most important longevity lever is achieving and maintaining high CRF, largely independent of HOW it is achieved. [CONSENSUS]

### 6.2 Zone 2 / mitochondrial argument (San-Millán, popularized by Attia)
- CLAIM: training at Zone 2 (just below LT1, "FatMax") maximally stimulates mitochondrial biogenesis, fat oxidation, and lactate clearance (MCT1), driving both performance and metabolic health/longevity. [PRACTITIONER / partly CONTESTED]
- WHAT IS SOLID: low-intensity/Zone-2 training does improve mitochondrial function, fat oxidation, and lactate handling; a high aerobic base characterizes elite endurance athletes; mitochondrial dysfunction is associated with cardiometabolic disease. [CONSENSUS]
- WHERE PRACTITIONER OPINION HAS OUTRUN THE EVIDENCE: the claim that Zone 2 SPECIFICALLY and MAXIMALLY stimulates mitochondrial adaptation more than other intensities is NOT established — high-intensity work also strongly drives mitochondrial and MCT4 adaptations (McGinley et al. 2016), and optimal mitochondrial development likely requires mixed intensities. The "Zone 2 is uniquely optimal for longevity" framing is extrapolated from athlete performance observations and mechanistic reasoning, not from longevity RCTs. San-Millán's strongest primary data are observational metabolomics/lactate-profiling in professional cyclists (Frontiers in Physiology 2020), not mortality outcomes. [PRACTITIONER — mechanistically plausible; longevity claims unproven]
- The well-evidenced longevity benefit runs THROUGH achieving high CRF (§6.1), which Zone 2 volume contributes to but does not monopolize.

### 6.3 Resistance training / muscle strength, power & mass as INDEPENDENT mortality predictors
- Muscular strength (handgrip) meta-analysis (García-Hermoso et al., 38 studies, ~1.9M adults, 63,087 deaths): high vs low grip strength all-cause mortality HR 0.69 (95% CI 0.64–0.74); knee-extension strength HR 0.86 (0.80–0.93). Association slightly stronger in women (HR 0.60). [CONSENSUS]
- Resistance-training behavior: Saeidifard et al. 2019 (Eur J Prev Cardiol; 11 studies, 370,256 participants) — RT vs none ~21% lower all-cause mortality (HR 0.79, 0.69–0.91), rising to ~40% lower when combined with aerobic exercise (HR 0.60, 0.49–0.72). Dose ~30–60 min/week (and specifically 90–119 min/week: HR 0.87 all-cause, 0.81 CVD) associated with lower mortality, with attenuation/reversal at very high volumes in some cohorts. Boyle/Shailendra/Bennie meta-analysis links RT with reduced all-cause, CVD, and cancer mortality. [CONSENSUS]
- Muscle POWER may predict mortality more strongly than strength: Araújo et al. 2025 (Mayo Clin Proc 100(8):1319–1331; CLINIMEX cohort, n=3889 aged 46–75, median 10.8-y follow-up) — lowest vs highest relative power HR 5.88 (95% CI 2.28–15.17) in men and 6.90 (1.61–29.58) in women, versus non-significant relative-strength HRs of 1.62 (0.89–2.96) and 1.71 (0.61–4.80). [as reported]
- IMPLICATION: strength/power/muscle is an INDEPENDENT mortality axis not captured by CRF. A longevity-oriented program therefore requires resistance training, which performance-endurance plans often under-prescribe. [CONSENSUS]

### 6.4 VO2max decline with age and its modifiers
- General population: VO2max declines ~10% per decade after ~25–30 y, accelerating after 60–70 (longitudinally ~8% in the 4th decade rising to ~23% by the 7th). [CONSENSUS]
- Masters athletes maintaining training: decline halved to ~5–6.5% per decade (Heath et al. 1990 reported 5.5%/decade in masters vs 12%/decade in sedentary controls). Rate closely tracks training-volume/intensity maintenance — Tanaka & Seals: changes in training volume explain ~54% of the decline variance in men and ~39% in women. Male masters maintaining volume (≤10% reduction): −5% to −6.5%/decade; those who reduce sharply: up to −46%/decade. [CONSENSUS]
- IRREDUCIBLE component: maximal heart rate falls with age and caps VO2max regardless of training — it cannot be fully trained away. [CONSENSUS]
- DETRAINING: near-linear VO2max fall within days of cessation, up to −20% by 12 weeks, driven by drops in stroke volume/cardiac output and in mitochondrial enzyme activity (citrate synthase, succinate dehydrogenase). [CONSENSUS]

### 6.5 Contested J/U-curve — very high lifelong volume and cardiac remodeling
- ATRIAL FIBRILLATION: endurance athletes carry roughly double the odds of AF (OR ≈ 2.34, 95% CI 1.04–5.28 in one cohort), with a reversed-J dose-response — reduced risk at light-to-moderate volumes, increased risk at extreme volumes. Traditional AF risk factors (hypertension, obesity, diabetes) are LOWER in masters athletes, yet AF prevalence is higher. [CONSENSUS that AF risk is elevated in high-volume male endurance athletes]
- CORONARY ARTERY CALCIFICATION (CAC): male masters endurance athletes show HIGHER CAC and coronary-plaque prevalence than less-active peers (e.g., ≥50% stenosis 7.5% vs 0%; high CAC >300 Agatston more prevalent), with a non-linear association with lifelong exercise volume; athlete plaques may be more calcified and potentially more stable. This is NOT seen (or is much attenuated) in female athletes. [CONSENSUS on the finding; clinical significance CONTESTED]
- MYOCARDIAL FIBROSIS: focal/diffuse fibrosis is found in a small subgroup of veteran male athletes; its prognostic significance is unknown. [CONTESTED]
- KEY RECONCILIATION: the two largest CRF-mortality studies (Mandsager 2018; the JACC veterans cohort) found NO increased mortality at extreme fitness. Adverse cardiac markers appear in specific subgroups (older males, high lifelong volume, and — per La Gerche — possibly those exercising excessively relative to their fitness), and have not translated into higher all-cause mortality in fitness cohorts. Thus adverse remodeling markers are real, but their prognostic meaning is unresolved, and they coexist with a net mortality benefit. Female athletes appear largely protected from CAC (AF protection is now less certain, per La Gerche). [CONTESTED — the "extreme exercise hypothesis"]

### 6.6 Where longevity-optimal DIVERGES from performance-optimal
- Performance-optimal endurance training maximizes sport-specific volume/intensity, often to the edge of tissue and cardiac tolerance. Longevity-optimal training seeks high-but-not-extreme CRF PLUS resistance/power training PLUS avoidance of the very-high-volume zone associated with AF/CAC in susceptible males.
- Specific divergences: (a) longevity gains from CRF are largely captured well below elite training volumes — mortality returns diminish above high fitness while performance keeps improving; (b) resistance/power training is longevity-critical but is often minimized in performance endurance plans; (c) extreme lifelong volumes (needed for elite performance) carry AF/CAC signals with unresolved risk, so are not longevity-justified in susceptible males; (d) longevity training requires neither tapering/peaking nor event-specific specificity. [CONSENSUS on direction; magnitude of divergence CONTESTED]

**Open questions (Section 6):**
- What is the prognostic significance of athlete CAC/fibrosis — do calcified athlete plaques carry lower event risk?
- Is there a true upper threshold of exercise volume where the mortality benefit reverses, or only subgroup cardiac-marker risk?
- Why do female athletes appear protected from CAC, and are they protected from AF?
- What resistance-training dose maximizes mortality benefit, and does very high RT volume attenuate it?

---

## SECTION 7 — INJURY PREVENTION

**Scope note:** This section extends the prior review's injury coverage (previously limited to running load-management via ramp rate and ACWR) into a cross-disciplinary, prevention-focused evidence layer. Every substantive claim is labeled **[CONSENSUS]**, **[CONTESTED]**, or **[PRACTITIONER]** (practitioner convention with thin evidential support). Effect sizes are given with CIs where available. A recurring transferability caveat applies throughout: the strongest prevention-RCT evidence is pooled from team/contact sports and youth, not from endurance athletes — this is flagged wherever it matters. Numeric thresholds are stated wherever the literature supplies them.

---

### 7.1 Cross-sport intervention evidence

#### Strength / resistance training — the single best-supported preventive intervention. [CONSENSUS]
- **Lauersen, Bertelsen & Andersen 2014 (BJSM)** — meta-analysis of 25 RCTs, 26,610 participants, 3,464 injuries. Strength training reduced overall sports injuries to less than one-third (RR 0.338). Overuse injuries reduced by ~half (RR 0.527, 95% CI 0.373–0.746, I²=19%). **Stretching showed no significant protective effect.** Proprioception training reduced injuries but by less than strength.
- **Lauersen, Andersen & Andersen 2018 (BJSM)** — dose-response follow-up. Strength-training programs consistently reduced injuries across four acute and overuse outcomes; a clear dose-response was reported (greater volume → greater risk reduction). Pooled RR ~0.34; GRADEpro "high certainty" for the hamstring-injury subset; zero serious adverse events across included trials.
- **TRANSFERABILITY CAVEAT [CONTESTED as to magnitude in endurance populations]:** Lauersen's pooled trials are overwhelmingly team/contact sports (soccer, handball) and military recruits, in adolescents/young adults. Direct endurance-sport RCT evidence is far sparser. The ~68% acute / ~50% overuse reductions should be treated as an upper-bound estimate when extrapolated to endurance athletes.

#### Multi-component neuromuscular programs (FIFA 11+ as template). [CONSENSUS for football; template value only for endurance]
- **Thorborg et al. 2017 (BJSM)**, pooling 4 FIFA 11+ cluster-RCTs, reported a reduction in overall injury risk (incidence rate ratio 0.61, 95% CI 0.48–0.77, p<0.001) — i.e., **football injuries reduced by 39%.**
- Soligard et al. cluster-RCT (1,892 female youth footballers): 32% overall injury reduction. Silvers-Granelli et al.: 46.1% reduction in male collegiate players.
- Site-specific pooled outcomes: knee injury reduction 46% (IRR 0.54, 95% CI 0.43–0.69) across 9,647 players; **ankle injury rate ratio 0.67 (95% CI 0.46–0.96, p=0.03, I²=52%), a 33% lower risk** (2025 SR+MA of 3 RCTs, 3,833 participants, 286,827 exposure hours, moderate certainty); FIFA 11+ Kids overall injury RR 0.52 (95% CI 0.44–0.62).
- Lauersen's group argued multi-component ("a little bit of everything") programs risk diluting the most effective single component (strength). **[CONTESTED: single-modality strength vs multi-component packaging]**

#### Stretching does not prevent injury. [CONSENSUS]
- Multiple systematic reviews conclude static stretching in warm-up does not reduce overall injury rates; there is only preliminary/weak evidence it may reduce musculotendinous injuries specifically. In one large military RCT (Pope et al.), ~337 individuals would need to stretch to prevent a single lower-limb injury.
- **Dynamic warm-up:** widely used and defensible for performance/readiness, but injury-prevention evidence is thin and largely narrative. **[PRACTITIONER]**

---

### 7.2 Running

#### Incidence baseline. [CONSENSUS]
- Weighted injury incidence (Videbæk/Andersen et al. 2015 SR+MA): **novice runners 17.8 per 1000 h (95% CI 16.7–19.1); recreational runners 7.7 per 1000 h (95% CI 6.9–8.7).** Range across studies 2.5 (long-distance track/field) to 33.0 (novice) per 1000 h. Novice runners face significantly greater per-hour risk than recreational runners.

#### Risk factors. [CONSENSUS on previous injury]
- **Previous injury is the dominant, most consistent predictor of RRI. [CONSENSUS]** van der Worp et al. 2015 (PLOS One; 15 longitudinal studies): strong/moderate evidence for previous injury and orthotic/insert use as risk factors; sex differences exist but should be interpreted cautiously (few studies report by sex).
- Umbrella review (2024, J Sport Health Sci): training characteristics and health/lifestyle factors carry the largest effect sizes; underlying SR quality is generally low; biomechanical risk factors remain inconclusive.
- Biomechanical risk factors (vertical loading rate, kinematics): evidence sparse and inconsistent, and injury-specific (e.g., greater peak hip adduction linked to patellofemoral pain and ITBS in some female-runner samples). **[CONTESTED]**

#### Gait retraining / cadence. [CONTESTED — promising but low-certainty for injury endpoints]
- JOSPT 2022 SR+MA (19 RCTs, 673 participants): gait retraining reliably increases step rate, alters knee kinematics, and lowers vertical loading rates without harming running performance. Two trials showed reduced 1-year injury incidence.
- A moderate cadence increase (typically 5–10%) yields consistent biomechanical improvements — reduced vertical ground-reaction forces, lower loading rates, shorter stride length, improved lower-limb alignment (2025 Cureus SR).
- **Chan et al. 2018 (AJSM; n=320 novice runners):** at 12-month follow-up, running-related injury occurred in 16% (gait-retraining) vs 38% (control); hazard ratio 0.38 (95% CI 0.25–0.59) — a **62% lower injury risk.** This single influential RCT drives much of the optimism; injury-endpoint certainty remains low overall. **[CONTESTED]**

#### Footwear / minimalist transition. [CONTESTED / cautionary]
- Transitioning to minimalist footwear increases short-term injury risk when done too quickly; body mass and weekly distance moderate pain/injury. Ryan et al. 2014 (BJSM) found a higher injured-runner proportion in the partial-minimalist (Nike Free) condition vs conventional/Vibram.
- Shoe cushioning: an RCT of 848 recreational runners (Malisoux et al., AJSM 2020) found cushioning influences injury risk as a function of body mass.
- **No strong evidence that any single footwear category prevents injury across the board. [CONSENSUS on absence of evidence]**

#### Strength training for runners specifically. [CONTESTED — practitioner belief has outrun endurance-specific evidence]
- Endurance-runner-specific SR+MA (2024, Sports Medicine — "Do Exercise-Based Prevention Programs Reduce Injury in Endurance Runners?"): supervision status matters; evidence is weaker than in team-sport settings.
- Narrative reviews note ample retrospective evidence that hip/muscle weakness characterizes injured runners, but limited prospective evidence that strength training *prevents* RRIs — especially when unsupervised. The general Lauersen effect therefore does not cleanly transfer to running.

#### Load management (integrating the prior review). [CONSENSUS on training error as cause; CONTESTED on specific metrics]
- Overuse dominates RRI etiology. The Garmin-RUNSAFE cohort (Nielsen et al., JOSPT Open 2025; 18-month follow-up, 1,666 injuries) classified **1,199 of 1,666 injuries (72%) as overuse** and 467 (28%) as overload — confirming that the majority of RRIs arise from load/tissue-tolerance mismatch rather than acute overload.
- Training errors ("too much, too soon") are the principal modifiable cause. The **"10% rule" lacks validating evidence** as an injury-prevention threshold; GRONORUN tested exactly this and found no benefit (below). Integrate with — do not replace — the prior review's ramp-rate/ACWR logic.

#### Online / graded-training prevention program trials — largely NULL. [CONSENSUS: these do not work as delivered]
- **GRONORUN (Buist et al. 2008, AJSM; N=532 novice runners):** graded 13-week vs standard 8-week program — **NO effect.** Injury incidence 20.8% (graded) vs 20.3% (standard), χ²=0.016, P=.90.
- **SPRINT (Cloosterman et al. 2022, BJSM; N=4,105 — largest RRI-prevention RCT):** enhanced educational online program — **NO effect.** New RRI 35.5% (95% CI 33.5–37.6) intervention vs 35.4% (95% CI 33.3–37.5) control, OR 1.03. Program compliance was paradoxically associated with slightly higher injury rates.
- **INSPIRE (Fokkema et al. 2019, BJSM; N=2,378):** multifactorial online prevention — **NO effect** (37.5% vs 36.7%, OR 1.08, 95% CI 0.90–1.30). Subgroup signal of possible **harm** in previously-uninjured runners (OR 1.30, 95% CI 0.99–1.70).
- **TrailS6 (Hespanhol et al. 2018, BJSM; N=232 trail runners):** tailored biweekly online advice — **POSITIVE but an outlier.** 13% fewer RRIs (absolute risk difference −13.1%, 95% Bayesian credible interval −23.3 to −3.1), NNT=8. Bayesian analysis, small sample.
- **SYNTHESIS:** generic online education and graded-training interventions do not reduce RRIs (all ~OR 1.0, CIs crossing 1). Only individually-tailored, iterated feedback (TrailS6) showed benefit — and only in a small Bayesian trial. Individualization appears to be the candidate active ingredient.

---

### 7.3 Cycling

#### Injury split: overuse vs traumatic. [CONSENSUS]
- Overuse injuries dominate in road/endurance cycling; traumatic injuries (fractures, lacerations from crashes) dominate in competition and in off-road/BMX.
- Systematic review of competitive cycling: upper-limb injuries most common overall — highest in BMX (65.2%, 95% CI 54.5–74.7), road (48.3%, 95% CI 46.5–50.1), track (44.2%). Skin lacerations/abrasions were the most common type; bone fractures second.

#### Overuse sites and prevalence. [CONSENSUS]
- **Low back pain and anterior knee pain are the two most prevalent overuse complaints.** In professional road cyclists (Clarsen et al.): 58% experienced LBP in the previous 12 months (41% sought medical attention); 36% anterior knee pain (19% sought care). Of time-loss injuries: 57% knee, 22% lower back, 13% lower leg.
- LBP point prevalence ranges 10–60% across studies. Knee pain: amateur 27.6% vs professional 15.9% in one study; lifetime prevalence ~48% in another cohort (period prevalence 26.1% past-month, 18.3% past-week).
- Bike-fit registry (1,505 cyclists, Brazil): lumbar pain 29.1%, hand/finger numbness 21.5%, knee pain 19.5%, neck pain 14%, foot numbness 11.5%.

#### Bike fit — practitioner convention has outrun evidence. [CONTESTED / PRACTITIONER]
- Systematic review (Priego Quesada/Vilas-Boas et al., J Sci Med Sport 2021): **no strong evidence** links any specific bike/body/load measure to overuse injury, and there is **moderate evidence of NO association** for several traditional measures (seat height, knee angle, knee-over-pedal-spindle). The historical emphasis on these measures in bike-fit practice is not evidentially supported for injury prevention. **[Say plainly: bike-fit conventions are largely unvalidated for injury prevention.]**
- Saddle-position SRs (7 reviews, AMSTAR-2 low/critically-low quality): associations reported for LBP and knee injury, but heterogeneous and weak. **[CONTESTED]**

---

### 7.4 Swimming

#### Swimmer's shoulder — prevalence. [CONSENSUS]
- Shoulder pain is the dominant complaint, with prevalence reported as high as ~91%. **Feijen et al. 2020 (J Athl Train; SR, 12 studies, N=1,460): adolescent swimmers showed the highest shoulder-pain rate (91.3%) vs other age groups (range 19.4%–70.3%).** In elite Portuguese swimmers, 42% reported prior-season shoulder pain.

#### Risk factors. [CONTESTED on most variables]
- **McKenzie et al. 2023 (Scand J Med Sci Sports) SR (22 studies):** of 80 assessed variables, **no strong evidence** supported or refuted most associations. Moderate evidence only for competitive level (nondirectional) and shoulder muscle-recruitment profiles (e.g., increased serratus anterior activity). ROM measures, training frequency, stroke specialty, height/weight, sex, and age showed no supported association.
- **Training volume thresholds:** Sein et al. — swimmers training >20 h/week or >60 km/week all had supraspinatus tendinopathy on MRI; >15 h/week roughly doubled tendinopathy odds; **>35 km/week ≈ 4× the supraspinatus tendinopathy rate.** Feijen et al. concluded swim-training volume is associated with shoulder pain in adolescents (Level II).

#### Scapular dyskinesis. [CONTESTED]
- Hickey et al. 2018 (BJSM) SR+MA (5 prospective studies, 419 athletes, mixed overhead populations): scapular dyskinesis associated with a **43% greater risk of developing shoulder pain (pooled RR ≈ 1.43).** 35% of dyskinetic vs 25% of non-dyskinetic athletes developed pain over 9–24 months.
- **CONTESTED:** Hogan et al. 2021 (AJSM) meta-analysis concluded scapular dyskinesis is NOT an isolated risk factor for shoulder injury; swimmer-specific cross-sectional data (Joo & Kim 2025) found no dyskinesis–pain relationship. The link is real but debated.

#### Prevention programs — evidence essentially absent for injury endpoints. [CONTESTED / thin]
- **No SR or RCT demonstrates that dryland/rotator-cuff/scapular programs reduce shoulder pain or injury INCIDENCE in swimmers.** Existing prevention RCTs measure only surrogate outcomes. Correia et al. 2025 RCT: a 12-week weights/elastic-band program reduced progressive rotator-cuff rotational imbalance (isokinetic torque ratios) vs sham — but reported no injury-incidence endpoint.
- SR of therapeutic exercise (2022): programs of <6 exercises performed out-of-water, 2–3×/week for 6 weeks, improved rotator-cuff strength/endurance — again, only risk-factor/surrogate outcomes. **[PRACTITIONER — prevention programs are widely prescribed on mechanistic rationale, not injury-outcome evidence.]**

---

### 7.5 Triathlon / multisport

#### Epidemiology. [CONSENSUS]
- Overuse injuries dominate. Long-distance triathlon SR (Vitale/Carmont et al. 2022): overuse injury incidence 37–91%; acute injury 24–27%. Knee and spine are the most frequent sites; running and cycling are the most-affected disciplines; **swimming is lowest (5–11%).**
- Short-course triathlon SR (Guevara et al. 2023, J Sport Health Sci): injury incidence 15.7–24.3 per 1,000 athlete-exposures; **most injuries occur during running (45–92%);** illness burden mostly GI, cardiovascular, respiratory. Critically, **79–83% of injuries occur in training, not competition** — competition-only datasets substantially underestimate the true burden.
- Long-course training injury incidence: 0.7–5.4 per 1,000 training hours.

#### Run dominance in overuse share. [CONSENSUS]
- Running is associated with the largest share of overuse injuries; cycling with more acute injuries. One cohort found triathletes spend ~48% of training time cycling, 24% running, 12% swimming, 16% other — meaning running produces a **disproportionate injury share relative to its training-time allocation.**

#### Does multisport participation modify per-discipline risk? [CONTESTED / under-studied]
- Elite triathletes show lower overuse incidence (37%, low end of range) and lower acute injury than non-elite (acute up to 27% in non-elite). Whether cross-training distributes load protectively versus this simply reflecting fitness/selection effects is unresolved. Study quality is poor (mostly retrospective cross-sectional; only one long-distance study met >50% of a quality checklist).

---

### 7.6 Systemic risk modifiers

#### Sleep. [CONSENSUS for adolescents; CONTESTED magnitude in adult endurance athletes]
- **Milewski et al. 2014 (J Pediatr Orthop; 112 adolescent athletes, mean age 15):** athletes averaging <8 h sleep/night were **1.7× more likely to be injured (95% CI 1.0–3.0, P=.04);** each additional grade in school conferred 1.4× risk.
- SR+MA: adolescents chronically sleeping <8 h had significantly increased musculoskeletal injury risk (pooled OR 1.58, 95% CI 1.05–2.37, p=0.03) — but only 3 studies, and only 1 in an organized athletic population.
- Adolescent athletes average ~6.3 h sleep vs the recommended 8–10 h; athletes may need more than general-population recommendations. Objective-measure (actigraphy/polysomnography) evidence is sparse; adult-endurance-specific evidence is thin.

#### Energy availability / REDs (IOC 2023 consensus). [CONSENSUS, with active minority debate]
- **IOC 2023 REDs consensus (Mountjoy et al., BJSM):** low energy availability (LEA) drives a syndrome of impaired bone health, endocrine, metabolic, immune, cardiovascular, and other outcomes, in **both female AND male athletes.** Builds on 2014/2018 statements with >170 new studies; introduces the REDs CAT2 clinical tool and a new physiological model. Emphasizes low carbohydrate availability and mental-health interplay.
- LEA/REDs elevates bone stress injury (BSI) risk. Retrospective elite-athlete analysis (von Brackel et al. 2025, J Cachexia Sarcopenia Muscle): REDs diagnosed in 24%; **stress fractures in 70% (REDs) vs 25% (non-REDs), p<0.001;** significantly reduced lumbar-spine and hip Z-scores, suppressed bone formation (osteocalcin, P1NP), increased resorption markers.
- **CONTESTED (scientific-honesty flag):** a 2024 critique (Nutrients) argues the REDs model rests substantially on questionnaire-based/proxy LEA measurement and that clinical trials showing a causal LEA effect remain limited. Present as consensus-with-active-debate, not settled mechanism.

#### Bone stress injuries — risk and return. [CONSENSUS]
- **Incidence:** US military recruits 3.2–5.7 per 1,000 person-years (5–10% develop a BSI in the first 2–3 months of basic training); athletes <5%. Higher in women than men.
- **Risk factors:** LEA/REDs, low BMD, menstrual dysfunction (female athletes), and biomechanical/training factors. Nattiv et al. 2013 (AJSM, 5-yr prospective, collegiate track & field): higher MRI grade and lower total-body BMD independently predicted longer return; trabecular-predominant sites (femoral neck, pubic bone, sacrum) and oligo/amenorrhea associated with more severe/higher-grade injuries.
- **Return timelines by site (Hoenig et al. 2023, BJSM SR+MA):** >90% of athletes returned to sport overall. High-risk sites (femoral neck, anterior tibial shaft, tarsal navicular, fifth metatarsal) carry higher complication rates and more challenging RTS; low-risk sites (posteromedial tibia, fibula, pubic bone) return faster. Conservatively managed tibial BSI: ~6–27 weeks depending on severity.
- **BSI prevention evidence is weak:** foot orthoses may help in military settings (studies at high risk of bias); footwear and training-strategy benefits are unknown, and women/athletes are under-studied. **[CONTESTED]**

#### Training surface / terrain. [CONTESTED — thin, confounded evidence]
- Some evidence associates concrete surfaces with injury (especially in women, per van der Worp SR), but surface evidence is generally low-quality and confounded by pace, volume, and footwear. No strong surface prescription is supported. **[PRACTITIONER]**

---

### 7.7 Injury prediction modeling status

#### Machine-learning injury prediction is NOT deployable. [CONSENSUS]
- Van Eetvelde et al. 2021 (J Exp Orthop) SR (11 studies): Random Forest, gradient boosting, and neural nets show meaningful in-sample prediction in specific scenarios, but small datasets, high label noise, and methodological inconsistency constrain the field.
- Amendolara et al. scoping review: class imbalance and overfitting are the core obstacles to real deployment; in 4 studies logistic regression matched or outperformed ML (e.g., Jauhiainen: logistic AUC 0.65 vs Random Forest 0.63).
- Football-specific ML SR (2026, Aslani et al.): reported accuracy ranged 55–96%, but "should not be interpreted as sufficient evidence to support routine practical implementation" given widespread gaps in calibration, external validation, and real-world deployment. ML should be treated as decision-support, not standalone prediction.
- **SYNTHESIS:** No validated, externally generalizable injury-prediction model exists for endurance athletes. Wearable-based injury-prediction marketing claims outrun the evidence. **[PRACTITIONER for commercial claims]**

#### Recovery modalities marketed for prevention. [CONTESTED / mostly ineffective for prevention]
- **Foam rolling:** acute ROM/DOMS benefit; no injury-prevention evidence; performance effects unclear.
- **Compression garments:** small recovery/DOMS benefit in some meta-analyses (most pronounced >24 h post-exercise); no injury-prevention evidence.
- These are recovery aids at best; none has injury-prevention RCT support. **[PRACTITIONER]**

---

### Open questions
1. Does the Lauersen team-sport strength-training effect (RR ~0.34) transfer quantitatively to endurance athletes? No adequately powered endurance-specific prevention RCT exists.
2. Can gait retraining/cadence manipulation reduce RRI incidence (not just biomechanical surrogates) in adequately powered, multi-site RCTs — or is Chan 2018 an outlier?
3. Why do generic online/educational programs fail (SPRINT n=4,105; INSPIRE n=2,378) while tailored, iterated feedback succeeds (TrailS6)? Is individualization the active ingredient, and can it scale?
4. What are validated, actionable weekly-volume thresholds for swimmer's shoulder beyond the 15 h/week and 35 km/week signals?
5. Are bike-fit modifications ever causally protective, or purely symptom-responsive? No RCT-grade evidence exists.
6. Does REDs cause BSI via a dose-response of LEA, and what are male-specific LEA/energy-availability thresholds?
7. Can any injury-prediction model achieve external validation and calibration sufficient for deployment in endurance athletes?

### Cross-cutting recommendations for the planning system
*(Consistent with the prior review's staged, threshold-driven style. Benchmarks that would change a recommendation are stated explicitly.)*

1. **Prescribe structured resistance/strength training as the primary preventive modality across all disciplines** (best-supported intervention). Flag internally that the magnitude of benefit in endurance athletes is extrapolated from team-sport data. *Threshold to upgrade confidence: publication of an adequately powered endurance-specific prevention RCT showing RR<1 with CI excluding 1.*
2. **Do NOT prescribe static stretching, foam rolling, or compression as injury-prevention interventions.** Permit them only as optional athlete-preference recovery/performance aids, labeled as such.
3. **Treat previous injury as the highest-weight risk flag** for load-cap and monitoring logic. Integrate with — do not replace — existing ramp-rate/ACWR logic from the prior section.
4. **Do not hard-code the "10% rule" as evidence-based.** Treat it as a soft heuristic only (GRONORUN null; Garmin-RUNSAFE shows 72% of RRIs are overuse, favoring cumulative-load monitoring over single ramp caps).
5. **Gate footwear/minimalist and cadence changes behind slow, individualized transition schedules;** never impose abrupt changes. A 5–10% cadence increase is a reasonable, load-reducing default when gait retraining is indicated.
6. **Encode systemic modifiers as first-class constraints:** screen for LEA/REDs (both sexes) before high-load bone-loading blocks; enforce sleep-duration floors (≥8 h, adolescents especially); escalate athletes with BSI history or high-risk-site BSI to conservative, site-specific return timelines (femoral neck / anterior tibia / navicular / 5th metatarsal = extended, higher-complication pathways).
7. **Do NOT present any wearable/ML injury-prediction output as validated.** Treat it as low-confidence decision-support only, with explicit uncertainty labeling.
8. **Discipline-specific rules:** For swimmers, cap/monitor weekly volume (watch the 15 h/week and 35 km/week signals) rather than relying on unproven dryland "prevention." For cyclists, do not present bike-fit changes as evidence-based prevention. For triathletes, weight running as the dominant overuse-injury contributor when allocating and progressing load.

---

## CROSS-CUTTING RECOMMENDATIONS FOR THE PLANNING SYSTEM

1. **Use load models as bookkeeping, not physiology.** Treat CTL/ATL/TSB and TSS as dose indices (Impellizzeri framing). Do NOT present ACWR as an injury predictor; if surfaced at all, label it descriptive. Threshold that would change this: a prospective causal-inference study showing ACWR manipulation reduces injury — none exists as of 2026. [CONSENSUS-grounded]

2. **Default intensity distribution by athlete tier.** Recreational/time-limited: flexible, pyramidal-leaning, intensity as needed. Well-trained/elite in base: pyramidal. Approaching competition: shift toward polarized. Do not hard-code POL as globally superior — the meta-analytic evidence is split (Rosenblat 2019 pro-POL, Silva Oliveira 2024 null). [CONTESTED — build in the moderator logic, not a winner]

3. **Sport-specific load ceilings, not a shared one.** For running, cap single-session distance increases near ≤10% above the 30-day longest run (the datapoint with the strongest evidence) and respect bone/tendon timescales (weeks-to-months) that lag aerobic gains. For cycling, power-based load is robust. For swimming, anchor to CSS for pacing but flag load quantification as unvalidated. [mix of CONSENSUS and CONTESTED]

4. **Do not silently sum triathlon load.** Maintain discipline-specific load tracking in parallel (prioritize running mechanical load and bike+run); expose the caveat that a single combined TSS is not validated. [CONTESTED/UNRESOLVED]

5. **Taper default:** 2 weeks, exponential fast-decay, cut volume 41–60%, hold intensity and frequency; extend frequency maintenance for technical sports (swimming). Expected gain ~2–3%. Change this if athlete is low-volume (shorter taper) or high-technical (protect frequency). [CONSENSUS]

6. **Separate the longevity objective from the performance objective explicitly.** If the user goal is longevity, the plan must include resistance/power training (independent mortality axis), target high-but-not-extreme CRF, and avoid pushing toward the extreme-volume cardiac-risk zone (especially older males). If the goal is performance, accept that some longevity-optimal constraints are relaxed. [CONSENSUS on direction]

## GLOBAL CAVEATS
- Much of the intensity-distribution and block-periodization evidence rests on SMALL, SHORT studies in well-trained but not always elite subjects, with low PEDro scores; effect sizes are real but fragile and sometimes reverse with larger samples.
- Load–adaptation model parameters (Banister, Busso) are derived from tiny samples (often n≤6, sometimes untrained) and reverse-engineered; treat all specific τ/k values as illustrative, not prescriptive.
- Foster monotony/strain thresholds, TSB peaking targets, and sweet-spot zones are practitioner heuristics, not validated cut-points.
- Longevity findings are OBSERVATIONAL (cohort/case-control); they establish strong associations (CRF, strength) but the extreme-exercise cardiac literature cannot yet establish net harm, and confounding by self-selection is unresolved.
- Where a claim is labeled [CONTESTED] or [PRACTITIONER], the planning system should expose uncertainty rather than assert, and should state the moderating variables that drive the decision rather than defaulting to a single answer.