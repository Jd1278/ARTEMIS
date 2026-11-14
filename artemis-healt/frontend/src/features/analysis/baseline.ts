import type { Comparison, IndicatorKey, Observation, OriginType } from "../../services/types";

/** Rule configuration mirrored from artemis.rule_versions ('baseline_v1'). */
export const BASELINE_V1 = {
  version: "baseline_v1",
  window_days: 30,
  max_days: 14,
  minimum_days: 7,
  exclude_current_day: true,
  exclude_imputed: true,
} as const;

const DAY_MS = 86_400_000;
const utcDay = (iso: string) => Math.floor(Date.parse(iso) / DAY_MS);

export function median(values: number[]): number {
  const s = [...values].sort((a, b) => a - b);
  const m = s.length >> 1;
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
}

interface CompareInput {
  observations: Observation[];
  profileId: string;
  indicator: IndicatorKey;
  at: string;
  /** Comparisons never mix origins (synthetic vs user_report). Defaults to the current observation's origin. */
  originType?: OriginType;
}

/**
 * Causal personal-baseline comparison (RF-09/10/11).
 * - current: latest valid observation on the cursor day (else latest at/before cursor).
 * - baseline: median of the last valid observation per day, for up to 14 days
 *   strictly before the cursor day and within 30 days; at least 7 days required.
 * - Same profile, indicator, context, unit and origin. Null values never count.
 */
export function compareBaseline({ observations, profileId, indicator, at, originType }: CompareInput): Comparison {
  const atMs = Date.parse(at);
  const cursorDay = utcDay(at);
  const candidates = observations
    .filter((o) => o.profile_id === profileId && o.indicator === indicator && o.namespace === "demo" && Date.parse(o.timestamp) <= atMs)
    .sort((a, b) => Date.parse(a.timestamp) - Date.parse(b.timestamp));

  const current =
    [...candidates].reverse().find((o) => o.value !== null && (originType ? o.origin_type === originType : true)) ?? null;
  const origin: OriginType = originType ?? current?.origin_type ?? "synthetic";

  const base: Comparison = {
    profile_id: profileId,
    indicator,
    rule_version: BASELINE_V1.version,
    at,
    origin_type: origin,
    current,
    baseline: null,
    difference: null,
    days_used: 0,
    minimum_days: BASELINE_V1.minimum_days,
    period_from: null,
    period_to: null,
    sufficient: false,
    reference_observation_ids: [],
    explanation: "",
  };

  if (!current) {
    return { ...base, explanation: "No hay un valor válido hasta el día seleccionado." };
  }

  // Reference days are counted relative to the day of the current observation.
  const refDay = utcDay(current.timestamp);
  const lastPerDay = new Map<number, Observation>();
  for (const o of candidates) {
    if (o.value === null) continue; // imputed / out of range are excluded
    if (o.origin_type !== origin || o.context !== current.context || o.unit !== current.unit) continue;
    const day = utcDay(o.timestamp);
    if (day >= refDay || day > cursorDay) continue; // exclude current and future days
    if (day < refDay - BASELINE_V1.window_days) continue;
    lastPerDay.set(day, o); // sorted ascending → keeps the last of each day
  }
  const days = [...lastPerDay.keys()].sort((a, b) => b - a).slice(0, BASELINE_V1.max_days);
  const refs = days.map((d) => lastPerDay.get(d)!).sort((a, b) => Date.parse(a.timestamp) - Date.parse(b.timestamp));

  const withPeriod = {
    ...base,
    days_used: refs.length,
    period_from: refs[0]?.timestamp ?? null,
    period_to: refs.at(-1)?.timestamp ?? null,
    reference_observation_ids: refs.map((r) => r.id),
  };

  if (refs.length < BASELINE_V1.minimum_days) {
    return {
      ...withPeriod,
      explanation: `Historial insuficiente: ${refs.length} de ${BASELINE_V1.minimum_days} días válidos necesarios en los ${BASELINE_V1.window_days} días previos.`,
    };
  }

  const baseline = median(refs.map((r) => r.value as number));
  const difference = (current.value as number) - baseline;
  return {
    ...withPeriod,
    baseline,
    difference,
    sufficient: true,
    explanation: `Mediana de ${refs.length} días válidos previos (máximo ${BASELINE_V1.max_days}, ventana de ${BASELINE_V1.window_days} días, sin el día actual ni valores excluidos).`,
  };
}
