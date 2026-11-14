import { useAsync } from "../../app/useAsync";
import { Banner, Card, Skeleton } from "../../design-system/components";
import { api } from "../../services";
import { INDICATORS } from "../../services/domain";
import { IndicatorBadge } from "../../design-system/illustrations";

export function EducationPage() {
  const state = useAsync(() => Promise.all(INDICATORS.map((i) => api.getEducation(i.key))), []);

  return (
    <>
      <div className="page-head">
        <h1>Aprender</h1>
        <p className="meta">Qué mide cada indicador, cómo se registra y qué no puede decirte.</p>
      </div>
      {state.status === "error" && (
        <Banner tone="error" title="No se pudieron cargar las fichas">
          {state.error.message}
        </Banner>
      )}
      <div className="edu-grid">
        {state.data
          ? state.data.map((c) => (
              <Card key={c.indicator} as="article" className="stack" aria-labelledby={`edu-${c.indicator}`}>
                <div className="row" style={{ gap: "var(--space-4)", flexWrap: "nowrap" }}>
                  <IndicatorBadge indicator={c.indicator} />
                  <h2 id={`edu-${c.indicator}`}>{c.title}</h2>
                </div>
                <dl className="stack" style={{ gap: "var(--space-3)", margin: 0 }}>
                  <div>
                    <dt className="meta">Qué mide</dt>
                    <dd style={{ margin: 0 }}>{c.measures}</dd>
                  </div>
                  <div>
                    <dt className="meta">Cómo registrarlo</dt>
                    <dd style={{ margin: 0 }}>{c.how_to_record}</dd>
                  </div>
                  <div>
                    <dt className="meta">Escala</dt>
                    <dd style={{ margin: 0 }}>{c.scale}</dd>
                  </div>
                  <div>
                    <dt className="meta">Límites</dt>
                    <dd style={{ margin: 0 }}>
                      <ul style={{ margin: 0, paddingLeft: "1.2em" }}>
                        {c.limits.map((l) => (
                          <li key={l}>{l}</li>
                        ))}
                      </ul>
                    </dd>
                  </div>
                </dl>
                <p className="meta">
                  Referencia: {c.reference.url ? <a href={c.reference.url}>{c.reference.citation}</a> : c.reference.citation} ({c.reference.review_status})
                </p>
              </Card>
            ))
          : INDICATORS.map((i) => <Skeleton key={i.key} height={280} />)}
      </div>
    </>
  );
}
