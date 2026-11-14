import type { Indicator, IndicatorKey, OriginType, Profile } from "./types";

// Mission constants from artemis-sleep-dataset/data/reference/crew_roster.csv.
export const MISSION = { name: "SIM-ISS-180", launch: "2026-03-01", days: 180 } as const;

export const INDICATORS: Indicator[] = [
  { key: "sleep_duration_h", label: "Sleep duration", unit: "h", unit_label: "hours", context: "sleep_report", minimum: 0, maximum: 24, exclusive_minimum: false, integer_only: false, difference_unit: "h" },
  { key: "samn_perelli", label: "Perceived fatigue", unit: "points_1_7", unit_label: "points (1–7)", context: "fatigue_report", minimum: 1, maximum: 7, exclusive_minimum: false, integer_only: true, difference_unit: "points" },
  { key: "stress_vas", label: "Perceived stress", unit: "points_0_100", unit_label: "points (0–100)", context: "stress_report", minimum: 0, maximum: 100, exclusive_minimum: false, integer_only: false, difference_unit: "points" },
  { key: "resting_hr_bpm", label: "Resting pulse", unit: "bpm", unit_label: "bpm", context: "rest", minimum: 0, maximum: null, exclusive_minimum: true, integer_only: false, difference_unit: "bpm" },
];

export const INDICATOR_BY_KEY = Object.fromEntries(INDICATORS.map((i) => [i.key, i])) as Record<IndicatorKey, Indicator>;

export const PROFILES: Profile[] = [
  { id: "CM-01", display_name: "CM-01", role: "Commander", namespace: "demo" },
  { id: "CM-02", display_name: "CM-02", role: "Flight Engineer 1", namespace: "demo" },
  { id: "CM-03", display_name: "CM-03", role: "Flight Engineer 2", namespace: "demo" },
  { id: "CM-04", display_name: "CM-04", role: "Flight Engineer 3", namespace: "demo" },
  { id: "CM-05", display_name: "CM-05", role: "Science Officer", namespace: "demo" },
  { id: "CM-06", display_name: "CM-06", role: "Medical Officer", namespace: "demo" },
];

export const ORIGIN_LABEL: Record<OriginType, string> = {
  synthetic: "Simulated",
  user_report: "Manual entry",
  public_dataset: "Public data",
};

export const SCALE_HELP: Record<IndicatorKey, string> = {
  sleep_duration_h: "Hours slept as you report them, from 0 to 24. Not a sensor measurement.",
  samn_perelli: "Samn–Perelli scale, whole number from 1 to 7: 1 = fully alert; 7 = completely exhausted, unable to function.",
  stress_vas: "Visual analogue scale from 0 to 100: 0 = no stress at all; 100 = the worst stress imaginable.",
  resting_hr_bpm: "Beats per minute measured at rest. Must be greater than 0.",
};

/** Mission day 1 = launch date. Returns the UTC date (YYYY-MM-DD) for a mission day. */
export function missionDayToDate(day: number): string {
  const d = new Date(`${MISSION.launch}T00:00:00Z`);
  d.setUTCDate(d.getUTCDate() + day - 1);
  return d.toISOString().slice(0, 10);
}

/** End of the given mission day (UTC), used as the "at" cursor. */
export function missionDayCursor(day: number): string {
  return `${missionDayToDate(day)}T23:59:59Z`;
}

export function dateToMissionDay(isoDate: string): number {
  const launch = Date.parse(`${MISSION.launch}T00:00:00Z`);
  const t = Date.parse(`${isoDate.slice(0, 10)}T00:00:00Z`);
  return Math.round((t - launch) / 86_400_000) + 1;
}

/** Flags that force value=null and exclude the row from any calculation. */
export function isExcludedFlag(flag: string): boolean {
  return flag.endsWith("_imputed") || flag.endsWith("_out_of_range");
}

export function describeFlag(flag: string): string {
  if (flag === "ok") return "No issues";
  if (flag.endsWith("_imputed")) return "Imputed at source: excluded";
  if (flag.endsWith("_out_of_range")) return "Out of range: excluded";
  return flag;
}

/** Technical-domain validation (RF-04). Returns an error message or null. */
export function validateValue(indicator: Indicator, value: number): string | null {
  if (!Number.isFinite(value)) return "Enter a valid number.";
  if (indicator.integer_only && !Number.isInteger(value)) return "Must be a whole number.";
  if (indicator.minimum !== null) {
    if (indicator.exclusive_minimum ? value <= indicator.minimum : value < indicator.minimum)
      return indicator.exclusive_minimum ? `Must be greater than ${indicator.minimum}.` : `Must be at least ${indicator.minimum}.`;
  }
  if (indicator.maximum !== null && value > indicator.maximum) return `Must be at most ${indicator.maximum}.`;
  return null;
}
