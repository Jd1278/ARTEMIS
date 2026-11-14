import { Banner, OriginBadge } from "../../design-system/components";
import { ComparisonStrip } from "../../design-system/components/viz";
import { INDICATOR_BY_KEY } from "../../services/domain";
import { formatDate, formatDifference, formatNumber, formatValue } from "../../services/format";
import type { Comparison } from "../../services/types";

/** Explains the baseline comparison in plain language (RF-10, RF-11). No thresholds, no clinical wording. */
export function ComparisonPanel({ comparison, references }: { comparison: Comparison; references?: number[] }) {
  const ind = INDICATOR_BY_KEY[comparison.indicator];
  const { current } = comparison;

  if (!current) {
    return <Banner title="No valid value">{comparison.explanation}</Banner>;
  }

  if (!comparison.sufficient) {
    return (
      <Banner title={`Insufficient history (${comparison.days_used} of ${comparison.minimum_days} days)`} icon="…">
        {comparison.explanation} No comparison is calculated until there are at least {comparison.minimum_days} valid days from the same origin.
      </Banner>
    );
  }

  return (
    <div className="stack" style={{ gap: "var(--space-3)" }}>
      <p style={{ fontSize: "var(--text-lg)", fontWeight: 600 }}>{formatDifference(comparison.indicator, comparison.difference!)}</p>
      {references && references.length > 0 && (
        <figure style={{ margin: 0 }}>
          <ComparisonStrip
            references={references}
            baseline={comparison.baseline!}
            current={current.value as number}
            format={(v) => formatNumber(v)}
          />
          <figcaption className="meta">
            Each grey dot is a reference day; the vertical line is the median and the ring is the compared value.
          </figcaption>
        </figure>
      )}
      <dl className="cmp-grid">
        <div>
          <dt className="meta">Compared value</dt>
          <dd>
            {formatValue(comparison.indicator, current.value)} <span className="meta">(day {current.mission_day})</span>
          </dd>
        </div>
        <div>
          <dt className="meta">Personal median</dt>
          <dd>
            {formatNumber(comparison.baseline!)} {ind.unit_label}
          </dd>
        </div>
        <div>
          <dt className="meta">Days used</dt>
          <dd>
            {comparison.days_used} (minimum {comparison.minimum_days})
          </dd>
        </div>
        <div>
          <dt className="meta">Period</dt>
          <dd>
            {formatDate(comparison.period_from!)} – {formatDate(comparison.period_to!)}
          </dd>
        </div>
      </dl>
      <p className="meta">
        {comparison.explanation} It only compares with your own history from the same origin (<OriginBadge origin={comparison.origin_type} />). It is a description, not a health assessment. Rule{" "}
        <span className="mono">{comparison.rule_version}</span>.
      </p>
    </div>
  );
}
