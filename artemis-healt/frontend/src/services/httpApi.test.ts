import { afterEach, describe, expect, it, vi } from "vitest";
import { ApiError } from "./api";
import { httpApi, toComparison, toObservation, type BackendComparison, type BackendObservation } from "./httpApi";

// Fixtures captured from the running backend (GET/POST on /api, SQLite demo seed).
const OBS: BackendObservation = {
  id: "c0aab7fa-cc39-5b98-a5c0-c13b27d7a239",
  profile_id: "CM-03",
  namespace: "demo",
  indicator: "stress_vas",
  value: 27.2,
  source_value: 27.2,
  unit: "points_0_100",
  context: "stress_report",
  measured_at: "2026-03-01T07:09:00Z",
  timestamp: "2026-03-01T07:09:00Z",
  mission_day: 1,
  origin_type: "synthetic",
  capture_method: "import",
  source_reference: "crew_daily_log_clean.csv",
  quality_flag: "ok",
  quality_flags: ["ok"],
};

const CMP_OK: BackendComparison = {
  indicator: "sleep_duration_h",
  unit: "h",
  context: "sleep_report",
  origin_type: "synthetic",
  rule_version: "baseline_v1",
  reference_timestamp: "2026-04-29T06:35:00Z",
  current_value: 6.02,
  baseline_median: 6.7,
  difference: -0.68,
  sufficient_history: true,
  status: "comparison_available",
  days_used: 14,
  minimum_days_required: 7,
  period_start: "2026-04-15",
  period_end: "2026-04-28",
  descriptive_notice: "Regla baseline_v1: …",
  reference_observation_ids: ["a", "b"],
};

const json = (status: number, body: unknown) =>
  Promise.resolve(new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } }));

afterEach(() => vi.unstubAllGlobals());

describe("mappers", () => {
  it("maps backend observations to the screen contract", () => {
    const o = toObservation({ ...OBS, timestamp: undefined, mission_day: null, capture_method: "manual", origin_type: "user_report" });
    expect(o.timestamp).toBe("2026-03-01T07:09:00Z");
    expect(o.mission_day).toBe(1); // derived from the date when the backend omits it
    expect(o.source_file).toBeNull(); // manual captures have no source file
  });

  it("maps a sufficient comparison and builds the current value", () => {
    const c = toComparison(CMP_OK, "CM-01", "2026-04-29T23:59:59Z");
    expect(c.sufficient).toBe(true);
    expect(c.baseline).toBe(6.7);
    expect(c.current?.value).toBe(6.02);
    expect(c.current?.mission_day).toBe(60);
    expect(c.period_from).toBe("2026-04-15T00:00:00Z");
    expect(c.minimum_days).toBe(7);
  });

  it("maps insufficient history with no current value", () => {
    const c = toComparison(
      { ...CMP_OK, current_value: null, baseline_median: null, difference: null, sufficient_history: false, status: "insufficient_history", days_used: 5 },
      "CM-01",
      "2026-03-06T23:59:59Z",
    );
    expect(c.sufficient).toBe(false);
    expect(c.current).toBeNull();
    expect(c.days_used).toBe(5);
  });
});

describe("httpApi", () => {
  it("unwraps history, asks for strict scales and drops 1–5 check-in indicators", async () => {
    const fetchMock = vi.fn(() => json(200, { observations: [OBS, { ...OBS, id: "x", indicator: "fatigue", unit: "scale_1_5" }] }));
    vi.stubGlobal("fetch", fetchMock);
    const rows = await httpApi.listObservations("CM-03", { indicator: "stress_vas", to: "2026-03-08T23:59:59Z" });
    expect(rows.map((r) => r.indicator)).toEqual(["stress_vas"]);
    expect(String((fetchMock.mock.calls[0] as unknown[])[0])).toContain("strict_indicator=true");
  });

  it("sends measured_at and reports 201 vs 200 replay", async () => {
    const fetchMock = vi
      .fn()
      .mockImplementationOnce(() => json(201, { status: "created", observation: { ...OBS, origin_type: "user_report", capture_method: "manual" } }))
      .mockImplementationOnce(() => json(200, { status: "idempotent_replay", observation: { ...OBS, origin_type: "user_report", capture_method: "manual" } }));
    vi.stubGlobal("fetch", fetchMock);
    const input = { id: OBS.id, profile_id: "CM-03", indicator: "stress_vas" as const, value: 27.2, unit: "points_0_100", context: "stress_report", timestamp: OBS.measured_at, mission_day: 1 };
    expect((await httpApi.createObservation(input)).status).toBe(201);
    expect((await httpApi.createObservation(input)).status).toBe(200);
    const sent = JSON.parse((fetchMock.mock.calls[0] as [string, RequestInit])[1].body as string);
    expect(sent.measured_at).toBe(OBS.measured_at);
    expect(sent.origin_type).toBe("user_report");
  });

  it("normalises backend error fields (lists → text, measured_at → timestamp)", async () => {
    vi.stubGlobal("fetch", () =>
      json(422, { code: "DOMAIN_VALIDATION_ERROR", message: "x", fields: { value: ["Se requiere un número entero"], measured_at: "bad", existing_value: 4 }, request_id: "r1" }),
    );
    const err = await httpApi.createObservation({ id: OBS.id, profile_id: "CM-03", indicator: "samn_perelli", value: 3.5, unit: "points_1_7", context: "fatigue_report", timestamp: OBS.measured_at, mission_day: 1 }).catch((e) => e);
    expect(err).toBeInstanceOf(ApiError);
    expect(err.status).toBe(422);
    expect(Object.keys(err.body.fields).sort()).toEqual(["timestamp", "value"]);
    expect(err.body.request_id).toBe("r1");
  });

  it("treats network failures as unavailable", async () => {
    vi.stubGlobal("fetch", () => Promise.reject(new TypeError("Failed to fetch")));
    const err = await httpApi.listProfiles().catch((e) => e);
    expect(err).toBeInstanceOf(ApiError);
    expect(err.unavailable).toBe(true);
  });
});
