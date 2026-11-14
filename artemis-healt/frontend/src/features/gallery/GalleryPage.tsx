import { useState } from "react";
import { Banner, Button, Card, EmptyState, Field, OriginBadge, QualityBadge, Segmented, SimBadge, Skeleton } from "../../design-system/components";
import { api } from "../../services";
import type { Comparison, Observation } from "../../services/types";
import { ComparisonPanel } from "../analysis/ComparisonPanel";
import { IndicatorChart } from "../history/IndicatorChart";

// Fixed data so I4/I6 can approve screenshots (docs/design.md).
const OBS: Observation = {
  id: "00000000-0000-4000-8000-000000000001",
  profile_id: "CM-01",
  indicator: "sleep_duration_h",
  value: 6.4,
  source_value: 6.4,
  unit: "h",
  timestamp: "2026-04-29T06:30:00Z",
  mission_day: 60,
  context: "sleep_report",
  namespace: "demo",
  origin_type: "synthetic",
  capture_method: "import",
  quality_flags: ["ok"],
  source_file: "crew_daily_log_clean.csv",
  source_row: 361,
};
const CMP_OK: Comparison = {
  profile_id: "CM-01",
  indicator: "sleep_duration_h",
  rule_version: "baseline_v1",
  at: "2026-04-29T23:59:59Z",
  origin_type: "synthetic",
  current: OBS,
  baseline: 7.1,
  difference: -0.7,
  days_used: 14,
  minimum_days: 7,
  period_from: "2026-04-15T06:30:00Z",
  period_to: "2026-04-28T06:30:00Z",
  sufficient: true,
  reference_observation_ids: [],
  explanation: "Median of 14 previous valid days (up to 14, 30-day window, excluding the current day and excluded values).",
};
const CMP_LOW: Comparison = {
  ...CMP_OK,
  baseline: null,
  difference: null,
  days_used: 3,
  sufficient: false,
  explanation: "Insufficient history: 3 of 7 valid days required in the previous 30 days.",
};
const POINTS = Array.from({ length: 20 }, (_, i) => ({
  day: 41 + i,
  value: [4, 9, 15].includes(i) ? null : 6.5 + Math.sin(i / 2),
  excluded: [4, 9].includes(i),
}));

export function GalleryPage() {
  const [seg, setSeg] = useState<"a" | "b">("a");
  const [outage, setOutage] = useState(() => !!window.__ARTEMIS_SIMULATE_OUTAGE__);

  return (
    <>
      <div className="page-head">
        <h1>Component gallery</h1>
        <p className="meta">Internal page with fixed data for visual and accessibility review.</p>
      </div>
      <div className="stack">
        <Card className="stack">
          <h2>State tests</h2>
          <label className="row">
            <input
              type="checkbox"
              checked={outage}
              disabled={api.mode !== "mock"}
              onChange={(e) => {
                window.__ARTEMIS_SIMULATE_OUTAGE__ = e.target.checked;
                setOutage(e.target.checked);
              }}
              style={{ width: 20, height: 20 }}
            />
            Simulate a server outage (local demo mode only)
          </label>
        </Card>

        <Card className="stack">
          <h2>Buttons and controls</h2>
          <div className="row">
            <Button variant="primary">Primary</Button>
            <Button>Secondary</Button>
            <Button variant="ghost">Link</Button>
            <Button disabled>Disabled</Button>
          </div>
          <Segmented label="Example" value={seg} onChange={setSeg} options={[{ value: "a", label: "Chart" }, { value: "b", label: "Table" }]} />
          <Field label="Field with error" hint="Scale 1–7, whole number." error="Must be a whole number.">
            {(a) => <input {...a} className="input" defaultValue="3.5" />}
          </Field>
        </Card>

        <Card className="stack">
          <h2>Badges</h2>
          <div className="row">
            <SimBadge />
            <OriginBadge origin="synthetic" method="import" />
            <OriginBadge origin="user_report" method="manual" />
            <QualityBadge flags={["ok"]} />
            <QualityBadge flags={["stress_vas_imputed"]} />
            <QualityBadge flags={["samn_perelli_out_of_range"]} />
          </div>
        </Card>

        <Card className="stack">
          <h2>Messages and states</h2>
          <Banner title="Information">Neutral informational message.</Banner>
          <Banner tone="error" title="NOT SAVED">
            The database is unavailable. Your draft is kept for this session.
          </Banner>
          <EmptyState title="No entries for these filters">Try another period.</EmptyState>
          <Skeleton height={80} />
        </Card>

        <Card className="stack">
          <h2>Comparison</h2>
          <ComparisonPanel comparison={CMP_OK} />
          <ComparisonPanel comparison={CMP_LOW} />
        </Card>

        <Card>
          <h2>Chart with gaps</h2>
          <IndicatorChart indicator="sleep_duration_h" points={POINTS} baseline={7.1} summary="Example chart with three days without a value." />
        </Card>
      </div>
    </>
  );
}
