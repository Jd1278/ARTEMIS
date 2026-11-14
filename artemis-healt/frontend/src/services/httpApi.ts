import { ApiError, type ArtemisApi } from "./api";
import { dateToMissionDay, INDICATOR_BY_KEY, INDICATORS, PROFILES } from "./domain";
import { EDUCATION_CARDS } from "../features/education/content";
import { BASELINE_V1 } from "../features/analysis/baseline";
import type {
  CaptureMethod,
  Comparison,
  Dashboard,
  EducationCard,
  IndicatorKey,
  NewObservation,
  Observation,
  ObservationQuery,
  OriginType,
  Profile,
  SaveResult,
} from "./types";

/*
 * Adapter for the FastAPI backend (src/artemis_health, docs/api_endpoints.md).
 * The backend wraps lists, names timestamps `measured_at` and returns comparison fields with
 * its own names; this file translates them to the contract the screens use (services/types.ts).
 * History is requested with strict_indicator=true so the 1–7 / 0–100 scales are never mixed
 * with the backend's 1–5 check-in scales (requirements.md: no convertir a 1–5).
 */

const P0_KEYS = new Set<string>(INDICATORS.map((i) => i.key));
const ERROR_FIELD_ALIASES: Record<string, string> = { measured_at: "timestamp" };
const ERROR_FIELDS = new Set(["value", "unit", "context", "timestamp", "profile_id", "indicator"]);

// The backend writes messages in Spanish; the UI is English, so messages are chosen by status here.
const STATUS_MESSAGE: Record<number, string> = {
  404: "The requested resource was not found.",
  409: "An observation with this ID already exists with different content.",
  422: "The observation is not valid.",
};
const FIELD_MESSAGE: Record<string, string> = {
  value: "Value outside the technical range for this indicator.",
  unit: "Unit not compatible with the indicator.",
  context: "Context not compatible with the indicator.",
  timestamp: "Invalid date.",
  profile_id: "Unknown profile.",
  indicator: "Unknown indicator.",
};

// ---- Backend response shapes (subset actually used) ----
export interface BackendObservation {
  id: string;
  profile_id: string;
  namespace?: string;
  indicator: string;
  value: number | null;
  source_value?: number | null;
  unit: string;
  context: string;
  measured_at: string;
  timestamp?: string;
  mission_day?: number | null;
  origin_type: string;
  capture_method: string;
  source_reference?: string | null;
  quality_flag?: string;
  quality_flags?: string[];
}

export interface BackendComparison {
  indicator: string;
  unit: string;
  context: string;
  origin_type: string;
  rule_version: string;
  reference_timestamp: string;
  current_value: number | null;
  baseline_median: number | null;
  difference: number | null;
  sufficient_history: boolean;
  status: string;
  days_used: number;
  minimum_days_required: number;
  period_start: string | null;
  period_end: string | null;
  descriptive_notice: string;
  reference_observation_ids?: string[];
}

interface BackendEducation {
  indicator: string;
  title: string;
  description: string;
  limitations: string;
  bibliographic_reference: string;
}

// ---- HTTP plumbing ----
function normalizeFields(raw: unknown): Record<string, string> {
  const out: Record<string, string> = {};
  if (!raw || typeof raw !== "object") return out;
  for (const [k, v] of Object.entries(raw as Record<string, unknown>)) {
    const key = ERROR_FIELD_ALIASES[k] ?? k;
    if (!ERROR_FIELDS.has(key)) continue;
    if (v != null) out[key] = FIELD_MESSAGE[key];
  }
  return out;
}

async function request<T>(path: string, init?: RequestInit): Promise<{ status: number; data: T }> {
  let response: Response;
  try {
    response = await fetch(path, { headers: { "Content-Type": "application/json", Accept: "application/json" }, ...init });
  } catch {
    throw new ApiError(0, { code: "network_unavailable", message: "Could not reach the server.", fields: {}, request_id: "" });
  }
  const text = await response.text();
  let body: Record<string, unknown> | null = null;
  try {
    body = text ? JSON.parse(text) : null;
  } catch {
    body = null;
  }
  if (!response.ok) {
    throw new ApiError(response.status, {
      code: String(body?.code ?? `http_${response.status}`),
      message: response.status >= 500 ? "The server is unavailable." : (STATUS_MESSAGE[response.status] ?? "The request could not be completed."),
      fields: normalizeFields(body?.fields),
      request_id: String(body?.request_id ?? response.headers.get("x-request-id") ?? ""),
    });
  }
  return { status: response.status, data: body as T };
}

const qs = (params: Record<string, string | undefined>) => {
  const p = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) if (v) p.set(k, v);
  const s = p.toString();
  return s ? `?${s}` : "";
};

// ---- Mappers ----
export function toObservation(o: BackendObservation): Observation {
  const timestamp = o.timestamp ?? o.measured_at;
  const flags = o.quality_flags?.length ? o.quality_flags : [o.quality_flag ?? "ok"];
  return {
    id: o.id,
    profile_id: o.profile_id,
    indicator: o.indicator as IndicatorKey,
    value: o.value,
    source_value: o.source_value ?? o.value,
    unit: o.unit,
    timestamp,
    mission_day: o.mission_day ?? dateToMissionDay(timestamp),
    context: o.context,
    namespace: o.namespace === "research" ? "research" : "demo",
    origin_type: o.origin_type as OriginType,
    capture_method: o.capture_method as CaptureMethod,
    quality_flags: flags,
    source_file: o.capture_method === "import" ? (o.source_reference ?? null) : null,
    source_row: null,
  };
}

export function toComparison(c: BackendComparison, profileId: string, at: string): Comparison {
  const indicator = c.indicator as IndicatorKey;
  const current: Observation | null =
    c.current_value === null
      ? null
      : {
          id: `current:${c.reference_timestamp}`,
          profile_id: profileId,
          indicator,
          value: c.current_value,
          source_value: c.current_value,
          unit: c.unit,
          timestamp: c.reference_timestamp,
          mission_day: dateToMissionDay(c.reference_timestamp),
          context: c.context,
          namespace: "demo",
          origin_type: c.origin_type as OriginType,
          capture_method: c.origin_type === "user_report" ? "manual" : "import",
          quality_flags: ["ok"],
          source_file: null,
          source_row: null,
        };
  const sufficient = c.sufficient_history && c.baseline_median !== null && current !== null;
  return {
    profile_id: profileId,
    indicator,
    rule_version: c.rule_version,
    at,
    origin_type: c.origin_type as OriginType,
    current,
    baseline: c.baseline_median,
    difference: c.difference,
    days_used: c.days_used,
    minimum_days: c.minimum_days_required,
    period_from: c.period_start ? `${c.period_start.slice(0, 10)}T00:00:00Z` : null,
    period_to: c.period_end ? `${c.period_end.slice(0, 10)}T00:00:00Z` : null,
    sufficient,
    reference_observation_ids: c.reference_observation_ids ?? [],
    explanation: explain(c, current !== null, sufficient),
  };
}

/** English explanation built from the backend numbers (its descriptive_notice is in Spanish). */
function explain(c: BackendComparison, hasCurrent: boolean, sufficient: boolean): string {
  if (!hasCurrent) return "There is no valid value up to the selected day.";
  if (!sufficient)
    return `Insufficient history: ${c.days_used} of ${c.minimum_days_required} valid days required in the previous ${BASELINE_V1.window_days} days.`;
  return `Median of ${c.days_used} previous valid days (up to ${BASELINE_V1.max_days}, ${BASELINE_V1.window_days}-day window, excluding the current day and excluded values).`;
}

/**
 * Education text stays the local English card (the backend's text is Spanish);
 * the backend only contributes its bibliographic reference, which is already in English.
 */
export function toEducation(indicator: IndicatorKey, b: BackendEducation | null): EducationCard {
  const local = EDUCATION_CARDS.find((c) => c.indicator === indicator)!;
  if (!b?.bibliographic_reference) return local;
  return { ...local, reference: { citation: b.bibliographic_reference, url: null, review_status: "reference provided by the backend" } };
}

// ---- API ----
export const httpApi: ArtemisApi = {
  mode: "http",

  async listProfiles(): Promise<Profile[]> {
    const { data } = await request<{ profiles: { id: string; display_name: string; role?: string }[] }>("/api/profiles");
    // The UI shows the six fictional crew; the backend's extra "demo" alias profile is omitted.
    const known = new Map(PROFILES.map((p) => [p.id, p]));
    return data.profiles.filter((p) => known.has(p.id)).map((p) => known.get(p.id)!);
  },

  listIndicators: async () => INDICATORS,

  async getDashboard(id, at): Promise<Dashboard> {
    const { data } = await request<{ indicators_summary: { indicator: string; latest_observation: BackendObservation | null }[] }>(
      `/api/profiles/${encodeURIComponent(id)}/dashboard${qs({ at })}`,
    );
    const items = INDICATORS.map(({ key }) => {
      const card = data.indicators_summary.find((c) => c.indicator === key);
      const latest = card?.latest_observation ? toObservation(card.latest_observation) : null;
      return { indicator: key, latest, latest_valid: latest && latest.value !== null ? latest : null };
    });
    return { profile_id: id, at, mission_day: dateToMissionDay(at), items };
  },

  async createObservation(input: NewObservation): Promise<SaveResult> {
    const body = {
      id: input.id,
      profile_id: input.profile_id,
      indicator: input.indicator,
      value: input.value,
      unit: input.unit,
      context: input.context,
      measured_at: input.timestamp,
      mission_day: input.mission_day,
      origin_type: "user_report",
      capture_method: "manual",
      namespace: "demo",
    };
    const { status, data } = await request<{ observation: BackendObservation }>("/api/observations", { method: "POST", body: JSON.stringify(body) });
    return { status: status === 201 ? 201 : 200, observation: toObservation(data.observation) };
  },

  async listObservations(id, query: ObservationQuery = {}): Promise<Observation[]> {
    const { data } = await request<{ observations: BackendObservation[] }>(
      `/api/profiles/${encodeURIComponent(id)}/observations${qs({ indicator: query.indicator, from: query.from, to: query.to, strict_indicator: "true" })}`,
    );
    return data.observations
      .filter((o) => P0_KEYS.has(o.indicator) && (o.namespace ?? "demo") === "demo")
      .map(toObservation)
      .sort((a, b) => a.timestamp.localeCompare(b.timestamp));
  },

  async getComparison(id, indicator, at): Promise<Comparison> {
    const { data } = await request<BackendComparison>(`/api/profiles/${encodeURIComponent(id)}/comparison${qs({ indicator, at })}`);
    return toComparison(data, id, at);
  },

  async getEducation(indicator): Promise<EducationCard> {
    if (!INDICATOR_BY_KEY[indicator]) throw new ApiError(404, { code: "not_found", message: "Card not found.", fields: {}, request_id: "" });
    try {
      const { data } = await request<BackendEducation>(`/api/education/${indicator}`);
      return toEducation(indicator, data);
    } catch (e) {
      if (e instanceof ApiError && e.status === 404) return toEducation(indicator, null);
      throw e;
    }
  },
};
