import { useEffect, useMemo, useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { useMission } from "../../app/state";
import { Banner, Button, Card, Field } from "../../design-system/components";
import { api, ApiError } from "../../services";
import { dateToMissionDay, INDICATOR_BY_KEY, INDICATORS, MISSION, missionDayToDate, PROFILES, SCALE_HELP, validateValue } from "../../services/domain";
import { formatDateTime, formatValue } from "../../services/format";
import type { IndicatorKey, Observation } from "../../services/types";
import { ScaleInput } from "./ScaleInput";
import { INDICATOR_ICON } from "../../design-system/icons";

const DRAFT_KEY = "artemis.draft";

interface Draft {
  id: string;
  profile_id: string;
  indicator: IndicatorKey;
  value: string;
  /** "YYYY-MM-DDTHH:mm", interpreted as UTC. */
  time: string;
}

type SaveState =
  | { kind: "idle" }
  | { kind: "saving" }
  | { kind: "saved"; status: 201 | 200; observation: Observation }
  | { kind: "failed"; error: ApiError };

function loadDraft(): Draft | null {
  try {
    const raw = sessionStorage.getItem(DRAFT_KEY);
    return raw ? (JSON.parse(raw) as Draft) : null;
  } catch {
    return null;
  }
}
function storeDraft(d: Draft | null) {
  try {
    if (d) sessionStorage.setItem(DRAFT_KEY, JSON.stringify(d));
    else sessionStorage.removeItem(DRAFT_KEY);
  } catch {
    /* session storage unavailable: draft stays in memory */
  }
}

function newDraft(profileId: string, missionDay: number, indicator: IndicatorKey = "sleep_duration_h"): Draft {
  return { id: crypto.randomUUID(), profile_id: profileId, indicator, value: "", time: `${missionDayToDate(missionDay)}T08:00` };
}

function validate(d: Draft): Record<string, string> {
  const errors: Record<string, string> = {};
  const ind = INDICATOR_BY_KEY[d.indicator];
  if (d.value.trim() === "") errors.value = "Enter a value.";
  else {
    const err = validateValue(ind, Number(d.value.replace(",", ".")));
    if (err) errors.value = err;
  }
  const t = Date.parse(`${d.time}:00Z`);
  if (!d.time || Number.isNaN(t)) errors.timestamp = "Enter a valid date and time.";
  else {
    const day = dateToMissionDay(d.time);
    if (day < 1 || day > MISSION.days) errors.timestamp = `The date must be within the mission (days 1 to ${MISSION.days}).`;
  }
  return errors;
}

export function RecordPage() {
  const { profileId, missionDay, bumpRevision } = useMission();
  const [draft, setDraft] = useState<Draft>(() => loadDraft() ?? newDraft(profileId, missionDay));
  const [touched, setTouched] = useState(false);
  const [save, setSave] = useState<SaveState>({ kind: "idle" });
  const [serverErrors, setServerErrors] = useState<Record<string, string>>({});

  useEffect(() => storeDraft(draft), [draft]);

  const ind = INDICATOR_BY_KEY[draft.indicator];
  const localErrors = useMemo(() => validate(draft), [draft]);
  const errors = touched ? { ...serverErrors, ...localErrors } : serverErrors;

  const update = (patch: Partial<Draft>) => {
    setDraft((d) => ({ ...d, ...patch }));
    setServerErrors({});
    if (save.kind === "saved") setSave({ kind: "idle" });
  };

  async function submit(e: FormEvent) {
    e.preventDefault();
    setTouched(true);
    if (Object.keys(localErrors).length) return;
    setSave({ kind: "saving" });
    try {
      const result = await api.createObservation({
        id: draft.id, // same UUID on every retry → idempotent
        profile_id: draft.profile_id,
        indicator: draft.indicator,
        value: Number(draft.value.replace(",", ".")),
        unit: ind.unit,
        context: ind.context,
        timestamp: new Date(`${draft.time}:00Z`).toISOString(),
        mission_day: dateToMissionDay(draft.time),
      });
      setSave({ kind: "saved", status: result.status, observation: result.observation });
      bumpRevision();
      // Saved: start a fresh draft (new UUID) for the next capture, keeping profile/indicator/time.
      setDraft((d) => ({ ...d, id: crypto.randomUUID(), value: "" }));
      setTouched(false);
    } catch (err) {
      const error = err instanceof ApiError ? err : new ApiError(0, { code: "unknown", message: String(err), fields: {}, request_id: "" });
      setServerErrors(error.body.fields ?? {});
      setSave({ kind: "failed", error });
    }
  }

  return (
    <>
      <div className="page-head">
        <h1>Log an observation</h1>
        <p className="meta">Manual self-reported entry. It is only saved once the server confirms it.</p>
      </div>

      <div className="detail-grid">
        <Card>
          <form className="stack" onSubmit={submit} noValidate>
            <Field label="Profile" hint="Fictional demo profiles only.">
              {(a) => (
                <select {...a} className="input" value={draft.profile_id} onChange={(e) => update({ profile_id: e.target.value })}>
                  {PROFILES.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.id} · {p.role}
                    </option>
                  ))}
                </select>
              )}
            </Field>

            <fieldset className="ind-picker">
              <legend className="field__label">Indicator</legend>
              {INDICATORS.map((i) => (
                <label key={i.key} className={`ind-picker__item ${draft.indicator === i.key ? "is-checked" : ""}`}>
                  <input type="radio" name="indicator" value={i.key} checked={draft.indicator === i.key} aria-label={`${i.label}, ${i.unit_label}`} onChange={() => {
                      update({ indicator: i.key, value: "" });
                      setTouched(false);
                    }} />
                  <span className="ind-picker__icon" aria-hidden="true">
                    {(() => {
                      const Icon = INDICATOR_ICON[i.key];
                      return <Icon size={24} />;
                    })()}
                  </span>
                  <span>
                    <span className="ind-picker__label">{i.label}</span>
                    <span className="meta">{i.unit_label}</span>
                  </span>
                </label>
              ))}
            </fieldset>

            <Field label={`Value (${ind.unit_label})`} hint={SCALE_HELP[draft.indicator]} error={errors.value}>
              {(a) => <ScaleInput indicator={draft.indicator} value={draft.value} onChange={(v) => update({ value: v })} inputProps={a} onBlur={() => setTouched(true)} />}
            </Field>

            <Field label="Date and time (UTC)" hint="Historical date of the simulated mission. Defaults to the selected day." error={errors.timestamp}>
              {(a) => (
                <input {...a} className="input" type="datetime-local" value={draft.time} onChange={(e) => update({ time: e.target.value })} onBlur={() => setTouched(true)} />
              )}
            </Field>

            {(errors.unit || errors.context || errors.profile_id || errors.id) && (
              <Banner tone="error" title="The server rejected some fields">
                {[errors.unit, errors.context, errors.profile_id, errors.id].filter(Boolean).join(" ")}
              </Banner>
            )}

            <div className="row">
              <Button type="submit" variant="primary" disabled={save.kind === "saving"}>
                {save.kind === "saving" ? "Saving…" : save.kind === "failed" ? "Retry" : "Save"}
              </Button>
              <Button
                variant="ghost"
                onClick={() => {
                  setDraft(newDraft(profileId, missionDay, draft.indicator));
                  setTouched(false);
                  setServerErrors({});
                  setSave({ kind: "idle" });
                }}
              >
                Discard draft
              </Button>
            </div>
            <p className="meta">
              Draft ID: <span className="mono">{draft.id}</span>. It is reused on every retry to avoid duplicates.
            </p>
          </form>
        </Card>

        <div className="stack" aria-live="polite">
          {save.kind === "saved" && (
            <Banner title={save.status === 201 ? "Saved" : "Already saved"} icon="✓">
              {formatValue(save.observation.indicator, save.observation.value)} of {INDICATOR_BY_KEY[save.observation.indicator].label.toLowerCase()} for{" "}
              {save.observation.profile_id}, {formatDateTime(save.observation.timestamp)}.{" "}
              {save.status === 200 && "The server recognised an identical submission and did not duplicate it. "}
              <Link to={`/history?indicator=${save.observation.indicator}`}>View in history</Link>
            </Banner>
          )}
          {save.kind === "failed" && (
            <Banner tone="error" title="NOT SAVED">
              {save.error.status === 409
                ? "An observation with this ID already exists with different content. Discard the draft to create a new one."
                : save.error.status === 422
                  ? "The server rejected the observation. Check the highlighted fields."
                  : `${save.error.message} Your draft is kept for this session; you can retry.`}
              {save.error.body.request_id && <span className="mono"> · ref {save.error.body.request_id}</span>}
            </Banner>
          )}
          <Banner title="Before you log">
            Manual entries are not compared with the simulated data. With fewer than 7 valid manual days you will see "insufficient history". This app does not
            interpret the value as good or bad.
          </Banner>
        </div>
      </div>
    </>
  );
}
