import { useEffect, useMemo, useState } from "react";

/*
 * Simplified Earth globe: coarse continent outlines (lon, lat) projected orthographically and
 * slowly rotating. Outlines are hand-simplified for illustration only (not cartographic data).
 */
type Ring = [number, number][];

const LAND: { ring: Ring; ice?: boolean }[] = [
  // North America
  { ring: [[-165, 62], [-160, 70], [-140, 70], [-125, 70], [-110, 68], [-95, 70], [-82, 67], [-78, 62], [-65, 60], [-56, 52], [-65, 46], [-70, 42], [-76, 37], [-81, 31], [-80, 25], [-83, 29], [-90, 30], [-97, 27], [-97, 21], [-92, 18], [-87, 21], [-88, 16], [-83, 10], [-79, 8], [-86, 12], [-93, 15], [-105, 20], [-110, 23], [-114, 30], [-118, 34], [-122, 37], [-124, 42], [-124, 48], [-130, 54], [-138, 59], [-150, 61], [-158, 57], [-165, 60]] },
  // Hudson Bay (cut out as water by drawing it on top later)
  // Greenland
  { ring: [[-72, 78], [-60, 82], [-32, 83], [-20, 78], [-20, 72], [-25, 68], [-40, 63], [-44, 60], [-50, 63], [-54, 68], [-58, 74], [-68, 76]], ice: true },
  // South America
  { ring: [[-80, 9], [-75, 11], [-70, 12], [-62, 10], [-52, 5], [-50, 0], [-44, -2], [-35, -6], [-38, -13], [-40, -22], [-48, -26], [-53, -34], [-58, -38], [-62, -40], [-65, -45], [-68, -50], [-69, -55], [-74, -52], [-75, -42], [-72, -30], [-71, -18], [-76, -14], [-81, -6], [-80, -1], [-78, 4]] },
  // Africa
  { ring: [[-17, 21], [-16, 14], [-14, 10], [-11, 6], [-6, 4.5], [1, 5.5], [8, 4.5], [9.5, 1], [12, -5], [13, -12], [12, -18], [15, -27], [18, -34], [22, -34.5], [27, -33.5], [32, -28], [35, -22], [40, -15], [40, -10], [39, -5], [43, 0], [48, 5], [51, 11], [44, 11.5], [39, 17], [35, 24], [33, 28], [32, 31], [25, 32], [20, 31], [15, 32.5], [10, 34], [10, 37], [3, 36.8], [-6, 35.8], [-10, 30], [-13, 27]] },
  // Madagascar
  { ring: [[44, -25], [47, -25], [50, -15.5], [49, -12], [44, -17]] },
  // Eurasia
  { ring: [[-9, 37], [-9, 43], [-2, 43.5], [-4.5, 48], [2, 51], [8, 54], [9, 57], [5, 60], [10, 63], [15, 68], [25, 71], [32, 70], [40, 67], [45, 68], [60, 70], [70, 73], [85, 75], [100, 77], [115, 74], [130, 72], [142, 72], [160, 70], [180, 68], [180, 62], [165, 60], [160, 55], [156, 51], [142, 54], [140, 46], [132, 43], [128, 38], [126, 35], [122, 31], [120, 25], [113, 22], [108, 21], [106, 11], [104, 8.5], [100, 6], [98, 9], [98, 16], [94, 18], [90, 22], [86, 20], [80, 15], [77, 8], [73, 17], [69, 22], [62, 25], [57, 25.5], [56, 22], [59, 22.5], [52, 16], [45, 13], [43, 13], [39, 21], [35, 28], [34.5, 31.5], [36, 36], [27, 37], [26, 40], [23, 38], [22, 40], [19.5, 41], [16, 41.5], [18, 40], [15.5, 38], [12, 41.5], [9, 44], [3, 43.3], [0, 40], [-1, 37.5], [-5, 36.2]] },
  // British Isles
  { ring: [[-5.5, 50], [1.5, 51], [0, 53.5], [-2, 56], [-5, 58.5], [-6.5, 56], [-4.5, 54], [-5, 52]] },
  // Japan
  { ring: [[130, 31], [134, 34], [140, 35.5], [141.5, 40], [141, 45], [139.5, 42], [137, 37], [132, 35]] },
  // Arabia is part of Eurasia; Indonesia (simplified)
  { ring: [[95, 5], [102, 1], [106, -6], [114, -8], [119, -8.5], [110, -7], [104, -5], [98, 2]] },
  { ring: [[109, 2], [117, 7], [119, 1], [116, -4], [110, -2]] },
  // Australia
  { ring: [[114, -22], [114, -34], [118, -35], [124, -33.5], [131, -31.5], [137, -34.5], [140, -38], [146, -39], [150, -37.5], [153, -30], [153, -25], [146, -19], [142, -11], [136, -12], [131, -11.5], [126, -14], [122, -18]] },
  // New Zealand
  { ring: [[172.5, -34.5], [178, -38], [175, -41.5], [171, -44], [167, -46], [170.5, -42]] },
  // Antarctica (edge)
  { ring: [[-180, -70], [-120, -73], [-60, -64], [0, -70], [60, -67], [120, -66], [180, -70], [180, -90], [-180, -90]], ice: true },
];

const HUDSON: Ring = [[-95, 59], [-90, 57], [-82, 55], [-78, 58], [-78, 62], [-85, 64], [-94, 63]];

const CLOUDS = [
  { lon: -40, lat: 45, rx: 0.32, ry: 0.07, rot: -12 },
  { lon: 20, lat: -5, rx: 0.25, ry: 0.06, rot: 8 },
  { lon: -120, lat: 10, rx: 0.3, ry: 0.06, rot: -5 },
  { lon: 100, lat: 35, rx: 0.28, ry: 0.07, rot: 10 },
  { lon: 160, lat: -30, rx: 0.3, ry: 0.06, rot: -8 },
  { lon: -10, lat: -45, rx: 0.35, ry: 0.06, rot: 4 },
  { lon: 60, lat: 55, rx: 0.3, ry: 0.06, rot: -6 },
];

const D = Math.PI / 180;

function project(lon: number, lat: number, lon0: number, lat0: number, r: number) {
  const l = (lon - lon0) * D;
  const p = lat * D;
  const p0 = lat0 * D;
  const cosc = Math.sin(p0) * Math.sin(p) + Math.cos(p0) * Math.cos(p) * Math.cos(l);
  let x = r * Math.cos(p) * Math.sin(l);
  let y = r * (Math.cos(p0) * Math.sin(p) - Math.sin(p0) * Math.cos(p) * Math.cos(l));
  if (cosc < 0) {
    // behind the globe: pin to the limb so filled shapes stay closed and are clipped by the disc
    const k = r / Math.max(1e-6, Math.hypot(x, y));
    x *= k;
    y *= k;
  }
  return { x, y: -y, visible: cosc >= 0, depth: cosc };
}

/** Densify long edges so projected outlines curve with the sphere. */
function densify(ring: Ring, step = 4): Ring {
  const out: Ring = [];
  for (let i = 0; i < ring.length; i++) {
    const [a1, b1] = ring[i];
    const [a2, b2] = ring[(i + 1) % ring.length];
    const n = Math.max(1, Math.ceil(Math.max(Math.abs(a2 - a1), Math.abs(b2 - b1)) / step));
    for (let k = 0; k < n; k++) out.push([a1 + ((a2 - a1) * k) / n, b1 + ((b2 - b1) * k) / n]);
  }
  return out;
}

const DENSE = LAND.map((l) => ({ ...l, ring: densify(l.ring) }));
const DENSE_HUDSON = densify(HUDSON);

function ringPath(ring: Ring, lon0: number, lat0: number, r: number) {
  let any = false;
  const pts = ring.map(([lon, lat]) => {
    const p = project(lon, lat, lon0, lat0, r);
    if (p.visible) any = true;
    return `${p.x.toFixed(1)},${p.y.toFixed(1)}`;
  });
  return any ? `M${pts.join("L")}Z` : "";
}

const reducedMotion = () => typeof window !== "undefined" && window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;

/** Rotating globe centred at (cx, cy). Spins ~8°/s; static with reduced motion. */
export function EarthGlobe({ cx, cy, r, lat0 = 18 }: { cx: number; cy: number; r: number; lat0?: number }) {
  const [lon0, setLon0] = useState(-40);

  useEffect(() => {
    if (reducedMotion()) return;
    let raf = 0;
    let last = performance.now();
    let acc = 0;
    const tick = (t: number) => {
      acc += t - last;
      last = t;
      if (acc > 50) {
        // ~20 fps is plenty for a slow spin
        setLon0((l) => (((l + acc * 0.008 + 180) % 360) + 360) % 360 - 180);
        acc = 0;
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, []);

  const land = useMemo(() => DENSE.map((l) => ({ d: ringPath(l.ring, lon0, lat0, r), ice: l.ice })), [lon0, lat0, r]);
  const hudson = useMemo(() => ringPath(DENSE_HUDSON, lon0, lat0, r), [lon0, lat0, r]);
  const clouds = useMemo(
    () =>
      CLOUDS.map((c) => ({ ...c, p: project(c.lon + 25, c.lat, lon0, lat0, r) })) // clouds drift slightly ahead of the ground
        .filter((c) => c.p.visible),
    [lon0, lat0, r],
  );
  const graticule = useMemo(() => {
    const lines: string[] = [];
    for (let lon = -180; lon < 180; lon += 30) {
      const ring: Ring = [];
      for (let lat = -80; lat <= 80; lat += 5) ring.push([lon, lat]);
      const pts = ring.map(([a, b]) => project(a, b, lon0, lat0, r)).filter((p) => p.visible);
      if (pts.length > 1) lines.push(`M${pts.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join("L")}`);
    }
    for (let lat = -60; lat <= 60; lat += 30) {
      const pts: { x: number; y: number }[] = [];
      for (let lon = -180; lon <= 180; lon += 5) {
        const p = project(lon, lat, lon0, lat0, r);
        if (p.visible) pts.push(p);
        else if (pts.length > 1) break;
      }
      if (pts.length > 1) lines.push(`M${pts.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join("L")}`);
    }
    return lines.join(" ");
  }, [lon0, lat0, r]);

  const id = "earth";
  return (
    <g transform={`translate(${cx} ${cy})`} className="earth">
      <defs>
        <radialGradient id={`${id}-atmo`} cx="50%" cy="50%" r="50%">
          <stop offset="0.8" stopColor="#7fb2ff" stopOpacity="0" />
          <stop offset="0.9" stopColor="#7fb2ff" stopOpacity="0.45" />
          <stop offset="1" stopColor="#7fb2ff" stopOpacity="0" />
        </radialGradient>
        <radialGradient id={`${id}-ocean`} cx="38%" cy="32%" r="78%">
          <stop offset="0" stopColor="#3f8fe0" />
          <stop offset="0.55" stopColor="#1c5aa8" />
          <stop offset="1" stopColor="#0b2a5c" />
        </radialGradient>
        {/* Land colour by screen latitude band (user space): tundra → temperate → desert → tropical → desert → temperate */}
        <linearGradient id={`${id}-land`} gradientUnits="userSpaceOnUse" x1="0" y1={-r} x2="0" y2={r}>
          <stop offset="0" stopColor="#a9b89c" />
          <stop offset="0.22" stopColor="#6fa35c" />
          <stop offset="0.38" stopColor="#7ea65a" />
          <stop offset="0.44" stopColor="#cdb27a" />
          <stop offset="0.52" stopColor="#c2a66c" />
          <stop offset="0.6" stopColor="#5d9a4a" />
          <stop offset="0.7" stopColor="#3f8a3f" />
          <stop offset="0.8" stopColor="#6ea25a" />
          <stop offset="0.86" stopColor="#c4ab72" />
          <stop offset="0.95" stopColor="#6ea25a" />
        </linearGradient>
        <radialGradient id={`${id}-shade`} cx="30%" cy="28%" r="85%">
          <stop offset="0.45" stopColor="#000" stopOpacity="0" />
          <stop offset="1" stopColor="#020a1c" stopOpacity="0.6" />
        </radialGradient>
        <radialGradient id={`${id}-shine`} cx="32%" cy="26%" r="35%">
          <stop offset="0" stopColor="#fff" stopOpacity="0.45" />
          <stop offset="1" stopColor="#fff" stopOpacity="0" />
        </radialGradient>
        <clipPath id={`${id}-clip`}>
          <circle r={r} />
        </clipPath>
        <filter id={`${id}-blur`} x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation={r * 0.02} />
        </filter>
      </defs>

      <circle r={r * 1.22} fill={`url(#${id}-atmo)`} />
      <circle r={r} fill={`url(#${id}-ocean)`} />
      <g clipPath={`url(#${id}-clip)`}>
        <path d={graticule} fill="none" stroke="#ffffff" strokeOpacity="0.08" strokeWidth="0.5" />
        {land.map((l, i) =>
          l.d ? <path key={i} d={l.d} fill={l.ice ? "#eef4f8" : `url(#${id}-land)`} stroke={l.ice ? "#d5e2ec" : "#3f7a3a"} strokeWidth="0.4" strokeLinejoin="round" /> : null,
        )}
        {hudson && <path d={hudson} fill="#1f5fae" />}
        <g filter={`url(#${id}-blur)`} opacity="0.6">
          {clouds.map((c, i) => (
            <ellipse
              key={i}
              cx={c.p.x}
              cy={c.p.y}
              rx={r * c.rx * 0.7 * (0.4 + 0.6 * c.p.depth)}
              ry={r * c.ry}
              transform={`rotate(${c.rot} ${c.p.x} ${c.p.y})`}
              fill="#ffffff"
              opacity={0.35 + 0.5 * c.p.depth}
            />
          ))}
        </g>
        <circle r={r} fill={`url(#${id}-shade)`} />
        <circle r={r} fill={`url(#${id}-shine)`} />
      </g>
      <circle r={r} fill="none" stroke="#bcd6ff" strokeOpacity="0.6" strokeWidth="0.8" />
    </g>
  );
}
