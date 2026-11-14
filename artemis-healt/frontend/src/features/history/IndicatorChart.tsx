import { Brush, CartesianGrid, Line, LineChart, ReferenceArea, ReferenceDot, ReferenceLine, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { INDICATOR_BY_KEY } from "../../services/domain";
import { formatNumber } from "../../services/format";
import type { IndicatorKey, Observation } from "../../services/types";

export interface ChartPoint {
  day: number;
  value: number | null;
  excluded: boolean;
  /** Present when the day was used for the comparison median. */
  reference?: boolean;
}

/** One point per mission day (last observation of the day). Null → gap, never zero or interpolation (RF-08). */
export function toDailyPoints(observations: Observation[], fromDay: number, toDay: number, referenceIds?: Set<string>): ChartPoint[] {
  const byDay = new Map<number, Observation>();
  for (const o of observations) if (o.mission_day !== null) byDay.set(o.mission_day, o);
  const points: ChartPoint[] = [];
  for (let d = fromDay; d <= toDay; d++) {
    const o = byDay.get(d);
    points.push({ day: d, value: o?.value ?? null, excluded: !!o && o.value === null, reference: !!o && !!referenceIds?.has(o.id) });
  }
  return points;
}

interface Props {
  indicator: IndicatorKey;
  points: ChartPoint[];
  baseline?: number | null;
  /** Mission-day span used to compute the median, shaded behind the line. */
  referenceRange?: [number, number] | null;
  /** Day emphasised with a ring (the compared value). */
  currentDay?: number | null;
  /** Day selected by the user (shows a vertical marker). */
  selectedDay?: number | null;
  onSelectDay?: (day: number) => void;
  brush?: boolean;
  dimmed?: boolean;
  height?: number;
  /** Accessible summary; the equivalent table is the full alternative. */
  summary: string;
}

function ChartTooltip({ active, payload, label, unit, labelText }: { active?: boolean; payload?: { payload: ChartPoint }[]; label?: number; unit: string; labelText: string }) {
  if (!active || !payload?.length) return null;
  const p = payload[0].payload;
  return (
    <div className="chart-tip">
      <strong>{p.excluded ? "Excluido" : p.value == null ? "Sin dato" : `${formatNumber(p.value)} ${unit}`}</strong>
      <span>
        {labelText} · día {label}
      </span>
      {p.excluded && <span>Imputado o fuera de dominio: no se usa.</span>}
      {p.reference && <span>Usado en la mediana</span>}
    </div>
  );
}

export function IndicatorChart({ indicator, points, baseline, referenceRange, currentDay, selectedDay, onSelectDay, brush, dimmed, height = 260, summary }: Props) {
  const ind = INDICATOR_BY_KEY[indicator];
  const domain: [number | "auto", number | "auto"] =
    indicator === "samn_perelli" ? [1, 7] : indicator === "stress_vas" ? [0, 100] : ["auto", "auto"];
  const current = currentDay != null ? points.find((p) => p.day === currentDay && p.value !== null) : undefined;

  return (
    <figure style={{ margin: 0, opacity: dimmed ? 0.55 : 1, transition: "opacity .2s" }}>
      <div role="img" aria-label={summary} style={{ width: "100%", height }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={points}
            margin={{ top: 12, right: 16, bottom: 4, left: 0 }}
            onClick={(state) => {
              const l = (state as { activeLabel?: number | string } | null)?.activeLabel;
              if (l != null && onSelectDay) onSelectDay(Number(l));
            }}
            style={{ cursor: onSelectDay ? "pointer" : undefined }}
          >
            <CartesianGrid stroke="var(--chart-grid)" strokeDasharray="3 3" vertical={false} />
            {referenceRange && (
              <ReferenceArea
                x1={referenceRange[0]}
                x2={referenceRange[1]}
                fill="var(--accent)"
                fillOpacity={0.08}
                stroke="var(--accent)"
                strokeOpacity={0.25}
                strokeDasharray="2 4"
                label={{ value: "días de referencia", position: "insideTopLeft", fill: "var(--muted)", fontSize: 11 }}
              />
            )}
            <XAxis dataKey="day" stroke="var(--muted)" tick={{ fill: "var(--muted)", fontSize: 12 }} tickLine={false} minTickGap={16} />
            <YAxis
              domain={domain}
              allowDecimals={!ind.integer_only}
              stroke="var(--muted)"
              tick={{ fill: "var(--muted)", fontSize: 12 }}
              width={44}
              tickFormatter={(v: number) => formatNumber(v)}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              cursor={{ stroke: "var(--muted)", strokeWidth: 1 }}
              content={(props) => (
                <ChartTooltip active={props.active} payload={props.payload as unknown as { payload: ChartPoint }[]} label={props.label as number} unit={ind.unit_label} labelText={ind.label} />
              )}
            />
            {baseline != null && (
              <ReferenceLine
                y={baseline}
                stroke="var(--chart-ref)"
                strokeDasharray="6 4"
                label={{ value: `mediana ${formatNumber(baseline)}`, fill: "var(--muted)", fontSize: 12, position: "insideBottomRight" }}
              />
            )}
            {selectedDay != null && <ReferenceLine x={selectedDay} stroke="var(--text)" strokeWidth={1.5} />}
            <Line
              type="linear"
              dataKey="value"
              stroke="var(--chart-line)"
              strokeWidth={2}
              dot={(p: { cx?: number; cy?: number; payload?: ChartPoint; index?: number }) =>
                p.cx == null || p.cy == null || p.payload?.value == null ? (
                  <g key={p.index} />
                ) : (
                  <circle
                    key={p.index}
                    cx={p.cx}
                    cy={p.cy}
                    r={p.payload.reference ? 3.5 : 2.5}
                    fill={p.payload.reference ? "var(--chart-line)" : "var(--surface)"}
                    stroke="var(--chart-line)"
                    strokeWidth={1.5}
                  />
                )
              }
              activeDot={{ r: 6, stroke: "var(--surface)", strokeWidth: 2, fill: "var(--chart-line)" }}
              connectNulls={false}
              isAnimationActive={false}
            />
            {current && current.value != null && (
              <ReferenceDot x={current.day} y={current.value} r={8} fill="none" stroke="var(--text)" strokeWidth={2} ifOverflow="visible" />
            )}
            {brush && points.length > 30 && (
              <Brush
                dataKey="day"
                height={28}
                stroke="var(--border-strong)"
                fill="var(--surface-sunken)"
                travellerWidth={10}
                startIndex={Math.max(0, points.length - 30)}
                tickFormatter={(d: number) => `día ${d}`}
              />
            )}
          </LineChart>
        </ResponsiveContainer>
      </div>
      <figcaption className="chart-legend meta">
        <span>
          <svg width="22" height="10" aria-hidden="true">
            <line x1="0" y1="5" x2="22" y2="5" stroke="var(--chart-line)" strokeWidth="2" />
          </svg>
          {ind.label}
        </span>
        {baseline != null && (
          <span>
            <svg width="22" height="10" aria-hidden="true">
              <line x1="0" y1="5" x2="22" y2="5" stroke="var(--chart-ref)" strokeWidth="1.5" strokeDasharray="5 3" />
            </svg>
            Mediana personal
          </span>
        )}
        {referenceRange && (
          <span>
            <svg width="14" height="10" aria-hidden="true">
              <rect width="14" height="10" fill="var(--accent)" fillOpacity="0.15" />
            </svg>
            Días de referencia (punto relleno = usado)
          </span>
        )}
        <span>Huecos = sin valor válido; no se rellenan.</span>
      </figcaption>
    </figure>
  );
}
