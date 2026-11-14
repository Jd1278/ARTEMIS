import type { CSSProperties } from "react";
import type { IndicatorKey } from "../../services/types";
import "./scale.css";

// Samn–Perelli descriptors (7-point fatigue checklist).
const SAMN_PERELLI = [
  "Totalmente alerta, completamente despierto",
  "Muy animado, receptivo, pero no en el máximo",
  "Bien, algo descansado",
  "Un poco cansado, por debajo de lo óptimo",
  "Moderadamente cansado, con desgana",
  "Extremadamente cansado, con dificultad para concentrarse",
  "Completamente agotado, incapaz de funcionar con eficacia",
];

interface Props {
  indicator: IndicatorKey;
  value: string;
  onChange: (value: string) => void;
  inputProps: { id: string; "aria-describedby"?: string; "aria-invalid"?: boolean };
  onBlur: () => void;
}

const num = (v: string) => Number(v.replace(",", "."));

/** Visual input per scale. The numeric text box stays as the exact, keyboard-friendly source of truth. */
export function ScaleInput({ indicator, value, onChange, inputProps, onBlur }: Props) {
  if (indicator === "samn_perelli") {
    const current = Number.isInteger(num(value)) ? num(value) : null;
    return (
      <div className="stack" style={{ gap: "var(--space-2)" }}>
        <div className="sp-scale" role="radiogroup" aria-label="Fatiga percibida, escala de 1 a 7" aria-describedby={inputProps["aria-describedby"]} id={inputProps.id}>
          {SAMN_PERELLI.map((desc, i) => {
            const n = i + 1;
            const checked = current === n;
            return (
              <button
                key={n}
                type="button"
                role="radio"
                aria-checked={checked}
                aria-label={`${n}: ${desc}`}
                tabIndex={checked || (current === null && n === 1) ? 0 : -1}
                className={`sp-scale__item ${checked ? "is-checked" : ""}`}
                onClick={() => onChange(String(n))}
                onBlur={onBlur}
                onKeyDown={(e) => {
                  const delta = e.key === "ArrowRight" || e.key === "ArrowUp" ? 1 : e.key === "ArrowLeft" || e.key === "ArrowDown" ? -1 : 0;
                  if (!delta) return;
                  e.preventDefault();
                  const next = Math.min(7, Math.max(1, (current ?? n) + delta));
                  onChange(String(next));
                  const group = e.currentTarget.parentElement;
                  (group?.children[next - 1] as HTMLElement | undefined)?.focus();
                }}
              >
                <span className="sp-scale__n">{n}</span>
              </button>
            );
          })}
        </div>
        <div className="sp-scale__ends meta" aria-hidden="true">
          <span>Alerta</span>
          <span>Agotado</span>
        </div>
        <p className="sp-scale__desc" aria-live="polite">
          {current ? (
            <>
              <strong>{current}</strong> · {SAMN_PERELLI[current - 1]}
            </>
          ) : (
            <span className="meta">Elige un número del 1 al 7.</span>
          )}
        </p>
      </div>
    );
  }

  const cfg =
    indicator === "stress_vas"
      ? { min: 0, max: 100, step: 1, left: "Nada de estrés", right: "Máximo imaginable", suffix: "puntos" }
      : indicator === "sleep_duration_h"
        ? { min: 0, max: 14, step: 0.25, left: "0 h", right: "14 h (máx. técnico 24)", suffix: "h" }
        : { min: 30, max: 120, step: 1, left: "30 lpm", right: "120 lpm", suffix: "lpm" };
  const v = num(value);
  const sliderValue = Number.isFinite(v) && value.trim() !== "" ? Math.min(cfg.max, Math.max(cfg.min, v)) : (cfg.min + cfg.max) / 2;
  const pct = ((sliderValue - cfg.min) / (cfg.max - cfg.min)) * 100;
  const hasValue = value.trim() !== "" && Number.isFinite(v);

  return (
    <div className="stack" style={{ gap: "var(--space-2)" }}>
      <div className="scale-row">
        <input
          type="range"
          className={`scale-slider ${hasValue ? "" : "is-empty"}`}
          min={cfg.min}
          max={cfg.max}
          step={cfg.step}
          value={sliderValue}
          onChange={(e) => onChange(e.target.value)}
          onBlur={onBlur}
          aria-label={`Control deslizante, ${cfg.left} a ${cfg.right}`}
          style={{ "--pct": `${pct}%` } as CSSProperties}
        />
        <div className="scale-number">
          <input {...inputProps} className="input" inputMode="decimal" autoComplete="off" value={value} onChange={(e) => onChange(e.target.value)} onBlur={onBlur} />
          <span className="meta">{cfg.suffix}</span>
        </div>
      </div>
      <div className="sp-scale__ends meta" aria-hidden="true">
        <span>{cfg.left}</span>
        <span>{cfg.right}</span>
      </div>
      {indicator === "sleep_duration_h" && hasValue && (
        <div className="sleep-bar" aria-hidden="true">
          {Array.from({ length: 24 }, (_, h) => (
            <span key={h} style={{ opacity: v >= h + 1 ? 1 : v > h ? v - h : 0.12 }} />
          ))}
        </div>
      )}
    </div>
  );
}
