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
        <h1>Learn</h1>
        <p className="meta">What each indicator measures, how it is logged and what it cannot tell you.</p>
      </div>
      {state.status === "error" && (
        <Banner tone="error" title="Could not load the cards">
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
                    <dt className="meta">What it measures</dt>
                    <dd style={{ margin: 0 }}>{c.measures}</dd>
                  </div>
                  <div>
                    <dt className="meta">How to log it</dt>
                    <dd style={{ margin: 0 }}>{c.how_to_record}</dd>
                  </div>
                  <div>
                    <dt className="meta">Scale</dt>
                    <dd style={{ margin: 0 }}>{c.scale}</dd>
                  </div>
                  <div>
                    <dt className="meta">Limits</dt>
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
                  Reference: {c.reference.url ? <a href={c.reference.url}>{c.reference.citation}</a> : c.reference.citation} ({c.reference.review_status})
                </p>
              </Card>
            ))
          : INDICATORS.map((i) => <Skeleton key={i.key} height={280} />)}
      </div>

      <Card as="section" className="stack ai-note" aria-labelledby="ai-use-title" style={{ marginTop: "var(--space-4)" }}>
        <h2 id="ai-use-title">How AI was used in this project</h2>
        <p>
          We used Claude (Anthropic) as a support tool. Every AI-assisted part was reviewed, run and tested by the team.
        </p>
        <ul style={{ margin: 0, paddingLeft: "1.2em" }}>
          <li>
            <strong>Data:</strong> helped research published sources and write the scripts that simulate, clean and validate the fictional crew dataset.
          </li>
          <li>
            <strong>Web interface:</strong> helped write the frontend code, the illustrations and the English text of this page.
          </li>
        </ul>
        <p className="meta">
          No AI model runs inside the app: comparisons use a fixed, transparent rule (median of your own previous days, rule baseline_v1), and the app does not
          diagnose or give medical advice.
        </p>
      </Card>
    </>
  );
}
