import { useEffect, useRef, useState } from "react";

const reducedMotion = () => typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;

/** Animates a number towards `value` (ease-out). Returns the value immediately with reduced motion. */
export function useCountUp(value: number | null, duration = 450): number | null {
  const [shown, setShown] = useState(value);
  const from = useRef(value);
  useEffect(() => {
    if (value === null || from.current === null || reducedMotion()) {
      from.current = value;
      setShown(value);
      return;
    }
    const start = performance.now();
    const a = from.current;
    let raf = 0;
    const tick = (t: number) => {
      const k = Math.min(1, (t - start) / duration);
      const e = 1 - (1 - k) ** 3;
      setShown(a + (value - a) * e);
      if (k < 1) raf = requestAnimationFrame(tick);
      else from.current = value;
    };
    raf = requestAnimationFrame(tick);
    return () => {
      cancelAnimationFrame(raf);
      from.current = value;
    };
  }, [value, duration]);
  return shown;
}

interface SparklineProps {
  values: (number | null)[];
  baseline?: number | null;
  width?: number;
  height?: number;
  domain?: [number, number];
}

/** Tiny line with gaps for null days. Decorative: the card text carries the values. */
export function Sparkline({ values, baseline, width = 140, height = 36, domain }: SparklineProps) {
  const valid = values.filter((v): v is number => v !== null);
  if (valid.length < 2) return <svg width={width} height={height} aria-hidden="true" />;
  const lo = domain ? domain[0] : Math.min(...valid, baseline ?? Infinity);
  const hi = domain ? domain[1] : Math.max(...valid, baseline ?? -Infinity);
  const pad = 4;
  const x = (i: number) => pad + (i * (width - pad * 2)) / Math.max(1, values.length - 1);
  const y = (v: number) => (hi === lo ? height / 2 : height - pad - ((v - lo) / (hi - lo)) * (height - pad * 2));

  const segments: string[] = [];
  let current = "";
  values.forEach((v, i) => {
    if (v === null) {
      if (current) segments.push(current);
      current = "";
      return;
    }
    current += `${current ? "L" : "M"}${x(i).toFixed(1)},${y(v).toFixed(1)}`;
  });
  if (current) segments.push(current);
  const lastIndex = values.length - 1 - [...values].reverse().findIndex((v) => v !== null);

  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} aria-hidden="true" className="sparkline">
      {baseline != null && <line x1={pad} x2={width - pad} y1={y(baseline)} y2={y(baseline)} stroke="var(--chart-ref)" strokeDasharray="3 3" strokeWidth={1} />}
      {segments.map((d, i) => (
        <path key={i} d={d} fill="none" stroke="var(--chart-line)" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
      ))}
      {segments.length === 0 || values.length === 0 ? null : (
        <circle cx={x(lastIndex)} cy={y(values[lastIndex] as number)} r={3.5} fill="var(--chart-line)" stroke="var(--surface)" strokeWidth={2} />
      )}
    </svg>
  );
}

interface StripProps {
  references: number[];
  baseline: number;
  current: number;
  format: (v: number) => string;
  domain?: [number, number];
}

/**
 * Dot strip: each reference day is a dot, the median a vertical tick and the compared value a ring.
 * Shows spread without implying good/bad. Text alternative is provided by the caller.
 */
export function ComparisonStrip({ references, baseline, current, format, domain }: StripProps) {
  const all = [...references, baseline, current];
  let lo = domain ? domain[0] : Math.min(...all);
  let hi = domain ? domain[1] : Math.max(...all);
  if (hi === lo) {
    lo -= 1;
    hi += 1;
  }
  const W = 320;
  const H = 64;
  const pad = 16;
  const x = (v: number) => pad + ((v - lo) / (hi - lo)) * (W - pad * 2);
  // Stack duplicate values vertically so every reference day stays visible.
  const seen = new Map<string, number>();
  const dots = references.map((v) => {
    const key = x(v).toFixed(0);
    const n = seen.get(key) ?? 0;
    seen.set(key, n + 1);
    return { cx: x(v), cy: 30 - n * 7 };
  });
  return (
    <svg viewBox={`0 0 ${W} ${H}`} width="100%" style={{ maxWidth: 480, display: "block" }} aria-hidden="true">
      <line x1={pad} x2={W - pad} y1={36} y2={36} stroke="var(--border-strong)" strokeWidth={1} />
      {dots.map((d, i) => (
        <circle key={i} cx={d.cx} cy={d.cy} r={4} fill="var(--chart-ref)" opacity={0.75} />
      ))}
      <line x1={x(baseline)} x2={x(baseline)} y1={8} y2={44} stroke="var(--text)" strokeWidth={2} />
      <text x={x(baseline)} y={58} textAnchor="middle" fontSize={11} fill="var(--muted)">
        median {format(baseline)}
      </text>
      <circle cx={x(current)} cy={30} r={7} fill="none" stroke="var(--accent)" strokeWidth={3} />
      <text x={pad} y={58} fontSize={11} fill="var(--muted)" textAnchor="start" opacity={x(baseline) - pad > 70 ? 1 : 0}>
        {format(lo)}
      </text>
      <text x={W - pad} y={58} fontSize={11} fill="var(--muted)" textAnchor="end" opacity={W - pad - x(baseline) > 70 ? 1 : 0}>
        {format(hi)}
      </text>
    </svg>
  );
}
