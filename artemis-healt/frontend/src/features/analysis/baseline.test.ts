import { describe, expect, it } from "vitest";
import { compareBaseline, median } from "./baseline";
import type { Observation } from "../../services/types";

const day = (n: number) => {
  const d = new Date(Date.UTC(2026, 2, 1 + n - 1, 6, 0));
  return d.toISOString();
};
const obs = (n: number, value: number | null, extra: Partial<Observation> = {}): Observation => ({
  id: `id-${n}-${extra.origin_type ?? "s"}-${extra.timestamp ?? ""}`,
  profile_id: "CM-01",
  indicator: "stress_vas",
  value,
  source_value: value,
  unit: "points_0_100",
  timestamp: day(n),
  mission_day: n,
  context: "stress_report",
  namespace: "demo",
  origin_type: "synthetic",
  capture_method: "import",
  quality_flags: value === null ? ["stress_vas_imputed"] : ["ok"],
  source_file: null,
  source_row: null,
  ...extra,
});
const at = (n: number) => `${day(n).slice(0, 10)}T23:59:59Z`;
const run = (observations: Observation[], n: number) => compareBaseline({ observations, profileId: "CM-01", indicator: "stress_vas", at: at(n) });

describe("median", () => {
  it("handles odd and even lengths", () => {
    expect(median([3, 1, 2])).toBe(2);
    expect(median([4, 1, 3, 2])).toBe(2.5);
  });
});

describe("baseline_v1", () => {
  it("reports insufficient history with fewer than 7 valid previous days", () => {
    const rows = [1, 2, 3, 4, 5, 6, 7].map((n) => obs(n, 10 * n));
    const r = run(rows, 7);
    expect(r.sufficient).toBe(false);
    expect(r.days_used).toBe(6);
    expect(r.baseline).toBeNull();
  });

  it("excludes the current day and never uses future days", () => {
    const rows = [...Array.from({ length: 10 }, (_, i) => obs(i + 1, 50)), obs(11, 90), obs(12, 0)];
    const r = run(rows, 11);
    expect(r.current?.value).toBe(90);
    expect(r.baseline).toBe(50);
    expect(r.difference).toBe(40);
    expect(r.reference_observation_ids).not.toContain(rows[10].id);
    expect(r.reference_observation_ids).not.toContain(rows[11].id);
  });

  it("excludes null (imputed) values and requires 7 valid days", () => {
    const rows = [1, 2, 3, 4, 5, 6, 7, 8].map((n) => obs(n, n % 2 ? null : 20));
    const r = run([...rows, obs(9, 30)], 9);
    expect(r.days_used).toBe(4);
    expect(r.sufficient).toBe(false);
  });

  it("uses at most the 14 most recent valid days", () => {
    const rows = [...Array.from({ length: 20 }, (_, i) => obs(i + 1, i < 6 ? 0 : 100)), obs(21, 100)];
    const r = run(rows, 21);
    expect(r.days_used).toBe(14);
    expect(r.baseline).toBe(100); // the six zeros are older than the 14-day cap
  });

  it("ignores observations older than the 30-day window", () => {
    const rows = [...Array.from({ length: 10 }, (_, i) => obs(i + 1, 10)), obs(45, 10)];
    const r = run(rows, 45);
    expect(r.days_used).toBe(0);
    expect(r.sufficient).toBe(false);
  });

  it("uses the last valid observation of each day", () => {
    const rows: Observation[] = [];
    for (let n = 1; n <= 8; n++) {
      rows.push(obs(n, 0, { id: `a${n}` }));
      rows.push(obs(n, 60, { id: `b${n}`, timestamp: day(n).replace("06:00", "20:00") }));
    }
    const r = run([...rows, obs(9, 60, { id: "cur" })], 9);
    expect(r.baseline).toBe(60);
  });

  it("does not mix origins", () => {
    const synthetic = Array.from({ length: 10 }, (_, i) => obs(i + 1, 40));
    const manual = obs(11, 70, { id: "m", origin_type: "user_report", capture_method: "manual" });
    const r = run([...synthetic, manual], 11);
    expect(r.origin_type).toBe("user_report");
    expect(r.days_used).toBe(0);
    expect(r.sufficient).toBe(false);
  });
});
