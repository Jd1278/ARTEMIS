import { useMemo, useState } from "react";
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
  const indicator: IndicatorKey = isIndicator(params.get("indicador")) ? (params.get("indicador") as IndicatorKey) : "sleep_duration_h";
  const [origin, setOrigin] = useState<OriginType>("synthetic");
  const [fromDay, setFromDay] = useState(Math.max(1, missionDay - 29));
  const [toDay, setToDay] = useState(missionDay);
  const [view, setView] = useState<"chart" | "table">("chart");

  const lo = Math.max(1, Math.min(fromDay, toDay));
  const hi = Math.min(MISSION.days, Math.max(fromDay, toDay));
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
        <h1>Historial</h1>
        <p className="meta">
          Perfil {profileId}. Orden temporal. Filtros inclusivos. Un punto por día de misión (la última observación del día).
        </p>
      </div>

      <Card className="stack" as="section" aria-label="Filtros">
        <div className="filters">
          <Field label="Indicador">
            {(a) => (
              <select
                {...a}
                className="input"
                value={indicator}
                onChange={(e) => {
                  params.set("indicador", e.target.value);
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
          <Field label="Origen" hint="Los orígenes no se mezclan.">
            {(a) => (
              <select {...a} className="input" value={origin} onChange={(e) => setOrigin(e.target.value as OriginType)}>
                <option value="synthetic">{ORIGIN_LABEL.synthetic}</option>
                <option value="user_report">{ORIGIN_LABEL.user_report}</option>
              </select>
            )}
          </Field>
          <Field label="Desde el día">
            {(a) => <input {...a} className="input" type="number" min={1} max={MISSION.days} value={fromDay} onChange={(e) => setFromDay(Number(e.target.value) || 1)} />}
          </Field>
          <Field label="Hasta el día">
            {(a) => <input {...a} className="input" type="number" min={1} max={MISSION.days} value={toDay} onChange={(e) => setToDay(Number(e.target.value) || 1)} />}
          </Field>
        </div>
        <div className="row" style={{ justifyContent: "space-between" }}>
          <p className="meta" aria-live="polite">
            {state.status === "loading" ? "Cargando…" : `${rows.length} días con registro, ${excluded} con valor excluido, días ${lo}–${hi}.`}
          </p>
          <Segmented
            label="Vista"
            value={view}
            onChange={setView}
            options={[
              { value: "chart", label: "Gráfica" },
              { value: "table", label: "Tabla" },
            ]}
          />
        </div>
      </Card>

      <div style={{ marginTop: "var(--space-4)" }}>
        {state.status === "error" && (
          <Banner tone="error" title="No se pudo cargar el historial">
            {state.error.message}
          </Banner>
        )}
        {state.status === "loading" && !state.data && <Skeleton height={300} />}
        {state.data &&
          (rows.length === 0 ? (
            <EmptyState title="Sin registros para estos filtros">
              {origin === "user_report" && !hasManual ? "Aún no hay registros manuales para este perfil." : "Prueba con otro periodo u origen."}
            </EmptyState>
          ) : view === "chart" ? (
            <Card>
              <IndicatorChart
                indicator={indicator}
                points={points}
                height={340}
                brush
                dimmed={state.status === "loading"}
                summary={`${ind.label}, ${ORIGIN_LABEL[origin]}, días ${lo} a ${hi}: ${rows.length - excluded} valores válidos y ${excluded} excluidos.`}
              />
            </Card>
          ) : (
            <div className="table-wrap">
              <table className="table">
                <caption>
                  {ind.label} ({ind.unit_label}) · {ORIGIN_LABEL[origin]} · días {lo}–{hi}
                </caption>
                <thead>
                  <tr>
                    <th scope="col">Día</th>
                    <th scope="col">Fecha y hora</th>
                    <th scope="col">Valor</th>
                    <th scope="col">Original excluido</th>
                    <th scope="col">Origen</th>
                    <th scope="col">Calidad</th>
                    <th scope="col">Fuente</th>
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
                      <td className="meta">{o.source_file ? `${o.source_file}, fila ${o.source_row}` : "Captura manual"}</td>
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
