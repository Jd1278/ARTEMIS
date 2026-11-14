# Prompt de generación del frontend — ARTEMIS HEALTH (P0)

> Prompt autocontenido para un asistente de código o un desarrollador. Deriva de `requirements.md`, `design.md`, `architecture.md`, `supabase.md`, `migrations/001_initial.sql` y `data/demo/`. Si algo de este prompt contradice esos documentos, mandan los documentos.

---

## 1. Rol y objetivo

Actúa como ingeniero frontend senior especializado en interfaces de datos accesibles. Construye la interfaz web de **ARTEMIS HEALTH**, proyecto de NASA Space Apps Challenge 2026. La app permite a un tripulante **ficticio** registrar y entender la evolución personal de cuatro indicadores autoinformados durante una misión simulada de 180 días, con procedencia y calidad explícitas.

No es un producto clínico. Prohibido mostrar diagnósticos, terapias, clasificación normal/enfermo, riesgo clínico, puntuaciones de salud o semáforos (RNF-16). Se describen diferencias respecto al historial propio, nada más.

## 2. Stack y restricciones técnicas

- **React 19 + TypeScript (strict) + Vite.** Vite solo existe en desarrollo; en entrega FastAPI sirve `frontend/dist` y `/api` desde el mismo proceso. No hay microservicios.
- **react-router** con rutas SPA. El backend añadirá el fallback a `index.html`; no uses rutas hash.
- **Recharts** para las gráficas. Los `null` deben producir hueco (`connectNulls={false}`), nunca cero ni interpolación.
- **CSS plano con variables** desde `src/design-system/tokens.css`. Ningún color, radio ni espaciado fuera de los tokens (RNF-14). Sin frameworks CSS.
- **Tipografía local empaquetada**, sin CDN ni recursos remotos (RNF-05).
- **El navegador nunca habla con Supabase.** El flujo es navegador → `/api` → PostgreSQL. Sin claves, `service_role` ni secretos en el cliente (RNF-10).
- **Capa de servicios intercambiable:** interfaz `ArtemisApi` con dos implementaciones.
  - `mock`: por defecto mientras el backend esté en construcción. Lee `data/demo/observations.json` e implementa el contrato completo (validación, idempotencia, comparación).
  - `http`: usa `fetch` contra `/api`.
  - Se selecciona con `VITE_API_MODE=mock|http`. Ningún componente importa una implementación concreta.
- No inventes un lockfile; `npm install` lo genera con versiones reales.

## 3. Dominio

### Indicadores (P0)
| clave | etiqueta | unidad | contexto | dominio técnico | notas de UI |
|---|---|---|---|---|---|
| `sleep_duration_h` | Duración del sueño | `h` | `sleep_report` | 0–24, decimal | Autoinforme, no actigrafía. |
| `samn_perelli` | Fatiga percibida | `points_1_7` | `fatigue_report` | entero 1–7 | 1 = totalmente alerta; 7 = completamente agotado. Escala Samn–Perelli. |
| `stress_vas` | Estrés percibido | `points_0_100` | `stress_report` | 0–100, decimal | 0 = nada de estrés; 100 = estrés máximo imaginable. Escala visual analógica. |
| `resting_hr_bpm` | Pulso en reposo | `bpm` | `rest` | > 0 | Medido en reposo. |

Conserva las escalas originales: nunca conviertas fatiga ni estrés a 1–5. Las diferencias de fatiga y estrés se expresan en **puntos**, no en porcentajes. Son dominios técnicos, no rangos saludables.

### Observación (contrato)
`id` (UUID), `profile_id`, `indicator`, `value` (number|null), `source_value` (number|null), `unit`, `timestamp` (ISO 8601 UTC), `mission_day`, `context`, `namespace` (`demo`|`research`), `origin_type` (`synthetic`|`user_report`|`public_dataset`), `capture_method` (`import`|`manual`|`sensor`), `quality_flags` (string[]), `source_file`, `source_row`.

- Un flag `<indicador>_imputed` o `<indicador>_out_of_range` implica `value = null`. `source_value` se conserva solo para auditoría y se muestra como "valor original excluido", nunca como medición (RNF-12).
- Perfiles: `CM-01`…`CM-06`, tripulación ficticia de la misión `SIM-ISS-180`, lanzamiento 2026-03-01, 180 días. Roles: Commander, Flight Engineer 1–3, Science Officer, Medical Officer.
- Etiqueta siempre el origen real (RNF-15): `synthetic` → "SIMULADO"; `user_report` → "Registro manual"; `public_dataset` → "Dato público" (solo research, P1).
- Ignora siempre `baseline_*`, `status_*`, `overall_status`, `risk_score`, `event_label` e `is_anomaly`.

## 4. Contrato API

| Método y ruta | Uso |
|---|---|
| `GET /api/profiles` | Perfiles ficticios. |
| `GET /api/indicators` | Indicadores con unidad, contexto y dominio. |
| `GET /api/profiles/{id}/dashboard?at=` | Último valor por indicador hasta el cursor. |
| `POST /api/observations` | Registro manual: 201 si es nuevo, 200 si es una repetición idéntica, 409 si el UUID ya existe con otro contenido, 422 si no valida. |
| `GET /api/profiles/{id}/observations?indicator=&from=&to=` | Historial filtrado, en orden temporal y con filtros inclusivos. |
| `GET /api/profiles/{id}/comparison?indicator=&at=` | Comparación `baseline_v1`. |
| `GET /api/education/{indicator}` | Ficha educativa. |

Las fechas van en ISO 8601 UTC. Los errores siguen el formato `{ code, message, fields, request_id }`; muestra `fields` junto al campo correspondiente y `request_id` en el detalle técnico. El UUID de una captura lo genera el cliente una vez por borrador (`crypto.randomUUID()`) y se reutiliza en cada reintento.

## 5. Regla de comparación `baseline_v1` (RF-09, RF-10, RF-11)

- **Ventana:** días anteriores al cursor, dentro de 30 días, usando como máximo los 14 días válidos más recientes.
- **Mínimo:** 7 días válidos. Con menos, se muestra "Historial insuficiente (n de 7 días)" y no se calcula nada.
- **Exclusiones:** el día actual del cursor, los días futuros, los valores `null` (imputados o fuera de dominio) y las demás unidades, contextos u orígenes. `synthetic` y `user_report` no comparten línea base.
- **Agregación diaria:** se usa la última observación válida de cada día.
- **Explicación visible:** mediana, valor actual, diferencia con signo y unidad, días usados, periodo cubierto y `rule_version`.
- **Sin interpretación:** no hay umbrales, colores de severidad ni adjetivos clínicos. La redacción es neutra, por ejemplo: "2,1 h menos que la mediana de tus 14 días previos".
- **Cursor de misión:** todo cálculo respeta el día del cursor, nunca la fecha del equipo. La demo muestra fechas históricas sin fingir que son actuales.

## 6. Pantallas

Todas comparten un shell con el banner fijo **DEMO · DATOS SIMULADOS** (RF-01), un selector de perfil y un selector de día de misión (1–180).

1. **Resumen**
   - Cuatro tarjetas, una por indicador, con último valor válido, unidad, día de misión, fecha, origen y calidad (RF-02).
   - Si el último valor es nulo: "valor excluido (imputado)" y el valor válido anterior con su antigüedad ("dato antiguo, hace n días").
   - Al seleccionar una tarjeta: gráfica de los últimos 30 días y explicación de la comparación.
   - El último valor y su origen deben verse en la primera pantalla (RNF-01).
2. **Registrar** (RF-03, RF-04, RF-14, RF-15)
   - Formulario con etiquetas persistentes: perfil, indicador, valor, hora y contexto derivado del indicador.
   - Ayuda de escala con ambos extremos y aviso de autoinforme.
   - Validación local de valores no finitos, dominio, enteros en fatiga y fechas inválidas. El servidor valida igual.
   - El borrador se conserva en `sessionStorage` durante la sesión. Si guardar falla, muestra **NO GUARDADO**, conserva el borrador y ofrece reintentar con el mismo UUID. Solo un 201 o 200 confirma el guardado.
   - Avisa que los primeros registros manuales tienen historial insuficiente.
3. **Historial** (RF-07, RF-08)
   - Filtros por perfil, indicador y periodo (días de misión o fechas).
   - La gráfica deja huecos en los nulos.
   - Una tabla accesible muestra exactamente los mismos puntos: día, fecha, valor, original excluido, origen, método y flags.
   - Interruptor para cambiar entre gráfica y tabla.
4. **Aprender** (RF-13): cuatro fichas locales con qué mide el indicador, cómo se registra, cómo leer la escala, límites ("no diagnostica") y una referencia revisada.
5. **Galería de componentes** (`/componentes`, interna): todos los componentes y estados con datos fijos, para aprobación de I4 e I6.

### Estados obligatorios
Carga, vacío, imputado excluido, historial insuficiente, dato antiguo, error de guardado (NO GUARDADO) y API o Supabase no disponible. En este último caso se indica que no se puede consultar ni guardar y se conserva el borrador; no hay modo offline.

## 7. Diseño y accesibilidad

- **Paleta:** fondo `#08111F`, superficie `#122033`, texto `#F4F7FB`, secundario `#BCCBDD`, acento `#66D9E8`.
- **Escalas:** cuerpo 16 px, metadatos 14 px, objetivos táctiles de 44 px, radio de 12 px, espaciado 4/8/12/16/24/32.
- **Color:** ningún color representa estado clínico. El acento solo marca interacción y selección; los estados se comunican con texto e icono, además del color.
- **Layout:** navegación lateral en escritorio (≥ 1024 px), dos columnas en tablet y una columna con navegación inferior en móvil. Revisar a 360×800, 768×1024 y 1440×900 sin solapamientos (RNF-03).
- **Accesibilidad (RNF-02):**
  - Teclado completo y foco visible.
  - `label` en cada control.
  - Contraste ≥ 4.5:1.
  - Zoom al 200 % sin pérdida.
  - Gráficas con resumen textual y la tabla equivalente.
  - `aria-live` para el resultado de guardado.
- **Rendimiento:** panel usable en menos de 3 s con 1000 observaciones (RNF-04). Evita recalcular en cada render (memoización) y no cargues el dataset completo en componentes.

## 8. Prohibiciones

- No mostrar riesgo, estado, anomalía, semáforo ni "normal/anormal".
- No interpolar ni rellenar huecos. No usar valores excluidos en cálculos.
- No mezclar orígenes ni namespaces en un mismo cálculo (RNF-08).
- No admitir expedientes ni datos reales (RNF-09).
- No guardar en `localStorage` datos que deban persistir. La persistencia es solo del servidor; el borrador vive en la sesión.
- No acceder a Supabase desde el navegador.

## 9. Estructura esperada

```
frontend/
  index.html  package.json  vite.config.ts  tsconfig.json
  src/
    app/            router, providers, main.tsx
    layouts/        AppShell (navegación, banner, selectores)
    design-system/  tokens.css, base.css, components/
    services/       types.ts, api.ts, mockApi.ts, httpApi.ts, index.ts
    features/
      analysis/     baseline.ts (+ pruebas)
      dashboard/    observations/  history/  education/
```

## 10. Criterios de aceptación

- RF-01 a RF-04, RF-07 a RF-15 verificables en la UI con datos demo.
- RF-05 y RF-06 verificables contra el mock: 201, 200 en repetición y 409 en conflicto.
- `npm run build` sin errores. Las pruebas de `baseline.ts` cubren < 7 días, exclusión de imputados, exclusión del día actual y el máximo de 14 días.
- Capturas en los tres tamaños y recorrido completo con teclado.
- README con instrucciones para el modo mock y el modo http.
