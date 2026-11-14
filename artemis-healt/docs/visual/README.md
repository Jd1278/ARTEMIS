# Paquete visual ARTEMIS HEALTH

1. `01-identidad-visual.md`: marca, paleta, tipografía, componentes y stack propuesto.
2. `02-frames-modulos.md`: contenido y estados de cada pantalla, alcance P0/P1 y contratos pendientes.
3. `03-prompts-kombai.txt`: prompts secuenciales para copiar y pegar, desde componentes hasta integración.
4. `contrastes.json`: verificación numérica de combinaciones base de color.

Los documentos son Markdown editable y el archivo de prompts es texto plano. No se ha generado DOCX ni implementado el frontend. Los tokens reutilizables viven en `frontend/src/design-system/tokens.css` y preservan los nombres originales.

Flujo: adjuntar documentos, logo y tokens a Kombai; ejecutar prompt 01; revisar lenguaje visual y componentes; continuar por pantalla. Al recibir código de Kombai, revisar cambios limitados a frontend, build, accesibilidad y correspondencia con los requisitos antes de integrar.

El equipo backend mantiene Python, API, autenticación, persistencia, migraciones y reglas. El frontend mantiene composición visual, navegación, estados, presentación y validación de ayuda. El cálculo del dominio y la confirmación de guardado proceden del servidor. Ambos equipos acuerdan contratos antes de integrar.

La recomendación de librerías no implica que ya estén instaladas. Fuentes tipográficas propuestas pendientes de empaquetado y licencia. El logo original permanece intacto. Esta propuesta se limita a ARTEMIS HEALTH; una marca paraguas para otros proyectos requeriría una definición adicional.
