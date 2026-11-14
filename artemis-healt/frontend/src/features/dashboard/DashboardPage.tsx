import { memo, useDeferredValue, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useMission } from "../../app/state";
import { useAsync } from "../../app/useAsync";
import { Banner, Button, Card, EmptyState, OriginBadge, QualityBadge, Segmented, Skeleton } from "../../design-system/components";
import { Sparkline, useCountUp } from "../../design-system/components/viz";
import { api } from "../../services";
import { INDICATOR_BY_KEY, INDICATORS, MISSION, missionDayCursor, missionDayToDate, PROFILES } from "../../services/domain";
import { CrewAvatar, OrbitScene } from "../../design-system/illustrations";
import { INDICATOR_ICON } from "../../design-system/icons";
import { formatDate, formatDateTime, formatNumber, formatValue } from "../../services/format";
import type { Comparison, IndicatorKey, Observation } from "../../services/types";
import { ComparisonPanel } from "../analysis/ComparisonPanel";
import { IndicatorChart, toDailyPoints } from "../history/IndicatorChart";
import { OrbitMap } from "./OrbitMap";
import "./dashboard.css";

const STALE_AFTER_DAYS = 2;
const RANGES = [
  { value: "14", label: "14 d" },
  { value: "30", label: "30 d" },
  { value: "90", label: "90 d" },
  { value: "all", label: "Mission" },
] as const;
type Range = (typeof RANGES)[number]["value"];

function shortDiff(c: Comparison | undefined): string {
  if (!c) return "";
  if (!c.current) return "No valid value";
  if (!c.sufficient) return `Insufficient history (${c.days_used}/${c.minimum_days})`;
  const unit = INDICATOR_BY_KEY[c.indicator].difference_unit;
  const d = c.difference!;
  if (Math.abs(d) < 1e-9) return `= median (${formatNumber(c.baseline!)})`;
  return `${d > 0 ? "+" : "−"}${formatNumber(Math.abs(d))} ${unit} vs. median`;
}

interface CardProps {
  indicator: IndicatorKey;
  rows: Observation[];
  comparison?: Comparison;
  missionDay: number;
  selected: boolean;
  onSelect: () => void;
}

function IndicatorCard({ indicator, rows, comparison, missionDay, selected, onSelect }: CardProps) {
  const ind = INDICATOR_BY_KEY[indicator];
  const own = rows.filter((o) => o.indicator === indicator);
  const latest = own.at(-1) ?? null;
  const shown = [...own].reverse().find((o) => o.value !== null) ?? null;
  const latestExcluded = latest && latest.value === null ? latest : null;
  const age = shown?.mission_day != null ? missionDay - shown.mission_day : null;
  const animated = useCountUp(shown?.value ?? null);
  const Icon = INDICATOR_ICON[indicator];

  const origin = comparison?.origin_type ?? "synthetic";
  const byDay = new Map<number, number | null>();
  for (const o of own) if (o.origin_type === origin && o.mission_day !== null) byDay.set(o.mission_day, o.value);
  const spark: (number | null)[] = [];
  for (let d = Math.max(1, missionDay - 13); d <= missionDay; d++) spark.push(byDay.has(d) ? byDay.get(d)! : null);

  return (
    <button type="button" className={`card card--interactive ind-card ${selected ? "card--selected" : ""}`} aria-pressed={selected} onClick={onSelect}>
      <span className="ind-card__top">
        <span className="ind-card__label">
          <Icon size={20} className="icon-accent" />
          {ind.label}
        </span>
        <span className="ind-card__unit meta">{ind.unit_label}</span>
      </span>
      {shown ? (
        <>
          <span className="ind-card__main">
            <span className="ind-card__value" aria-label={formatValue(indicator, shown.value)}>
              {animated === null ? "—" : formatNumber(ind.integer_only ? Math.round(animated) : Math.round(animated * 100) / 100)}
            </span>
            <Sparkline values={spark} baseline={comparison?.sufficient ? comparison.baseline : null} />
          </span>
          <span className="ind-card__diff">{shortDiff(comparison)}</span>
          <span className="meta">
            Day {shown.mission_day} · {formatDateTime(shown.timestamp)}
          </span>
          <span className="row">
            <OriginBadge origin={shown.origin_type} method={shown.capture_method} />
            <QualityBadge flags={shown.quality_flags} />
          </span>
          {age !== null && age >= STALE_AFTER_DAYS && (
            <span className="ind-card__note">
              <span aria-hidden="true">⏱</span> Stale data: {age} days ago
            </span>
          )}
        </>
      ) : (
        <span className="meta">No valid values up to this day.</span>
      )}
      {latestExcluded && (
        <span className="ind-card__note">
          <span aria-hidden="true">⊘</span> Day {latestExcluded.mission_day}: value excluded
          {latestExcluded.source_value !== null ? ` (original ${formatValue(indicator, latestExcluded.source_value)}, not used)` : ""}
        </span>
      )}
    </button>
  );
}

function DayDetail({ indicator, day, rows, onMove, onClose }: { indicator: IndicatorKey; day: number; rows: Observation[]; onMove: (d: number) => void; onClose: () => void }) {
  const items = rows.filter((o) => o.indicator === indicator && o.mission_day === day);
  return (
    <div className="day-detail" aria-live="polite">
      <div className="row" style={{ justifyContent: "space-between" }}>
        <h3>Day {day}</h3>
        <div className="row">
          <Button aria-label="Previous day in the chart" onClick={() => onMove(day - 1)}>
            ‹
          </Button>
          <Button aria-label="Next day in the chart" onClick={() => onMove(day + 1)}>
            ›
          </Button>
          <Button variant="ghost" onClick={onClose}>
            Close
          </Button>
        </div>
      </div>
      {items.length === 0 ? (
        <p className="meta">No entry on this day.</p>
      ) : (
        items.map((o) => (
          <dl key={o.id} className="cmp-grid">
            <div>
              <dt className="meta">Value</dt>
              <dd>{o.value === null ? `Excluded (original ${o.source_value === null ? "—" : formatNumber(o.source_value)})` : formatValue(indicator, o.value)}</dd>
            </div>
            <div>
              <dt className="meta">Time</dt>
              <dd>{formatDateTime(o.timestamp)}</dd>
            </div>
            <div>
              <dt className="meta">Origin and quality</dt>
              <dd className="row">
                <OriginBadge origin={o.origin_type} method={o.capture_method} />
                <QualityBadge flags={o.quality_flags} />
              </dd>
            </div>
            <div>
              <dt className="meta">Provenance</dt>
              <dd className="mono" style={{ fontSize: "var(--text-meta)" }}>
                {o.source_file ? `${o.source_file}${o.source_row ? ` · row ${o.source_row}` : ""}` : "Manual entry"}
              </dd>
            </div>
          </dl>
        ))
      )}
    </div>
  );
}

/**
 * The mission cursor can advance up to ~22 days/s while playing. The heavy body renders from a
 * deferred copy of the day, so React can skip intermediate days instead of slowing the player.
 */
export function DashboardPage() {
  const { profileId, missionDay, setMissionDay, revision } = useMission();
  const day = useDeferredValue(missionDay);
  return <DashboardBody profileId={profileId} missionDay={day} at={missionDayCursor(day)} revision={revision} setMissionDay={setMissionDay} />;
}

interface BodyProps {
  profileId: string;
  missionDay: number;
  at: string;
  revision: number;
  setMissionDay: (d: number) => void;
}

const DashboardBody = memo(function DashboardBody({ profileId, missionDay, at, revision, setMissionDay }: BodyProps) {
  const [selected, setSelected] = useState<IndicatorKey>("sleep_duration_h");
  const [range, setRange] = useState<Range>("30");
  const [pickedDay, setPickedDay] = useState<number | null>(null);

  const history = useAsync(() => api.listObservations(profileId, { to: at }), [profileId, at, revision]);
  const comparisons = useAsync(() => Promise.all(INDICATORS.map((i) => api.getComparison(profileId, i.key, at))), [profileId, at, revision]);

  const rows = history.data ?? [];
  const cmp = comparisons.data?.find((c) => c.indicator === selected);
  const ind = INDICATOR_BY_KEY[selected];
  const unavailable = [history, comparisons].find((s) => s.status === "error");
  const profile = PROFILES.find((p) => p.id === profileId);

  const span = range === "all" ? missionDay : Number(range);
  const fromDay = Math.max(1, missionDay - span + 1);
  const origin = cmp?.origin_type ?? "synthetic";
  const refIds = useMemo(() => new Set(cmp?.reference_observation_ids ?? []), [cmp]);
  const selectedRows = useMemo(() => rows.filter((o) => o.indicator === selected && o.origin_type === origin), [rows, selected, origin]);
  const points = useMemo(() => toDailyPoints(selectedRows, fromDay, missionDay, refIds), [selectedRows, fromDay, missionDay, refIds]);
  const references = useMemo(() => selectedRows.filter((o) => refIds.has(o.id)).map((o) => o.value as number), [selectedRows, refIds]);
  const refDays = selectedRows.filter((o) => refIds.has(o.id)).map((o) => o.mission_day as number);
  const referenceRange: [number, number] | null = cmp?.sufficient && refDays.length ? [Math.max(fromDay, Math.min(...refDays)), Math.max(...refDays)] : null;
  const valid = points.filter((p) => p.value !== null).length;

  return (
    <>
      <section className="hero" aria-labelledby="hero-title">
        <div>
          <p className="hero__eyebrow">{MISSION.name} · Simulated mission</p>
          <h1 className="hero__title" id="hero-title">
            Day {missionDay} <span>of {MISSION.days}</span>
          </h1>
          <p className="meta">
            {formatDate(missionDayToDate(missionDay))} · simulated historical date. Press <strong>Play</strong> to run through the mission or tap the orbital map to jump to another day.
          </p>
          <div className="hero__progress" aria-hidden="true">
            <span style={{ width: `${(missionDay / MISSION.days) * 100}%` }} />
          </div>
          {profile && (
            <div className="hero__crew">
              <CrewAvatar id={profile.id} size={52} />
              <div>
                <strong>{profile.id}</strong>
                <p className="meta">{profile.role} · fictional crew member</p>
              </div>
            </div>
          )}
        </div>
        <OrbitScene progress={missionDay / MISSION.days} label={`Illustration: the spacecraft has covered ${Math.round((missionDay / MISSION.days) * 100)}% of the mission orbit.`} />
      </section>

      {unavailable?.status === "error" && (
        <div style={{ marginBottom: "var(--space-4)" }}>
          <Banner tone="error" title={unavailable.error.unavailable ? "Service unavailable" : "Could not load the data"}>
            {unavailable.error.message} No new data is shown until the connection is restored.
            {unavailable.error.body.request_id && <span className="mono"> · ref {unavailable.error.body.request_id}</span>}
          </Banner>
        </div>
      )}

      <section aria-label="Indicadores" className="ind-grid">
        {history.data
          ? INDICATORS.map((i) => (
              <IndicatorCard
                key={i.key}
                indicator={i.key}
                rows={rows}
                comparison={comparisons.data?.find((c) => c.indicator === i.key)}
                missionDay={missionDay}
                selected={selected === i.key}
                onSelect={() => {
                  setSelected(i.key);
                  setPickedDay(null);
                }}
              />
            ))
          : INDICATORS.map((i) => <Skeleton key={i.key} label={`Loading ${i.label}`} height={190} />)}
      </section>

      <div className="detail-grid">
        <Card>
          <div className="row" style={{ justifyContent: "space-between", marginBottom: "var(--space-3)" }}>
            <h2>{ind.label}</h2>
            <Segmented label="Chart period" value={range} onChange={setRange} options={RANGES.map((r) => ({ value: r.value, label: r.label }))} />
          </div>
          {history.data ? (
            valid === 0 ? (
              <EmptyState title="No valid values in this period" />
            ) : (
              <IndicatorChart
                indicator={selected}
                points={points}
                baseline={cmp?.sufficient ? cmp.baseline : null}
                referenceRange={referenceRange}
                currentDay={cmp?.current?.mission_day ?? null}
                selectedDay={pickedDay}
                onSelectDay={setPickedDay}
                brush={range === "all"}
                dimmed={history.status === "loading"}
                height={range === "all" ? 320 : 280}
                summary={`${ind.label} from day ${fromDay} to ${missionDay}: ${valid} days with a valid value and ${points.length - valid} without.`}
              />
            )
          ) : (
            <Skeleton height={280} label="Loading chart" />
          )}
          {pickedDay !== null ? (
            <DayDetail indicator={selected} day={pickedDay} rows={rows} onMove={(d) => setPickedDay(Math.min(missionDay, Math.max(1, d)))} onClose={() => setPickedDay(null)} />
          ) : (
            <p className="meta" style={{ marginTop: "var(--space-2)" }}>
              Click a point to see its provenance. <Link to={`/history?indicator=${selected}`}>View full table</Link>
            </p>
          )}
        </Card>
        <Card>
          <h2 style={{ marginBottom: "var(--space-3)" }}>Comparison with your history</h2>
          <div aria-live="polite">
            {cmp ? <ComparisonPanel comparison={cmp} references={references} /> : <Skeleton height={160} label="Calculating comparison" />}
          </div>
        </Card>
      </div>

      <Card className="stack" style={{ marginTop: "var(--space-4)" }}>
        <div>
          <h2>Mission map</h2>
          <p className="meta">The whole mission in one orbit: each sector is a day, each ring an indicator, and the satellite marks the current day. Hover to read the values; click to jump to that day.</p>
        </div>
        {history.data ? (
          <OrbitMap
            observations={rows}
            missionDay={missionDay}
            selected={selected}
            onPickIndicator={(k) => {
              setSelected(k);
            }}
            onPickDay={(d) => {
              setPickedDay(null);
              setMissionDay(d);
            }}
          />
        ) : (
          <Skeleton height={360} label="Loading map" />
        )}
      </Card>
    </>
  );
});
