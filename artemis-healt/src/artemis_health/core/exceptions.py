"""Uniform application exceptions and FastAPI error handlers."""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from artemis_health.core.logging import get_logger, redact_secrets

logger = get_logger("artemis_health.errors")


class ArtemisError(Exception):
    """Base domain error for ARTEMIS HEALTH."""

    def __init__(
        self,
        message: str,
        *,
        code: str = "ARTEMIS_ERROR",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        fields: Optional[Dict[str, Any]] = None,
        save_status: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = redact_secrets(message)
        self.code = code
        self.status_code = status_code
        self.fields = fields or {}
        self.save_status = save_status


class DomainValidationError(ArtemisError):
    """Raised when an input fails domain or technical range validation (HTTP 422)."""

    def __init__(self, message: str, *, fields: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            message,
            code="DOMAIN_VALIDATION_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            fields=fields,
            save_status="NO_GUARDADO",
        )


class ObservationConflictError(ArtemisError):
    """Raised when an existing UUID is re-submitted with different payload content (HTTP 409)."""

    def __init__(self, message: str, *, fields: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            message,
            code="UUID_CONFLICT",
            status_code=status.HTTP_409_CONFLICT,
            fields=fields,
            save_status="NO_GUARDADO",
        )


class ResourceNotFoundError(ArtemisError):
    """Raised when a requested profile, indicator, or resource does not exist (HTTP 404)."""

    def __init__(self, message: str, *, fields: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            message,
            code="RESOURCE_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            fields=fields,
        )


class NamespaceIsolationError(ArtemisError):
    """Raised when an operation attempts to mix research and demo namespaces (HTTP 422/403)."""

    def __init__(self, message: str, *, fields: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(
            message,
            code="NAMESPACE_ISOLATION_VIOLATION",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            fields=fields,
            save_status="NO_GUARDADO",
        )


class SupabaseUnavailableError(ArtemisError):
    """Raised when Supabase / PostgreSQL connection or query fails (HTTP 503)."""

    def __init__(
        self,
        message: str = "Servicio de base de datos Supabase no disponible temporalmente. El registro NO FUE GUARDADO.",
        *,
        fields: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            message,
            code="SUPABASE_UNAVAILABLE",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            fields=fields,
            save_status="NO_GUARDADO",
        )


def _build_error_payload(
    *,
    code: str,
    message: str,
    status_code: int,
    fields: Optional[Dict[str, Any]] = None,
    save_status: Optional[str] = None,
    request_id: Optional[str] = None,
) -> Dict[str, Any]:
    req_id = request_id or str(uuid.uuid4())
    safe_message = redact_secrets(message)
    payload: Dict[str, Any] = {
        "status": "error",
        "code": code,
        "message": safe_message,
        "detail": safe_message,
        "fields": fields or {},
        "request_id": req_id,
        "error": {
            "code": code,
            "message": safe_message,
            "fields": fields or {},
            "request_id": req_id,
        },
    }
    if save_status:
        payload["save_status"] = save_status
    return payload


def register_exception_handlers(app: FastAPI) -> None:
    """Attach uniform JSON exception handlers to the FastAPI app."""

    @app.exception_handler(ArtemisError)
    async def handle_artemis_error(request: Request, exc: ArtemisError) -> JSONResponse:
        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        logger.warning(
            "Domain exception [%s] on %s %s: %s",
            exc.code,
            request.method,
            request.url.path,
            exc.message,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=_build_error_payload(
                code=exc.code,
                message=exc.message,
                status_code=exc.status_code,
                fields=exc.fields,
                save_status=exc.save_status,
                request_id=req_id,
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        field_errors: Dict[str, List[str]] = {}
        messages: List[str] = []
        for err in exc.errors():
            loc = ".".join(str(part) for part in err.get("loc", []) if part != "body") or "payload"
            msg = err.get("msg", "Valor inválido")
            field_errors.setdefault(loc, []).append(msg)
            messages.append(f"{loc}: {msg}")
        summary = "; ".join(messages) if messages else "Error de validación en los datos enviados."
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_build_error_payload(
                code="VALIDATION_ERROR",
                message=summary,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                fields=field_errors,
                save_status="NO_GUARDADO",
                request_id=req_id,
            ),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        logger.error(
            "Unexpected error (%s) on %s %s",
            type(exc).__name__,
            request.method,
            request.url.path,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_build_error_payload(
                code="INTERNAL_SERVER_ERROR",
                message="Error interno del servidor. La operación no pudo completarse.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                save_status="NO_GUARDADO",
                request_id=req_id,
            ),
        )
