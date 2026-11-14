# User needs and health follow-up scenarios

Report 005. English submission edition. Date: 14 November 2026. Version 1.0. Sequential investigation 1 of 7. Documentary review complete. Human needs validation pending.

## Question, method and conclusion

Which astronaut and medical-team needs justify ARTEMIS HEALTH? Evidence supports investigating information continuity, understanding recorded status and follow-up under mission constraints. It does not establish that this interface meets those needs. Prioritize clear records, source, age, context and interpretation over a global health score.

Primary NASA care, decision-support and human-integration sources were compared with requirements at commit `80be128b17b5046ecd267d5a0604bbc5c74f5444`. README and requirements still identify functional implementation as pending. No astronauts, clinicians or team members were interviewed or contacted. The personas below are hypotheses, not testimonies.

Sources: [NASA CDS concept](https://ntrs.nasa.gov/citations/20205008731), [Health and Medical Care](https://www.nasa.gov/reference/3-0-health-and-medical-care/), [Human Integration Design Handbook](https://www.nasa.gov/organizations/ochmo/human-integration-design-handbook/), [fixed requirements](https://github.com/Jd1278/ARTEMIS/blob/80be128b17b5046ecd267d5a0604bbc5c74f5444/artemis-healt/docs/requirements.md).

The CDS source discusses autonomy, workload and information under resource constraints in a much broader medical system. Handbook use does not establish certification. Product requirements are scope evidence, not proof of demand or clinical benefit.

## Proposed users

| Hypothetical user | Task | Need to test | Design implication |
| --- | --- | --- | --- |
| Crew member | Record and review daily follow-up | Know what exists, its date and meaning | Brief input, history and units |
| Crew medical officer | Organize information for protocols | Distinguish measurements, reports, missing and synthetic data | Visible source and context |
| Ground professional | Review authorized information | Understand sequence, quality and capture conditions | Future traceable summaries |
| Researcher or demo evaluator | Explore information and limits | Separate real studies and fictional profiles | Distinct demo and research spaces |

Existing operations do not show that astronauts lack tools or medical care. The proposed problem is a comprehensible follow-up experience.

## Priority scenarios

Daily check-in: select a fictional profile and mission day, report sleep, fatigue and stress, and consult pulse if an appropriate source exists. Explain scales and distinguish reports from sensors.

Change review: show reference, days used and quality. A difference is not disease. Insufficient compatible history should produce that explicit state.

Save failure: when Supabase is unavailable, preserve the draft during the session and show NOT SAVED. A local page does not eliminate remote persistence dependence. Complete offline storage remains deferred.

Scientific review: keep real studies separate from personal demo history. The P1 scientific view is proposed, not verified.

Individual and crew use: minimize burden, define permissions and avoid public emotional rankings. The product has not been evaluated in solo missions.

## Proposed design decisions

Prioritize four indicators and one small recording/review workflow. Show phase, time, origin, units and quality. Confirm saving only after actual persistence. Separate synthetic, public and reported data in comparisons. Provide reviewed educational explanations and reference mission protocols rather than autonomous clinical recommendations.

These are proposed requirements. Reduced effort, adoption and medical-team usefulness remain unmeasured.

## Prepared interview guide

Propose a consented 20–30-minute session without medical records or personal health questions. Ask about actual work before showing the solution:

1. How do you currently record and review information during an operation or simulation?
2. What context is needed to interpret a change, and what is often missing?
3. Which recording task requires effort or creates confusion?
4. What changes when communication fails or operations transition?
5. Which wellbeing information should remain private, and who could receive it?
6. In a fictional example, what do old, imputed and changed-from-history mean?
7. What must a tool demonstrate to be useful, and what would prevent adoption?

Record general role, context, consented observation and resulting decision. Separate opinion from observed task behavior. Students or analog operators do not automatically represent astronauts.

## Closure

The documentary needs map and interview plan are complete. Human prioritization, acceptable frequency, burden and professional review format remain pending. No evidence of adoption, time savings or willingness to pay exists. Investigation 2 started only after this documentary closure.
