import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { useMission } from "../../app/state";
import { useAsync } from "../../app/useAsync";
import { Banner, Card, EmptyState, Field, OriginBadge, QualityBadge, Segmented, Skeleton } from "../../design-system/components";
import { api } from "../../services";
import { INDICATOR_BY_KEY, INDICATORS, MISSION, missionDayToDate, ORIGIN_LABEL } from "../../services/domain";
import { formatDateTime, formatNumber } from "../../services/format";
import type { IndicatorKey, Observation, OriginType } from "../../services/types";
import { IndicatorChart, toDailyPoints } from "./IndicatorChart";

const isIndicator = (v: string | null): v is IndicatorKey => INDICATORS.some((i) => i.key === v);

export function HistoryPage() {
  const { profileId, missionDay, revision } = useMission();
  const [params, setParams] = useSearchParams();
  const indicator: IndicatorKey = isIndicator(params.get("indicator")) ? (params.get("indicator") as IndicatorKey) : "sleep_duration_h";
  const [origin, setOrigin] = useState<OriginType>("synthetic");
  const [fromDay, setFromDay] = useState(Math.max(1, missionDay - 29));
  const [toDay, setToDay] = useState(missionDay);
  // Follow the mission cursor: the window resets to the 30 days up to the selected day.
  useEffect(() => {
    setFromDay(Math.max(1, missionDay - 29));
    setToDay(missionDay);
  }, [missionDay]);
  const [view, setView] = useState<"chart" | "table">("chart");

  const lo = Math.max(1, Math.min(fromDay, toDay, missionDay));
  // Never show data after the mission cursor (requirements: calculations respect the cursor).
  const hi = Math.min(missionDay, MISSION.days, Math.max(fromDay, toDay));
  const ind = INDICATOR_BY_KEY[indicator];

  const state = useAsync(
    () => api.listObservations(profileId, { indicator, from: `${missionDayToDate(lo)}T00:00:00Z`, to: `${missionDayToDate(hi)}T23:59:59Z` }),
    [profileId, indicator, lo, hi, revision],
  );

  // One row per mission day (last observation of that day, same origin) — identical to the chart points (RF-08).
  const rows = useMemo(() => {
    const byDay = new Map<number, Observation>();
    for (const o of state.data ?? []) if (o.origin_type === origin && o.mission_day !== null) byDay.set(o.mission_day, o);
    return [...byDay.values()].sort((a, b) => a.timestamp.localeCompare(b.timestamp));
  }, [state.data, origin]);
  const points = useMemo(() => toDailyPoints(rows, lo, hi), [rows, lo, hi]);
  const excluded = rows.filter((r) => r.value === null).length;
  const hasManual = (state.data ?? []).some((o) => o.origin_type === "user_report");

  return (
    <>
      <div className="page-head">
        <h1>History</h1>
        <p className="meta">
          Profile {profileId}. Chronological order. Inclusive filters. One point per mission day (the last observation of the day).
        </p>
      </div>

      <Card className="stack" as="section" aria-label="Filters">
        <div className="filters">
          <Field label="Indicator">
            {(a) => (
              <select
                {...a}
                className="input"
                value={indicator}
                onChange={(e) => {
                  params.set("indicator", e.target.value);
                  setParams(params, { replace: true });
                }}
              >
                {INDICATORS.map((i) => (
                  <option key={i.key} value={i.key}>
                    {i.label}
                  </option>
                ))}
              </select>
            )}
          </Field>
          <Field label="Origin" hint="Origins are never mixed.">
            {(a) => (
              <select {...a} className="input" value={origin} onChange={(e) => setOrigin(e.target.value as OriginType)}>
                <option value="synthetic">{ORIGIN_LABEL.synthetic}</option>
                <option value="user_report">{ORIGIN_LABEL.user_report}</option>
              </select>
            )}
          </Field>
          <Field label="From day">
            {(a) => <input {...a} className="input" type="number" min={1} max={missionDay} value={fromDay} onChange={(e) => setFromDay(Number(e.target.value) || 1)} />}
          </Field>
          <Field label="To day">
            {(a) => <input {...a} className="input" type="number" min={1} max={missionDay} value={toDay} onChange={(e) => setToDay(Number(e.target.value) || 1)} />}
          </Field>
        </div>
        <div className="row" style={{ justifyContent: "space-between" }}>
          <p className="meta" aria-live="polite">
            {state.status === "loading" ? "Loading…" : `${rows.length} days with entries, ${excluded} with an excluded value, days ${lo}–${hi}.`}
          </p>
          <Segmented
            label="View"
            value={view}
            onChange={setView}
            options={[
              { value: "chart", label: "Chart" },
              { value: "table", label: "Table" },
            ]}
          />
        </div>
      </Card>

      <div style={{ marginTop: "var(--space-4)" }}>
        {state.status === "error" && (
          <Banner tone="error" title="Could not load the history">
            {state.error.message}
          </Banner>
        )}
        {state.status === "loading" && !state.data && <Skeleton height={300} />}
        {state.data &&
          (rows.length === 0 ? (
            <EmptyState title="No entries for these filters">
              {origin === "user_report" && !hasManual ? "There are no manual entries for this profile yet." : "Try another period or origin."}
            </EmptyState>
          ) : view === "chart" ? (
            <Card>
              <IndicatorChart
                indicator={indicator}
                points={points}
                height={340}
                brush
                dimmed={state.status === "loading"}
                summary={`${ind.label}, ${ORIGIN_LABEL[origin]}, days ${lo} to ${hi}: ${rows.length - excluded} valid values and ${excluded} excluded.`}
              />
            </Card>
          ) : (
            <div className="table-wrap">
              <table className="table">
                <caption>
                  {ind.label} ({ind.unit_label}) · {ORIGIN_LABEL[origin]} · days {lo}–{hi}
                </caption>
                <thead>
                  <tr>
                    <th scope="col">Day</th>
                    <th scope="col">Date and time</th>
                    <th scope="col">Value</th>
                    <th scope="col">Excluded original</th>
                    <th scope="col">Origin</th>
                    <th scope="col">Quality</th>
                    <th scope="col">Source</th>
                  </tr>
                </thead>
                <tbody>
                  {rows.map((o) => (
                    <tr key={o.id}>
                      <td className="num">{o.mission_day}</td>
                      <td>{formatDateTime(o.timestamp)}</td>
                      <td className="num">{o.value === null ? "—" : formatNumber(o.value)}</td>
                      <td className="num">{o.value === null && o.source_value !== null ? formatNumber(o.source_value) : ""}</td>
                      <td>
                        <OriginBadge origin={o.origin_type} method={o.capture_method} />
                      </td>
                      <td>
                        <QualityBadge flags={o.quality_flags} />
                      </td>
                      <td className="meta">{o.source_file ? `${o.source_file}${o.source_row ? `, row ${o.source_row}` : ""}` : "Manual entry"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ))}
      </div>
    </>
  );
}
