import { useEffect, useState, type CSSProperties } from "react";
import { useMission } from "../app/state";
import { MISSION, missionDayToDate } from "../services/domain";
import { formatDate } from "../services/format";
import { IconChevron, IconPause, IconPlay } from "../design-system/icons";

// Milliseconds per mission day: 1× = 2 días por segundo; de 0.25× a 2× en pasos de 0.25.
const BASE_MS = 500;
const SPEEDS = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2].map((k) => ({ id: String(k), label: `${k}×`, ms: Math.round(BASE_MS / k) }));

/** Orbit ring showing mission progress. Decorative; the label next to it carries the numbers. */
function OrbitRing({ day }: { day: number }) {
  const r = 22;
  const c = 2 * Math.PI * r;
  const k = day / MISSION.days;
  const angle = k * 2 * Math.PI - Math.PI / 2;
  return (
    <svg width={56} height={56} viewBox="0 0 56 56" aria-hidden="true" className="orbit">
      <circle cx={28} cy={28} r={r} fill="none" stroke="var(--border)" strokeWidth={4} />
      <circle
        cx={28}
        cy={28}
        r={r}
        fill="none"
        stroke="var(--accent)"
        strokeWidth={4}
        strokeLinecap="round"
        strokeDasharray={`${c * k} ${c}`}
        transform="rotate(-90 28 28)"
        className="orbit__arc"
      />
      <circle cx={28} cy={28} r={7} fill="var(--surface-raised)" stroke="var(--muted)" strokeWidth={1.5} />
      <circle cx={28 + r * Math.cos(angle)} cy={28 + r * Math.sin(angle)} r={4.5} fill="var(--text)" stroke="var(--bg)" strokeWidth={2} />
    </svg>
  );
}

export function MissionTimeline() {
  const { missionDay, setMissionDay } = useMission();
  const [playing, setPlaying] = useState(false);
  const [speed, setSpeed] = useState("1");

  // Fixed cadence: an interval keeps the chosen speed regardless of how long the page takes to render.
  useEffect(() => {
    if (!playing) return;
    const ms = SPEEDS.find((s) => s.id === speed)!.ms;
    const id = setInterval(() => setMissionDay((d) => d + 1), ms);
    return () => clearInterval(id);
  }, [playing, speed, setMissionDay]);

  useEffect(() => {
    if (playing && missionDay >= MISSION.days) setPlaying(false);
  }, [playing, missionDay]);

  const toggle = () => {
    if (!playing && missionDay >= MISSION.days) setMissionDay(1);
    setPlaying((p) => !p);
  };

  return (
    <div className="timeline">
      <div className="timeline__head">
        <OrbitRing day={missionDay} />
        <div>
          <label className="field__label" htmlFor="day-range">
            Mission day <span className="timeline__day mono">{missionDay}</span>
            <span className="meta"> / {MISSION.days}</span>
          </label>
          <p className="meta">Simulated historical date: {formatDate(missionDayToDate(missionDay))}</p>
        </div>
        <div className="timeline__buttons">
          <button type="button" className="btn" aria-label="Previous day" onClick={() => setMissionDay(missionDay - 1)} disabled={missionDay <= 1}>
            <IconChevron dir="left" size={20} />
          </button>
          <button type="button" className="btn btn--primary timeline__play" onClick={toggle} aria-pressed={playing}>
            {playing ? <IconPause size={18} /> : <IconPlay size={18} />}
            <span className="timeline__play-label">{playing ? "Pause" : "Play"}</span>
          </button>
          <button type="button" className="btn" aria-label="Next day" onClick={() => setMissionDay(missionDay + 1)} disabled={missionDay >= MISSION.days}>
            <IconChevron size={20} />
          </button>
          <label className="timeline__speed">
            <span className="visually-hidden">Playback speed</span>
            <span aria-hidden="true" className="meta">Speed</span>
            <select className="input" value={speed} onChange={(e) => setSpeed(e.target.value)}>
              {SPEEDS.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.label}
                </option>
              ))}
            </select>
          </label>
        </div>
      </div>
      <div className="timeline__track">
        <input
          id="day-range"
          className="range"
          type="range"
          min={1}
          max={MISSION.days}
          value={missionDay}
          onChange={(e) => {
            setPlaying(false);
            setMissionDay(Number(e.target.value));
          }}
          aria-valuetext={`Day ${missionDay} of ${MISSION.days}, ${formatDate(missionDayToDate(missionDay))}`}
          style={{ "--progress": `${((missionDay - 1) / (MISSION.days - 1)) * 100}%` } as CSSProperties}
        />
        <div className="timeline__ticks" aria-hidden="true">
          {[1, 30, 60, 90, 120, 150, 180].map((d) => (
            <span key={d} style={{ left: `${((d - 1) / (MISSION.days - 1)) * 100}%` }}>
              {d}
            </span>
          ))}
        </div>
      </div>
      <span className="visually-hidden" aria-live="polite">
        {playing ? "" : `Day ${missionDay}`}
      </span>
    </div>
  );
}
