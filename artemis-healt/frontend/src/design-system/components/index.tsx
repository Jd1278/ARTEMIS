import { useId, type ButtonHTMLAttributes, type ReactNode } from "react";
import "./components.css";
import { describeFlag, isExcludedFlag, ORIGIN_LABEL } from "../../services/domain";
import type { CaptureMethod, OriginType } from "../../services/types";
import { EmptyIllustration } from "../illustrations";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "primary" | "secondary" | "ghost" };
export function Button({ variant = "secondary", className = "", ...rest }: ButtonProps) {
  return <button type="button" className={`btn btn--${variant} ${className}`} {...rest} />;
}

export function Card({ children, className = "", as: Tag = "section", ...rest }: { children: ReactNode; className?: string; as?: "section" | "article" | "div" } & Record<string, unknown>) {
  return (
    <Tag className={`card ${className}`} {...rest}>
      {children}
    </Tag>
  );
}

interface FieldProps {
  label: string;
  hint?: ReactNode;
  error?: string;
  children: (props: { id: string; "aria-describedby"?: string; "aria-invalid"?: boolean }) => ReactNode;
}
/** Persistent label + hint + error wired with aria attributes. */
export function Field({ label, hint, error, children }: FieldProps) {
  const id = useId();
  const hintId = hint ? `${id}-hint` : undefined;
  const errorId = error ? `${id}-error` : undefined;
  const describedBy = [hintId, errorId].filter(Boolean).join(" ") || undefined;
  return (
    <div className="field">
      <label className="field__label" htmlFor={id}>
        {label}
      </label>
      {hint && (
        <span id={hintId} className="field__hint">
          {hint}
        </span>
      )}
      {children({ id, "aria-describedby": describedBy, "aria-invalid": error ? true : undefined })}
      {error && (
        <span id={errorId} className="field__error">
          <span aria-hidden="true">✕</span> {error}
        </span>
      )}
    </div>
  );
}

export function SimBadge() {
  return <span className="badge badge--sim">SIMULADO</span>;
}

export function OriginBadge({ origin, method }: { origin: OriginType; method?: CaptureMethod }) {
  const methodLabel = method === "import" ? "importado" : method === "manual" ? "manual" : method;
  return (
    <span className={`badge ${origin === "synthetic" ? "badge--sim" : ""}`}>
      {ORIGIN_LABEL[origin]}
      {methodLabel && origin !== "user_report" ? ` · ${methodLabel}` : ""}
    </span>
  );
}

export function QualityBadge({ flags }: { flags: string[] }) {
  const excluded = flags.find(isExcludedFlag);
  return (
    <span className={`badge ${excluded ? "badge--excluded" : ""}`}>
      <span aria-hidden="true">{excluded ? "⊘" : "✓"}</span>
      {describeFlag(excluded ?? flags[0] ?? "ok")}
    </span>
  );
}

export function Banner({ tone = "info", title, children, icon }: { tone?: "info" | "error"; title: string; children?: ReactNode; icon?: string }) {
  return (
    <div className={`banner banner--${tone}`} role={tone === "error" ? "alert" : "status"}>
      <span className="banner__icon" aria-hidden="true">
        {icon ?? (tone === "error" ? "!" : "i")}
      </span>
      <div className="stack" style={{ gap: "var(--space-1)" }}>
        <p className="banner__title">{title}</p>
        {children && <div className="meta">{children}</div>}
      </div>
    </div>
  );
}

export function EmptyState({ title, children }: { title: string; children?: ReactNode }) {
  return (
    <div className="state">
      <EmptyIllustration />
      <p style={{ fontWeight: 700, color: "var(--text)" }}>{title}</p>
      {children && <p className="meta">{children}</p>}
    </div>
  );
}

export function Skeleton({ label = "Cargando…", height }: { label?: string; height?: number }) {
  return (
    <div className="skeleton" style={height ? { minHeight: height } : undefined} role="status" aria-live="polite">
      <span className="visually-hidden">{label}</span>
    </div>
  );
}

export function Segmented<T extends string>({ label, options, value, onChange }: { label: string; options: { value: T; label: string }[]; value: T; onChange: (v: T) => void }) {
  return (
    <div className="segmented" role="group" aria-label={label}>
      {options.map((o) => (
        <button key={o.value} type="button" aria-pressed={o.value === value} onClick={() => onChange(o.value)}>
          {o.label}
        </button>
      ))}
    </div>
  );
}
