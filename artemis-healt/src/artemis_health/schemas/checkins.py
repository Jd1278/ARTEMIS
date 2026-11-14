"""Schemas and validators for daily wellness check-ins."""
from __future__ import annotations

import re
import uuid
from datetime import date, datetime
from typing import Any, List, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator

from artemis_health.core.exceptions import DomainValidationError

PII_PATTERNS = re.compile(
    r"\b(ssn|dni|cedula|pasaporte|historia\s*clinica|expediente\s*medico|paciente\s*real)\b",
    re.IGNORECASE,
)


class CheckinCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique UUID for idempotency.")
    profile_id: str = Field(default="demo", description="Fictional astronaut profile ID.")
    date: str = Field(..., description="Check-in calendar date (YYYY-MM-DD).")
    fatigue: int = Field(..., description="Perceived fatigue on discrete 1-5 scale.")
    perceived_stress: int = Field(..., description="Perceived stress on discrete 1-5 scale.")
    notes: Optional[str] = Field(default=None, description="Optional non-identifiable wellness notes.")
    origin_type: str = Field(default="user_report")
    capture_method: str = Field(default="manual")

    @model_validator(mode="before")
    @classmethod
    def validate_checkin(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            raise DomainValidationError("El cuerpo del check-in debe ser un objeto JSON válido.")
        payload = dict(data)

        if "id" not in payload and "uuid" in payload:
            payload["id"] = payload.pop("uuid")
        else:
            payload.pop("uuid", None)

        if "date" not in payload and "checkin_date" in payload:
            payload["date"] = payload.pop("checkin_date")
        else:
            payload.pop("checkin_date", None)

        if "perceived_stress" not in payload and "stress" in payload:
            payload["perceived_stress"] = payload.pop("stress")
        else:
            payload.pop("stress", None)

        # Validate UUID
        raw_id = payload.get("id")
        if raw_id is not None:
            try:
                payload["id"] = str(uuid.UUID(str(raw_id)))
            except (ValueError, TypeError) as exc:
                raise DomainValidationError(
                    f"El identificador '{raw_id}' no es un UUID válido.",
                    fields={"id": ["UUID inválido"]},
                ) from exc

        # Validate date
        raw_date = payload.get("date")
        if not raw_date:
            raise DomainValidationError("La fecha ('date') es obligatoria.", fields={"date": ["Fecha requerida"]})
        try:
            if isinstance(raw_date, datetime):
                parsed_date = raw_date.date()
            elif isinstance(raw_date, date):
                parsed_date = raw_date
            else:
                text = str(raw_date).strip()
                if "T" in text:
                    parsed_date = datetime.fromisoformat(text.replace("Z", "+00:00")).date()
                else:
                    parsed_date = date.fromisoformat(text)
            payload["date"] = parsed_date.isoformat()
        except ValueError as exc:
            raise DomainValidationError(
                f"Fecha inválida: '{raw_date}'. Use formato YYYY-MM-DD.",
                fields={"date": ["Formato de fecha inválido"]},
            ) from exc

        # Validate fatigue (1-5 integer)
        for field_name in ("fatigue", "perceived_stress"):
            val = payload.get(field_name)
            if val is None or isinstance(val, bool):
                raise DomainValidationError(
                    f"El campo '{field_name}' es obligatorio y debe ser un entero en escala 1-5.",
                    fields={field_name: ["Requerido (escala 1-5)"]},
                )
            try:
                num = float(val)
            except (ValueError, TypeError) as exc:
                raise DomainValidationError(
                    f"El campo '{field_name}' debe ser numérico.",
                    fields={field_name: ["Valor no numérico"]},
                ) from exc
            if num != int(num) or int(num) < 1 or int(num) > 5:
                raise DomainValidationError(
                    f"El campo '{field_name}' ({val}) debe ser un entero en la escala 1 a 5.",
                    fields={field_name: ["Debe ser un entero entre 1 y 5"]},
                )
            payload[field_name] = int(num)

        # Validate optional non-identifiable notes
        notes = payload.get("notes")
        if notes is not None:
            if not isinstance(notes, str):
                raise DomainValidationError("El campo 'notes' debe ser texto.", fields={"notes": ["Texto inválido"]})
            cleaned_notes = notes.strip()
            if len(cleaned_notes) > 500:
                raise DomainValidationError(
                    "Las notas opcionales no pueden exceder 500 caracteres.",
                    fields={"notes": ["Máximo 500 caracteres"]},
                )
            if PII_PATTERNS.search(cleaned_notes):
                raise DomainValidationError(
                    "Las notas no deben incluir identificadores personales ni expedientes médicos reales.",
                    fields={"notes": ["Contenido identificable no permitido"]},
                )
            payload["notes"] = cleaned_notes or None

        return payload


class CheckinOut(BaseModel):
    id: str
    profile_id: str
    namespace: str = "demo"
    date: str
    fatigue: int
    perceived_stress: int
    notes: Optional[str] = None
    origin_type: str = "user_report"
    capture_method: str = "manual"
    quality_flag: str = "ok"
    created_at: str


class CheckinCreateResponse(BaseModel):
    status: str = Field(..., description="'created' or 'idempotent_replay'")
    save_status: str = "GUARDADO"
    idempotent: bool = False
    checkin: CheckinOut
    generated_observation_ids: List[str] = Field(default_factory=list)
    disclaimer: str
