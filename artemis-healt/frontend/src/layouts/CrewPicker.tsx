import { useRef } from "react";
import { useMission } from "../app/state";
import { IconChevron, IconClose } from "../design-system/icons";
import { CrewAvatar } from "../design-system/illustrations";
import { MISSION, PROFILES } from "../services/domain";

/** Crew selector: a trigger with the current avatar that opens a native modal dialog of crew cards. */
export function CrewPicker() {
  const { profileId, setProfileId } = useMission();
  const dialog = useRef<HTMLDialogElement>(null);
  const current = PROFILES.find((p) => p.id === profileId) ?? PROFILES[0];

  return (
    <div className="field">
      <span className="field__label" id="crew-label">
        Tripulante
      </span>
      <button type="button" className="crew-trigger" aria-labelledby="crew-label crew-current" aria-haspopup="dialog" onClick={() => dialog.current?.showModal()}>
        <CrewAvatar id={current.id} size={40} />
        <span className="crew-trigger__text" id="crew-current">
          <strong>{current.id}</strong>
          <span className="meta">{current.role} · ficticio</span>
        </span>
        <IconChevron dir="down" size={20} />
      </button>

      <dialog ref={dialog} className="crew-dialog" aria-labelledby="crew-dialog-title">
        <div className="row" style={{ justifyContent: "space-between" }}>
          <div>
            <h2 id="crew-dialog-title">Elige tripulante</h2>
            <p className="meta">Tripulación ficticia de {MISSION.name}. Ningún perfil corresponde a una persona real.</p>
          </div>
          <button type="button" className="btn" aria-label="Cerrar" onClick={() => dialog.current?.close()}>
            <IconClose size={20} />
          </button>
        </div>
        <div className="crew-grid">
          {PROFILES.map((p) => (
            <button
              key={p.id}
              type="button"
              className="crew-card"
              aria-pressed={p.id === profileId}
              autoFocus={p.id === profileId}
              onClick={() => {
                setProfileId(p.id);
                dialog.current?.close();
              }}
            >
              <CrewAvatar id={p.id} size={72} />
              <strong>{p.id}</strong>
              <span className="meta">{p.role}</span>
            </button>
          ))}
        </div>
      </dialog>
    </div>
  );
}
