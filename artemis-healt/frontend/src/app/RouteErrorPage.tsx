import { isRouteErrorResponse, useRouteError } from "react-router-dom";

/** Recover outside the damaged view; never swallow DOM exceptions or patch Node prototypes. */
export function RouteErrorPage() {
  const error = useRouteError();
  const notFound = isRouteErrorResponse(error) && error.status === 404;
  return (
    <main className="page" style={{ maxWidth: 640, margin: "64px auto", padding: 24 }}>
      <section className="card stack" role="alert" aria-labelledby="route-error-title" style={{ padding: 32, gap: 20 }}>
        <p className="brand__name">ARTEMIS HEALTH</p>
        <h1 id="route-error-title">{notFound ? "Page not found" : "This view could not be updated"}</h1>
        <p>{notFound ? "Return to the overview to continue." : "Reload this view to restore it. If browser translation or an extension changed the page, keep automatic translation off for this app."}</p>
        <p className="meta">No observation is saved by reloading. An unsaved draft may be lost.</p>
        <div className="row" style={{ flexWrap: "wrap" }}>
          <button type="button" className="btn btn--primary" onClick={() => window.location.reload()}>Reload view</button>
          <a className="btn" href="/">Back to overview</a>
        </div>
      </section>
    </main>
  );
}
