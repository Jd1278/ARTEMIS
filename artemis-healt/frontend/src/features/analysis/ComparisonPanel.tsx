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
    return <Banner title="Sin valor válido">{comparison.explanation}</Banner>;
  }

  if (!comparison.sufficient) {
    return (
      <Banner title={`Historial insuficiente (${comparison.days_used} de ${comparison.minimum_days} días)`} icon="…">
        {comparison.explanation} No se calcula ninguna comparación hasta reunir al menos {comparison.minimum_days} días válidos del mismo origen.
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
            Cada punto gris es un día de referencia; la línea vertical es la mediana y el anillo es el valor comparado.
          </figcaption>
        </figure>
      )}
      <dl className="cmp-grid">
        <div>
          <dt className="meta">Valor comparado</dt>
          <dd>
            {formatValue(comparison.indicator, current.value)} <span className="meta">(día {current.mission_day})</span>
          </dd>
        </div>
        <div>
          <dt className="meta">Mediana personal</dt>
          <dd>
            {formatNumber(comparison.baseline!)} {ind.unit_label}
          </dd>
        </div>
        <div>
          <dt className="meta">Días usados</dt>
          <dd>
            {comparison.days_used} (mínimo {comparison.minimum_days})
          </dd>
        </div>
        <div>
          <dt className="meta">Periodo</dt>
          <dd>
            {formatDate(comparison.period_from!)} – {formatDate(comparison.period_to!)}
          </dd>
        </div>
      </dl>
      <p className="meta">
        {comparison.explanation} Solo compara con tu propio historial del mismo origen (<OriginBadge origin={comparison.origin_type} />). Es una descripción, no una valoración de salud. Regla{" "}
        <span className="mono">{comparison.rule_version}</span>.
      </p>
    </div>
  );
}
