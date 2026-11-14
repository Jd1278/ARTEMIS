import type { EducationCard } from "../../services/types";

// Local educational cards (RF-13). References must be confirmed by I1 before the demo:
// review_status stays "pending review" until someone checks citation and URL.
export const EDUCATION_CARDS: EducationCard[] = [
  {
    indicator: "sleep_duration_h",
    title: "Sleep duration",
    measures: "The hours you believe you slept in your last rest period.",
    how_to_record: "Log the hours when you wake up, using decimals if needed (7.5 = seven and a half hours).",
    scale: "From 0 to 24 hours. It is a self-report: it does not replace actigraphy or polysomnography.",
    limits: [
      "It does not detect sleep disorders or measure sleep quality.",
      "Your own perception may differ from the actual duration.",
      "The comparison only uses your own history, not population ranges.",
    ],
    reference: {
      citation: "NASA Human Research Program — Risk of Performance Decrements and Adverse Health Outcomes Resulting from Sleep Loss, Circadian Desynchronization, and Work Overload.",
      url: "https://humanresearchroadmap.nasa.gov/",
      review_status: "pending review",
    },
  },
  {
    indicator: "samn_perelli",
    title: "Perceived fatigue (Samn–Perelli)",
    measures: "How tired you feel right now.",
    how_to_record: "Pick a single whole number from 1 to 7 that best matches the description.",
    scale: "1 = fully alert, wide awake; 4 = a little tired, less than fresh; 7 = completely exhausted, unable to function effectively.",
    limits: [
      "It is a subjective seven-point scale; it does not measure performance.",
      "Differences are expressed in points, never in percentages.",
      "It does not indicate whether there is a health problem.",
    ],
    reference: {
      citation: "Samn, S. W. & Perelli, L. P. (1982). Estimating aircrew fatigue: a technique with application to airlift operations. USAF School of Aerospace Medicine, SAM-TR-82-21.",
      url: null,
      review_status: "pending review",
    },
  },
  {
    indicator: "stress_vas",
    title: "Perceived stress (visual analogue scale)",
    measures: "How intense the stress you perceive is right now.",
    how_to_record: "Enter a value from 0 to 100 where you would mark your stress on a continuous line.",
    scale: "0 = no stress at all; 100 = the worst stress imaginable. Intermediate values have no fixed labels.",
    limits: [
      "It is a personal rating and changes with the context of the day.",
      "It is not a validated psychological test for diagnosis.",
      "Differences are expressed in points, not in percentages.",
    ],
    reference: {
      citation: "Lesage, F.-X., Berjot, S. & Deschamps, F. (2012). Clinical stress assessment using a visual analogue scale. Occupational Medicine, 62(8), 600–605.",
      url: "https://doi.org/10.1093/occmed/kqs140",
      review_status: "pending review",
    },
  },
  {
    indicator: "resting_hr_bpm",
    title: "Resting pulse",
    measures: "Heartbeats per minute at rest.",
    how_to_record: "Measure it after a few minutes sitting or lying down calmly, always under similar conditions.",
    scale: "Beats per minute (bpm). The only technical limit is that it must be greater than 0.",
    limits: [
      "It changes with posture, recent activity, caffeine or the time of day.",
      "A single value means nothing on its own.",
      "The app does not classify the pulse as normal or abnormal.",
    ],
    reference: {
      citation: "NASA Human Research Program — Risk of Cardiovascular Adaptations Contributing to Adverse Mission Performance and Health Outcomes.",
      url: "https://humanresearchroadmap.nasa.gov/",
      review_status: "pending review",
    },
  },
];
