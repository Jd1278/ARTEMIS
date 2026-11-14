import { useEffect, useMemo, useRef } from "react";
import type { IndicatorKey } from "../services/types";
import { INDICATOR_ICON } from "./icons";
import { EarthGlobe } from "./Earth";

/** Deterministic PRNG so the starfield and patches are identical on every render. */
function rng(seed: number) {
  let s = seed >>> 0;
  return () => {
    s = (s * 1664525 + 1013904223) >>> 0;
    return s / 4294967296;
  };
}

const reducedMotion = () => typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;

/** Fixed, decorative space backdrop: nebula glow + two star layers with slow parallax. */
export function SpaceBackground() {
  const near = useRef<HTMLDivElement>(null);
  const far = useRef<HTMLDivElement>(null);

  const layers = useMemo(() => {
    const make = (seed: number, n: number, maxR: number) => {
      const r = rng(seed);
      return Array.from({ length: n }, () => ({ x: r() * 100, y: r() * 100, r: 0.3 + r() * maxR, o: 0.35 + r() * 0.6, tw: r() < 0.18, d: r() * 6 }));
    };
    return { far: make(7, 140, 0.7), near: make(42, 55, 1.2) };
  }, []);

  useEffect(() => {
    if (reducedMotion()) return;
    let raf = 0;
    const onScroll = () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const y = window.scrollY;
        if (far.current) far.current.style.transform = `translate3d(0, ${-y * 0.03}px, 0)`;
        if (near.current) near.current.style.transform = `translate3d(0, ${-y * 0.08}px, 0)`;
      });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => {
      window.removeEventListener("scroll", onScroll);
      cancelAnimationFrame(raf);
    };
  }, []);

  const stars = (list: typeof layers.far) => (
    <svg width="100%" height="100%" preserveAspectRatio="none" viewBox="0 0 100 100">
      {list.map((s, i) => (
        <circle
          key={i}
          cx={s.x}
          cy={s.y}
          r={s.r * 0.12}
          fill="var(--star)"
          opacity={s.o}
          className={s.tw ? "twinkle" : undefined}
          style={s.tw ? { animationDelay: `${s.d}s` } : undefined}
          vectorEffect="non-scaling-stroke"
        />
      ))}
    </svg>
  );

  return (
    <div className="space-bg" aria-hidden="true">
      <div className="space-bg__nebula" />
      <div className="space-bg__layer" ref={far}>
        {stars(layers.far)}
      </div>
      <div className="space-bg__layer" ref={near}>
        {stars(layers.near)}
      </div>
    </div>
  );
}

// Crew identity hues (identity only; never used for data or state).
const CREW_HUES = ["#1f5fd1", "#7a5af8", "#0b8a85", "#c25412", "#b4387a", "#2f86b8"];

/** Generated mission-patch avatar for a fictional crew member. Original artwork. */
export function CrewAvatar({ id, size = 40 }: { id: string; size?: number }) {
  const n = Math.max(1, Number(id.replace(/\D/g, "")) || 1);
  const hue = CREW_HUES[(n - 1) % CREW_HUES.length];
  const r = rng(n * 97);
  const stars = Array.from({ length: 3 + (n % 3) }, () => ({ a: r() * Math.PI * 2, d: 11 + r() * 5 }));
  const tilt = -35 + n * 22;
  const gid = `patch-${id}`;
  return (
    <svg width={size} height={size} viewBox="0 0 48 48" aria-hidden="true" focusable="false" className="crew-avatar">
      <defs>
        <radialGradient id={gid} cx="35%" cy="30%" r="80%">
          <stop offset="0" stopColor="#ffffff" />
          <stop offset="1" stopColor={hue} stopOpacity="0.22" />
        </radialGradient>
      </defs>
      <circle cx="24" cy="24" r="22.5" fill={`url(#${gid})`} stroke={hue} strokeWidth="1.5" />
      <circle cx="24" cy="24" r="19" fill="none" stroke={hue} strokeOpacity="0.35" strokeDasharray="1.5 2.5" />
      {stars.map((s, i) => (
        <circle key={i} cx={24 + Math.cos(s.a) * s.d} cy={24 + Math.sin(s.a) * s.d} r={0.9} fill={hue} />
      ))}
      <ellipse cx="24" cy="24" rx="15" ry="5" transform={`rotate(${tilt} 24 24)`} fill="none" stroke="#0e1a2b" strokeOpacity="0.55" strokeWidth="1" />
      <circle cx="24" cy="24" r="6.5" fill={hue} />
      <circle cx={24 + 15 * Math.cos((tilt * Math.PI) / 180)} cy={24 + 15 * Math.sin((tilt * Math.PI) / 180)} r="2" fill="#0e1a2b" />
      <text x="24" y="44" textAnchor="middle" fontSize="7" fontWeight="800" fill="#0e1a2b" letterSpacing="0.5">
        {String(n).padStart(2, "0")}
      </text>
    </svg>
  );
}

/**
 * Mission scene: Earth, the orbit, the traveled arc and a generic spacecraft placed by mission progress.
 * Generic shapes only (not a replica of any real vehicle).
 */
export function OrbitScene({ progress, label }: { progress: number; label: string }) {
  const cx = 200;
  const cy = 130;
  const rx = 170;
  const ry = 62;
  const tilt = -10;
  const angle = -Math.PI / 2 + progress * Math.PI * 2;
  const t = (tilt * Math.PI) / 180;
  const px = Math.cos(angle) * rx;
  const py = Math.sin(angle) * ry;
  const sx = cx + px * Math.cos(t) - py * Math.sin(t);
  const sy = cy + px * Math.sin(t) + py * Math.cos(t);
  // traveled arc as a polyline sampled along the ellipse
  const steps = Math.max(2, Math.round(progress * 120));
  const trail = Array.from({ length: steps + 1 }, (_, i) => {
    const a = -Math.PI / 2 + (i / 120) * Math.PI * 2;
    const x = Math.cos(a) * rx;
    const y = Math.sin(a) * ry;
    return `${(cx + x * Math.cos(t) - y * Math.sin(t)).toFixed(1)},${(cy + x * Math.sin(t) + y * Math.cos(t)).toFixed(1)}`;
  }).join(" ");
  const behind = Math.sin(angle) < 0; // upper half of the ellipse passes behind the planet

  const ship = (
    <g transform={`translate(${sx.toFixed(1)} ${sy.toFixed(1)}) rotate(${((angle * 180) / Math.PI + 90 + tilt).toFixed(1)})`} className="orbit-scene__ship">
      <circle r="14" fill="var(--accent)" opacity="0.12" />
      <rect x="-13" y="-3" width="8" height="6" rx="1" fill="#5b8def" stroke="#0e1a2b" strokeWidth="0.6" />
      <rect x="5" y="-3" width="8" height="6" rx="1" fill="#5b8def" stroke="#0e1a2b" strokeWidth="0.6" />
      <rect x="-5" y="-0.6" width="10" height="1.2" fill="#0e1a2b" />
      <rect x="-3" y="-5" width="6" height="10" rx="2.5" fill="#ffffff" stroke="#0e1a2b" strokeWidth="0.8" />
      <circle cy="-1.5" r="1.2" fill="#0d1a2c" />
    </g>
  );

  return (
    <svg viewBox="0 0 400 260" className="orbit-scene" role="img" aria-label={label}>
      <defs>
        <radialGradient id="moon-g" cx="35%" cy="35%" r="70%">
          <stop offset="0" stopColor="#e9eef5" />
          <stop offset="1" stopColor="#7d8ba0" />
        </radialGradient>
      </defs>

      <circle cx="350" cy="40" r="13" fill="url(#moon-g)" stroke="#b3c0d3" />
      <circle cx="346" cy="37" r="2.5" fill="#9aa6b8" opacity="0.6" />

      {/* back half of the orbit */}
      <ellipse cx={cx} cy={cy} rx={rx} ry={ry} transform={`rotate(${tilt} ${cx} ${cy})`} fill="none" stroke="var(--border-strong)" strokeDasharray="3 5" />
      {behind && ship}

      <EarthGlobe cx={cx} cy={cy} r={58} />

      <polyline points={trail} fill="none" stroke="var(--accent)" strokeWidth="2.5" strokeLinecap="round" opacity="0.9" />
      {!behind && ship}
    </svg>
  );
}

/** Decorative badge for each indicator (education cards). */
export function IndicatorBadge({ indicator, size = 72 }: { indicator: IndicatorKey; size?: number }) {
  const Icon = INDICATOR_ICON[indicator];
  return (
    <div className="ind-badge" style={{ width: size, height: size }} aria-hidden="true">
      <svg viewBox="0 0 72 72" width={size} height={size} className="ind-badge__rings">
        <circle cx="36" cy="36" r="34" fill="none" stroke="var(--accent)" strokeOpacity="0.2" />
        <circle cx="36" cy="36" r="27" fill="var(--accent-soft)" stroke="var(--accent)" strokeOpacity="0.45" />
        <ellipse cx="36" cy="36" rx="35" ry="11" transform="rotate(-28 36 36)" fill="none" stroke="var(--secondary)" strokeOpacity="0.5" strokeDasharray="2 3" />
        <circle cx="66" cy="21" r="2.5" fill="var(--secondary)" />
      </svg>
      <span className="ind-badge__icon">
        <Icon size={size * 0.42} />
      </span>
    </div>
  );
}

/** Small satellite for empty states. */
export function EmptyIllustration() {
  return (
    <svg width="96" height="72" viewBox="0 0 96 72" aria-hidden="true" className="empty-illu">
      <ellipse cx="48" cy="40" rx="42" ry="12" fill="none" stroke="var(--border-strong)" strokeDasharray="3 4" />
      <g transform="translate(48 34) rotate(-18)">
        <rect x="-26" y="-5" width="16" height="10" rx="1.5" fill="#5b8def" />
        <rect x="10" y="-5" width="16" height="10" rx="1.5" fill="#5b8def" />
        <rect x="-10" y="-1" width="20" height="2" fill="#0e1a2b" />
        <rect x="-6" y="-9" width="12" height="18" rx="4" fill="#ffffff" stroke="#0e1a2b" />
        <circle cy="-2" r="2.2" fill="#0d1a2c" />
      </g>
      <circle cx="12" cy="12" r="1.2" fill="var(--accent)" />
      <circle cx="84" cy="18" r="1" fill="var(--secondary)" />
      <circle cx="74" cy="62" r="1.3" fill="var(--accent)" />
    </svg>
  );
}
