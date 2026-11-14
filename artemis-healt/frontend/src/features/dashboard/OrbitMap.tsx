import { memo, useMemo, useRef, useState, type KeyboardEvent, type PointerEvent } from "react";
import { INDICATORS, MISSION, missionDayToDate } from "../../services/domain";
import { formatDate, formatNumber, formatValue } from "../../services/format";
import type { IndicatorKey, Observation } from "../../services/types";
import "./orbit-map.css";

/*
 * Radial mission map: 180 days clockwise from the top, one concentric ring per indicator
 * (outer → inner: sleep, fatigue, stress, pulse). A satellite marks the cursor day.
 * Colour = magnitude within each ring (single hue, no clinical meaning).
 * Hover/focus never moves layout: the readout lives in the centre and in the side list.
 */

const STEPS = [26, 44, 62, 80, 100];
const stepColor = (i: number) => `color-mix(in oklch, var(--accent) ${STEPS[i]}%, var(--surface-sunken))`;

const C = 200; // centre
const OUTER = 186;
const RING_W = 25;
const RING_GAP = 4;
const GAP_DEG = 12; // opening at the top
const START = GAP_DEG / 2;
const PER_DAY = (360 - GAP_DEG) / MISSION.days;
const CELL_PAD = 0.18; // degrees of surface gap between cells

const rad = (deg: number) => (deg * Math.PI) / 180;
const polar = (r: number, deg: number) => [C + r * Math.sin(rad(deg)), C - r * Math.cos(rad(deg))] as const;
const ringRadii = (ring: number) => {
  const r1 = OUTER - ring * (RING_W + RING_GAP);
  return [r1 - RING_W, r1] as const;
};
const dayAngle = (day: number) => START + (day - 0.5) * PER_DAY;

function sector(r0: number, r1: number, a0: number, a1: number) {
  const [x0, y0] = polar(r1, a0);
  const [x1, y1] = polar(r1, a1);
  const [x2, y2] = polar(r0, a1);
  const [x3, y3] = polar(r0, a0);
  const large = a1 - a0 > 180 ? 1 : 0;
  return `M${x0.toFixed(2)},${y0.toFixed(2)}A${r1},${r1} 0 ${large} 1 ${x1.toFixed(2)},${y1.toFixed(2)}L${x2.toFixed(2)},${y2.toFixed(2)}A${r0},${r0} 0 ${large} 0 ${x3.toFixed(2)},${y3.toFixed(2)}Z`;
}

// Geometry never changes: compute the 720 cell paths once.
const CELL_PATHS: string[][] = INDICATORS.map((_, ring) => {
  const [r0, r1] = ringRadii(ring);
  return Array.from({ length: MISSION.days }, (_, i) => {
    const a0 = START + i * PER_DAY + CELL_PAD;
    return sector(r0, r1, a0, a0 + PER_DAY - CELL_PAD * 2);
  });
});

interface RowData {
  key: IndicatorKey;
  label: string;
  lo: number;
  hi: number;
  byDay: Map<number, Observation>;
  bins: (number | null | undefined)[]; // undefined → no record, null → excluded
}

const CellsLayer = memo(function CellsLayer({ rows, missionDay }: { rows: RowData[]; missionDay: number }) {
  return (
    <g>
      {rows.map((r, ring) =>
        CELL_PATHS[ring].map((d, i) => {
          const day = i + 1;
          if (day > missionDay) return <path key={day} d={d} className="orbit-map__future" />;
          const bin = r.bins[i];
          const fill = bin === undefined ? "var(--surface)" : bin === null ? "url(#om-hatch)" : stepColor(bin);
          return <path key={day} d={d} fill={fill} />;
        }),
      )}
    </g>
  );
});

interface Props {
  observations: Observation[];
  missionDay: number;
  selected: IndicatorKey;
  onPickDay: (day: number) => void;
  onPickIndicator: (key: IndicatorKey) => void;
}

export function OrbitMap({ observations, missionDay, selected, onPickDay, onPickIndicator }: Props) {
  const svgRef = useRef<SVGSVGElement>(null);
  const [hover, setHover] = useState<{ ring: number; day: number } | null>(null);
  const [focus, setFocus] = useState<{ ring: number; day: number }>({ ring: 0, day: missionDay });
  const [focused, setFocused] = useState(false);

  // Synthetic only and only up to the cursor: the scale never peeks into the future and origins never mix.
  const rows: RowData[] = useMemo(
    () =>
      INDICATORS.map((ind) => {
        const byDay = new Map<number, Observation>();
        for (const o of observations)
          if (o.indicator === ind.key && o.origin_type === "synthetic" && o.mission_day !== null && o.mission_day <= missionDay) byDay.set(o.mission_day, o);
        const vals = [...byDay.values()].map((o) => o.value).filter((v): v is number => v !== null);
        const lo = vals.length ? Math.min(...vals) : 0;
        const hi = vals.length ? Math.max(...vals) : 1;
        const bins = Array.from({ length: MISSION.days }, (_, i) => {
          const o = byDay.get(i + 1);
          if (!o) return undefined;
          if (o.value === null) return null;
          return hi === lo ? 2 : Math.min(4, Math.floor(((o.value - lo) / (hi - lo)) * 5));
        });
        return { key: ind.key, label: ind.label, lo, hi, byDay, bins };
      }),
    [observations, missionDay],
  );

  const active = hover ?? (focused ? focus : null);
  const readDay = active && active.day <= missionDay ? active.day : missionDay;

  const toCell = (e: PointerEvent<SVGSVGElement>) => {
    const svg = svgRef.current;
    const ctm = svg?.getScreenCTM();
    if (!svg || !ctm) return null;
    const p = new DOMPoint(e.clientX, e.clientY).matrixTransform(ctm.inverse());
    const dx = p.x - C;
    const dy = p.y - C;
    const r = Math.hypot(dx, dy);
    let deg = (Math.atan2(dx, -dy) * 180) / Math.PI;
    if (deg < 0) deg += 360;
    if (deg < START || deg > 360 - START) return null;
    const day = Math.min(MISSION.days, Math.floor((deg - START) / PER_DAY) + 1);
    const ring = INDICATORS.findIndex((_, i) => {
      const [r0, r1] = ringRadii(i);
      return r >= r0 - RING_GAP / 2 && r <= r1 + RING_GAP / 2;
    });
    return ring === -1 ? null : { ring, day };
  };

  const pick = (cell: { ring: number; day: number }) => {
    if (cell.day > missionDay) return;
    onPickIndicator(rows[cell.ring].key);
    onPickDay(cell.day);
  };

  const onKey = (e: KeyboardEvent) => {
    const step = e.shiftKey ? 7 : 1;
    let { ring, day } = focus;
    if (e.key === "ArrowRight") day = Math.min(missionDay, day + step);
    else if (e.key === "ArrowLeft") day = Math.max(1, day - step);
    else if (e.key === "ArrowUp") ring = Math.max(0, ring - 1);
    else if (e.key === "ArrowDown") ring = Math.min(rows.length - 1, ring + 1);
    else if (e.key === "Home") day = 1;
    else if (e.key === "End") day = missionDay;
    else if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      pick(focus);
      return;
    } else return;
    e.preventDefault();
    setFocus({ ring, day });
  };

  const valueText = (r: RowData, day: number) => {
    const o = r.byDay.get(day);
    if (!o) return "Sin registro";
    if (o.value === null) return "Excluido";
    return formatValue(r.key, o.value);
  };

  const activeRing = active ? rows[active.ring] : rows.find((r) => r.key === selected)!;
  const satAngle = dayAngle(missionDay);
  const [sx, sy] = polar(OUTER + 9, satAngle);
  const [lx0, ly0] = polar(ringRadii(rows.length - 1)[0] - 2, satAngle);
  const [lx1, ly1] = polar(OUTER + 2, satAngle);

  return (
    <div className="orbit-map">
      <div
        className="orbit-map__plot"
        tabIndex={0}
        role="group"
        aria-roledescription="mapa orbital"
        aria-label={`Mapa orbital de la misión: ${MISSION.days} días en sentido horario desde arriba; anillos de fuera hacia dentro: ${rows
          .map((r) => r.label)
          .join(", ")}. Flechas izquierda y derecha cambian de día (Mayús salta 7), arriba y abajo cambian de anillo, Intro va a ese día.`}
        onKeyDown={onKey}
        onFocus={() => {
          setFocused(true);
          setFocus((f) => ({ ...f, day: Math.min(f.day, missionDay) }));
        }}
        onBlur={() => setFocused(false)}
      >
        <svg
          ref={svgRef}
          viewBox="-6 -6 412 412"
          className="orbit-map__svg"
          onPointerMove={(e) => {
            const cell = toCell(e);
            setHover((h) => (h?.ring === cell?.ring && h?.day === cell?.day ? h : cell));
          }}
          onPointerLeave={() => setHover(null)}
          onClick={(e) => {
            const cell = toCell(e as unknown as PointerEvent<SVGSVGElement>);
            if (cell) {
              setFocus(cell);
              pick(cell);
            }
          }}
        >
          <defs>
            <pattern id="om-hatch" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
              <rect width="4" height="4" fill="var(--surface-sunken)" />
              <line x1="0" y1="0" x2="0" y2="4" stroke="var(--muted)" strokeWidth="1.5" />
            </pattern>
          </defs>

          {/* month-ish ticks every 30 days */}
          {[30, 60, 90, 120, 150, 180].map((d) => {
            const a = START + d * PER_DAY;
            const [x0, y0] = polar(OUTER + 2, a);
            const [x1, y1] = polar(OUTER + 6, a);
            return <line key={d} x1={x0} y1={y0} x2={x1} y2={y1} stroke="var(--border-strong)" strokeWidth={1} />;
          })}
          <text x={C} y={10} textAnchor="middle" className="orbit-map__start">
            día 1 →
          </text>

          <CellsLayer rows={rows} missionDay={missionDay} />

          {/* selected ring outline */}
          {(() => {
            const i = rows.findIndex((r) => r.key === selected);
            const [r0, r1] = ringRadii(i);
            return (
              <>
                <circle cx={C} cy={C} r={r1 + 1.5} className="orbit-map__sel" />
                <circle cx={C} cy={C} r={r0 - 1.5} className="orbit-map__sel" />
              </>
            );
          })()}

          {/* hover / focus: spoke across all rings + cell outline */}
          {active && (
            <g pointerEvents="none">
              {rows.map((_, i) => {
                const [r0, r1] = ringRadii(i);
                const a0 = START + (active.day - 1) * PER_DAY;
                return <path key={i} d={sector(r0 - 1, r1 + 1, a0 - 0.2, a0 + PER_DAY + 0.2)} className={i === active.ring ? "orbit-map__hot" : "orbit-map__spoke"} />;
              })}
            </g>
          )}

          {/* satellite = current mission day */}
          <line x1={lx0} y1={ly0} x2={lx1} y2={ly1} className="orbit-map__cursor" />
          <circle cx={sx} cy={sy} r={6} className="orbit-map__sat" />

          {/* centre readout */}
          <g className="orbit-map__center" pointerEvents="none">
            <text x={C} y={C - 26} textAnchor="middle" className="orbit-map__day">
              Día {readDay}
            </text>
            <text x={C} y={C - 8} textAnchor="middle" className="orbit-map__date">
              {formatDate(missionDayToDate(readDay))}
            </text>
            <text x={C} y={C + 18} textAnchor="middle" className="orbit-map__value">
              {valueText(activeRing, readDay)}
            </text>
            <text x={C} y={C + 36} textAnchor="middle" className="orbit-map__date">
              {activeRing.label}
            </text>
          </g>
        </svg>
      </div>

      <div className="orbit-map__side">
        <p className="meta">
          {active ? `Día ${readDay}` : `Día ${missionDay} (actual)`} · anillos de fuera hacia dentro
        </p>
        <ul className="orbit-map__list">
          {rows.map((r, i) => (
            <li key={r.key}>
              <button
                type="button"
                className={`orbit-map__row ${selected === r.key ? "is-selected" : ""} ${active?.ring === i ? "is-hot" : ""}`}
                aria-pressed={selected === r.key}
                onClick={() => onPickIndicator(r.key)}
              >
                <svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true">
                  {[0, 1, 2, 3].map((k) => (
                    <circle key={k} cx="11" cy="11" r={10 - k * 2.6} fill="none" stroke={k === i ? "var(--accent)" : "var(--border-strong)"} strokeWidth={k === i ? 2.4 : 1} />
                  ))}
                </svg>
                <span className="orbit-map__row-label">{r.label}</span>
                <span className="orbit-map__row-value">{valueText(r, readDay)}</span>
              </button>
            </li>
          ))}
        </ul>
        <div className="orbit-map__legend">
          <span className="meta">Bajo</span>
          {STEPS.map((_, i) => (
            <span key={i} className="orbit-map__swatch" style={{ background: stepColor(i) }} aria-hidden="true" />
          ))}
          <span className="meta">Alto</span>
          <span className="orbit-map__swatch orbit-map__swatch--hatch" aria-hidden="true" />
          <span className="meta">Excluido</span>
          <span className="orbit-map__swatch orbit-map__swatch--empty" aria-hidden="true" />
          <span className="meta">Sin registro</span>
        </div>
        <p className="meta">
          La intensidad solo indica magnitud relativa dentro de cada anillo, hasta el día {missionDay}; no significa mejor ni peor. Rangos:{" "}
          {rows.map((r, i) => (
            <span key={r.key}>
              {i > 0 && " · "}
              {r.label.toLowerCase()} {formatNumber(r.lo)}–{formatNumber(r.hi)}
            </span>
          ))}
          .
        </p>
      </div>
      <p className="visually-hidden" aria-live="polite">
        {focused ? `${rows[focus.ring].label}, día ${focus.day}: ${valueText(rows[focus.ring], focus.day)}` : ""}
      </p>
    </div>
  );
}
