# Usability and comprehension of health follow-up

Report 009. English submission edition. Date: 14 November 2026. Version 1.0. Sequential investigation 5 of 7. Methodological review complete. No human tests performed.

## Question and method

How can the team establish that users understand a panel without mistaking observations for diagnoses? Observe tasks and explanations, errors and time. Attractive design, automated checks or developer opinion do not establish human comprehension.

After report 008, primary evaluation and accessibility sources were reviewed. No participants or simulated responses were used. This report provides a protocol and [empty recording template](../templates/009_usability_record.csv), not user results.

## Evidence

[NIST Usability Testing](https://www.nist.gov/programs-projects/usability-testing) describes task completion, errors, time and qualitative observations to examine effectiveness, efficiency and satisfaction in a defined context.

[NASA Systems Engineering Processes](https://www.nasa.gov/reference/3-0-systems-engineering-processes-vol-2/) describes iterative human-in-the-loop testing for operational and interface issues. This formative adaptation is not aerospace certification.

[W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) provides keyboard, label, contrast and non-color communication criteria. Passing selected checks does not establish full conformance.

## Questions to test

Can the person distinguish synthetic from manual records, missing from zero, and old from current data? Do they understand descriptive comparison and insufficient history? Can they recognize a failed save and recover a draft? Can they use keyboard navigation and a small screen?

Visible origin and explanations may reduce confusion, while brief forms may reduce burden. These are hypotheses.

## Prepared formative protocol

Invite adults from an available context and separately seek medical/operations experience. A proposed five-to-eight-person pilot can identify issues, not estimate population performance or represent astronauts. Use codes, general roles and no personal medical information.

Obtain consent, allow withdrawal and use fictional scenarios and a fixed interface version. Do not induce sleep deprivation, stress or physical exposure. If a mockup is used, assess that mockup rather than software persistence.

Explain that the tool is being evaluated. Give tasks without pointing to controls, observe, record assistance and then ask for interpretation. Explanation by the moderator during a task changes the measurement and needs recording.

| Task | Expected evidence | Important error |
| --- | --- | --- |
| T1 Latest observation | Correct value, unit, time and origin | Treating fictional data as an actual astronaut record |
| T2 Fictional input | Correct scale and saving state | Assuming sent means stored despite failure |
| T3 Missing values | Recognizing absence | Reading no data as healthy or zero |
| T4 Comparison | Reference, period and descriptive meaning | Inferring diagnosis or guaranteed safety |
| T5 Profile/origin change | Distinct histories | Mixing people or sources |
| T6 Simulated connection failure | NOT SAVED and draft recovery | Believing durable offline storage already exists |

## Metrics and proposed criteria

Record unassisted success, assisted success or failure, time, number/type of helps, errors, explanation and a clearly labeled nonvalidated ease question. Do not call that question SUS or NASA-TLX.

Preserve the engineering goal of finding main information within two screens. Set any timing goal before testing. Record denominators, withdrawals and unexecutable tasks. Missing results are not zero. A medical interpretation or save-confirmation error merits investigation even if other tasks perform well. Small pilots should report case details and counts rather than generalized astronaut satisfaction rates.

## Accessibility review prepared

Check focus and keyboard operation, control names, field errors, text with states, table alternatives to charts, zoom and planned screen sizes. WCAG AA's normal-text contrast reference is 4.5:1, with conditions and exceptions. A compliant color token does not establish application compliance.

## Closure

The rationale, tasks, protocol and template are complete. A testable interface, consent and sessions remain pending. The correct presentation claim is that a comprehension evaluation is prepared, not that astronauts validated the experience. Operational investigation followed without treating human validation as complete.
