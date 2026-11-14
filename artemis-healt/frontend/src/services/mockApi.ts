import { ApiError, type ArtemisApi } from "./api";
import { INDICATOR_BY_KEY, INDICATORS, PROFILES, validateValue } from "./domain";
import { compareBaseline } from "../features/analysis/baseline";
import { EDUCATION_CARDS } from "../features/education/content";
import type { DashboardItem, NewObservation, Observation, ObservationQuery } from "./types";

/**
 * In-browser implementation of the API contract over data/demo/observations.json.
 * Manual captures live in memory only (lost on reload) — the real persistence is Supabase via the backend.
 * Set window.__ARTEMIS_SIMULATE_OUTAGE__ = true (or use the toggle in /componentes) to test RF-14/RF-15.
 */
declare global {
  interface Window {
    __ARTEMIS_SIMULATE_OUTAGE__?: boolean;
  }
}

let dataset: Promise<Observation[]> | null = null;
const manual = new Map<string, Observation>();

function load(): Promise<Observation[]> {
  dataset ??= import("@demo-data/observations.json").then((m) => {
    const rows = (m.default as unknown as Observation[]).slice();
    rows.sort((a, b) => a.timestamp.localeCompare(b.timestamp));
    return rows;
  });
  return dataset;
}

async function all(): Promise<Observation[]> {
  const rows = await load();
  return manual.size ? [...rows, ...manual.values()].sort((a, b) => a.timestamp.localeCompare(b.timestamp)) : rows;
}

const requestId = () => crypto.randomUUID();
const delay = (ms = 120) => new Promise((r) => setTimeout(r, ms));

async function guard() {
  await delay();
  if (window.__ARTEMIS_SIMULATE_OUTAGE__) {
    throw new ApiError(503, { code: "database_unavailable", message: "The database is unavailable.", fields: {}, request_id: requestId() });
  }
}

function invalid(fields: Record<string, string>): never {
  throw new ApiError(422, { code: "validation_error", message: "The observation is not valid.", fields, request_id: requestId() });
}

function notFound(what: string): never {
  throw new ApiError(404, { code: "not_found", message: `${what} not found.`, fields: {}, request_id: requestId() });
}

const sameContent = (a: Observation, b: NewObservation) =>
  a.profile_id === b.profile_id && a.indicator === b.indicator && a.value === b.value && a.unit === b.unit && a.context === b.context && Date.parse(a.timestamp) === Date.parse(b.timestamp);

export const mockApi: ArtemisApi = {
  mode: "mock",

  async listProfiles() {
    await guard();
    return PROFILES;
  },

  async listIndicators() {
    await guard();
    return INDICATORS;
  },

  async getDashboard(profileId, at) {
    await guard();
    if (!PROFILES.some((p) => p.id === profileId)) notFound("Profile");
    const atMs = Date.parse(at);
    const rows = (await all()).filter((o) => o.profile_id === profileId && Date.parse(o.timestamp) <= atMs);
    const items: DashboardItem[] = INDICATORS.map(({ key }) => {
      const own = rows.filter((o) => o.indicator === key);
      return {
        indicator: key,
        latest: own.at(-1) ?? null,
        latest_valid: [...own].reverse().find((o) => o.value !== null) ?? null,
      };
    });
    const missionDay = Math.max(0, ...rows.map((r) => r.mission_day ?? 0));
    return { profile_id: profileId, at, mission_day: missionDay, items };
  },

  async createObservation(input) {
    await guard();
    const fields: Record<string, string> = {};
    const indicator = INDICATOR_BY_KEY[input.indicator];
    if (!/^[0-9a-f-]{36}$/i.test(input.id)) fields.id = "Invalid UUID.";
    if (!PROFILES.some((p) => p.id === input.profile_id)) fields.profile_id = "Unknown profile.";
    if (!indicator) fields.indicator = "Unknown indicator.";
    else {
      if (input.unit !== indicator.unit) fields.unit = "Unit not compatible with the indicator.";
      if (input.context !== indicator.context) fields.context = "Context not compatible with the indicator.";
      const err = validateValue(indicator, input.value);
      if (err) fields.value = err;
    }
    if (!input.timestamp || Number.isNaN(Date.parse(input.timestamp))) fields.timestamp = "Invalid date.";
    if (Object.keys(fields).length) invalid(fields);

    const existing = manual.get(input.id);
    if (existing) {
      if (sameContent(existing, input)) return { status: 200, observation: existing };
      throw new ApiError(409, { code: "conflict", message: "An observation with this ID already exists with different content.", fields: { id: "UUID already in use." }, request_id: requestId() });
    }
    const observation: Observation = {
      id: input.id,
      profile_id: input.profile_id,
      indicator: input.indicator,
      value: input.value,
      source_value: input.value,
      unit: input.unit,
      timestamp: new Date(input.timestamp).toISOString(),
      mission_day: input.mission_day,
      context: input.context,
      namespace: "demo",
      origin_type: "user_report",
      capture_method: "manual",
      quality_flags: ["ok"],
      source_file: null,
      source_row: null,
    };
    manual.set(observation.id, observation);
    return { status: 201, observation };
  },

  async listObservations(profileId, query: ObservationQuery = {}) {
    await guard();
    const from = query.from ? Date.parse(query.from) : -Infinity;
    const to = query.to ? Date.parse(query.to) : Infinity;
    return (await all()).filter((o) => {
      const t = Date.parse(o.timestamp);
      return o.profile_id === profileId && (!query.indicator || o.indicator === query.indicator) && t >= from && t <= to;
    });
  },

  async getComparison(profileId, indicator, at) {
    await guard();
    return compareBaseline({ observations: await all(), profileId, indicator, at });
  },

  async getEducation(indicator) {
    await guard();
    return EDUCATION_CARDS.find((c) => c.indicator === indicator) ?? notFound("Card");
  },
};
