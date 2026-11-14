import type { Indicator, IndicatorKey, OriginType, Profile } from "./types";

// Mission constants from artemis-sleep-dataset/data/reference/crew_roster.csv.
export const MISSION = { name: "SIM-ISS-180", launch: "2026-03-01", days: 180 } as const;

export const INDICATORS: Indicator[] = [
  { key: "sleep_duration_h", label: "Duración del sueño", unit: "h", unit_label: "horas", context: "sleep_report", minimum: 0, maximum: 24, exclusive_minimum: false, integer_only: false, difference_unit: "h" },
  { key: "samn_perelli", label: "Fatiga percibida", unit: "points_1_7", unit_label: "puntos (1–7)", context: "fatigue_report", minimum: 1, maximum: 7, exclusive_minimum: false, integer_only: true, difference_unit: "puntos" },
  { key: "stress_vas", label: "Estrés percibido", unit: "points_0_100", unit_label: "puntos (0–100)", context: "stress_report", minimum: 0, maximum: 100, exclusive_minimum: false, integer_only: false, difference_unit: "puntos" },
  { key: "resting_hr_bpm", label: "Pulso en reposo", unit: "bpm", unit_label: "lpm", context: "rest", minimum: 0, maximum: null, exclusive_minimum: true, integer_only: false, difference_unit: "lpm" },
];

export const INDICATOR_BY_KEY = Object.fromEntries(INDICATORS.map((i) => [i.key, i])) as Record<IndicatorKey, Indicator>;

export const PROFILES: Profile[] = [
  { id: "CM-01", display_name: "CM-01", role: "Comandante", namespace: "demo" },
  { id: "CM-02", display_name: "CM-02", role: "Ingeniera de vuelo 1", namespace: "demo" },
  { id: "CM-03", display_name: "CM-03", role: "Ingeniero de vuelo 2", namespace: "demo" },
  { id: "CM-04", display_name: "CM-04", role: "Ingeniera de vuelo 3", namespace: "demo" },
  { id: "CM-05", display_name: "CM-05", role: "Oficial científico", namespace: "demo" },
  { id: "CM-06", display_name: "CM-06", role: "Oficial médica", namespace: "demo" },
];

export const ORIGIN_LABEL: Record<OriginType, string> = {
  synthetic: "Simulado",
  user_report: "Registro manual",
  public_dataset: "Dato público",
};

export const SCALE_HELP: Record<IndicatorKey, string> = {
  sleep_duration_h: "Horas dormidas que informas tú, de 0 a 24. No es una medición de sensor.",
  samn_perelli: "Escala Samn–Perelli, entero de 1 a 7: 1 = totalmente alerta; 7 = completamente agotado, incapaz de funcionar.",
  stress_vas: "Escala visual analógica de 0 a 100: 0 = nada de estrés; 100 = el máximo estrés imaginable.",
  resting_hr_bpm: "Latidos por minuto medidos en reposo. Debe ser mayor que 0.",
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
  if (flag === "ok") return "Sin incidencias";
  if (flag.endsWith("_imputed")) return "Imputado en origen: excluido";
  if (flag.endsWith("_out_of_range")) return "Fuera de dominio: excluido";
  return flag;
}

/** Technical-domain validation (RF-04). Returns an error message or null. */
export function validateValue(indicator: Indicator, value: number): string | null {
  if (!Number.isFinite(value)) return "Introduce un número válido.";
  if (indicator.integer_only && !Number.isInteger(value)) return "Debe ser un número entero.";
  if (indicator.minimum !== null) {
    if (indicator.exclusive_minimum ? value <= indicator.minimum : value < indicator.minimum)
      return indicator.exclusive_minimum ? `Debe ser mayor que ${indicator.minimum}.` : `Debe ser al menos ${indicator.minimum}.`;
  }
  if (indicator.maximum !== null && value > indicator.maximum) return `Debe ser como máximo ${indicator.maximum}.`;
  return null;
}
