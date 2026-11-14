# ARTEMIS HEALTH · Identidad visual v1

Dirección propuesta para revisión visual. Fecha: 14 de noviembre de 2026.

## Concepto

**Precisión humana en órbita.** Un centro de misión que hace comprensible la evolución personal del sueño, la fatiga, el estrés y el pulso. La personalidad es serena, científica y exploradora. La fuerza visual nace del contraste, la composición y el emblema; los datos conservan una lectura tranquila.

Nombre visible: ARTEMIS HEALTH. Frase de marca propuesta: «Comprende tu evolución, día a día». No insinuar asociación oficial con NASA ni emplear sellos de terceros.

## Logo

Fuente: `frontend/public/img/logo-sin-fondo.png`. Conservar el emblema original: cohete ascendente, órbita, luna y circuitos. No redibujarlo ni cambiar sus proporciones, colores o inclinación. El nombre se compone como texto HTML junto al emblema; no incrustar texto adicional en la imagen.

El PNG tiene un lienzo amplio alrededor del emblema. Medir sus límites alfa antes de usarlo en navegación: el tamaño del archivo completo no equivale al tamaño visible del símbolo. Preparar después una copia recortada sin modificar el original. Hasta entonces, usar un contenedor de presentación controlado y comprobar que no corta los extremos del cohete. No asumir que ya existe un favicon o versión monocroma.

Aplicaciones: emblema visible de 48–56 px en navegación de escritorio; 36–40 px en móvil; 160–220 px en portada de marca. Usar siempre `object-fit: contain`. Área de respeto: al menos un cuarto del diámetro visible del emblema. Si el detalle se pierde a tamaño pequeño, usar el nombre textual hasta contar con un símbolo simplificado aprobado.

## Color

Paleta interpretada visualmente a partir del logo; los HEX siguientes son decisiones de diseño, no una extracción exacta de píxeles. Conservan la dirección oscura ya definida en el proyecto.

| Token | HEX | Uso |
| --- | --- | --- |
| Fondo orbital | #08111F | Fondo general |
| Superficie | #122033 | Tarjetas y navegación |
| Superficie elevada | #1A2D43 | Diálogos, popovers y hover |
| Borde discreto | #30465E | Separación decorativa |
| Borde de control | #66839F | Límites identificables de campos y controles |
| Texto principal | #F4F7FB | Títulos, valores y lectura |
| Texto secundario | #BCCBDD | Metadatos y ayudas |
| Cian órbita | #66D9E8 | Acción principal, selección y foco |
| Azul trayectoria | #79AAFF | Serie de fatiga y enlaces secundarios |
| Marfil lunar | #E8DFB7 | Acento editorial y serie de sueño |
| Verde agua | #7EDBC3 | Serie de pulso |
| Ámbar operativo | #F3C76A | Borrador, indisponibilidad e información pendiente |
| Coral operativo | #FF9AAB | Error de validación o guardado |

En botones cian usar texto #08111F. Los enlaces dentro del texto llevan subrayado. Nunca usar borde discreto como único identificador de un control. Verificar contraste por combinación: texto normal ≥4.5:1 y controles/foco ≥3:1. El informe `contrastes.json` registra combinaciones base; no sustituye la revisión de estados y transparencias implementados.

Distribución orientativa: 75% fondos oscuros, 18% superficies y texto, 5% cian y 2% acentos secundarios. El cian señala acciones y selección; el ámbar/coral describen operaciones de software. Ningún color clasifica la salud de la persona.

Series por indicador: sueño marfil, fatiga azul, estrés cian, pulso verde agua. El nombre, la unidad y el estilo de línea acompañan al color. Comparación con mediana mediante línea discontinua y etiqueta. Una gráfica principal muestra un indicador con su propia escala; evitar mezclar las cuatro unidades en un eje.

## Tipografía

Propuesta: Space Grotesk para marca y títulos; Inter para texto, formularios y navegación; IBM Plex Mono para fecha, día de misión e identificadores. Empaquetar WOFF2 localmente y conservar sus licencias. No están descargadas ni instaladas en esta entrega. Mientras tanto usar las familias de sistema definidas en los tokens.

Texto base 16/24 px; ayudas 14/20 px; título de pantalla 32/38 px, móvil 26/32 px; subtítulo 20/28 px; valor de tarjeta 36/40 px con cifras tabulares. Reservar las mayúsculas espaciadas a marca y etiquetas cortas, nunca a párrafos. No usar una fuente tecnológica ornamental para cifras o formularios.

## Composición y componentes

Base de espaciado: 4, 8, 12, 16, 24, 32, 48 y 64 px. Tarjetas con radio 16 px, campos y botones 10 px. Separación de tarjetas 16–24 px. Blanco visual suficiente, un solo CTA principal por bloque. Iconos Lucide de 20 o 24 px, trazo consistente y etiqueta para botones de icono.

Escritorio 1440×900: sidebar de 248 px, cabecera de contexto y contenido máximo 1280 px. Retícula de 12 columnas; cuatro tarjetas en una fila y gráfico de 8 columnas junto a explicación de 4. Tablet 768×1024: navegación compacta, dos tarjetas por fila y explicación bajo gráfica. Móvil 360×800: una columna, controles apilados y navegación inferior de cuatro destinos con espacio para safe area. Altura mínima de objetivos táctiles: 44 px. A 200% de zoom mantener lectura y acciones disponibles.

Motivo de marca: arcos orbitales finos y líneas de trayectoria en portada, encabezados vacíos o fondos editoriales. Sin estrellas detrás de tablas, sin animaciones continuas y sin brillo en cada tarjeta. Gradiente opcional #122033 → #1A2D43; el cian iluminado se limita al acento del encabezado. No usar globos 3D ni mapas corporales como decoración principal.

Movimiento: 160–220 ms para cambios de estado; entrada inicial máxima 300 ms. Respetar `prefers-reduced-motion`. Ningún dato debe depender de una animación para poder leerse.

## Voz y estados

Lenguaje directo en español: «Registrar observación», «Ver historial», «Historial insuficiente», «Dato excluido del cálculo». Evitar «salud óptima», «riesgo», «anomalía detectada», «paciente estable» o porcentajes de bienestar.

Mostrar DEMO y SIMULADO en el contexto global del perfil ficticio. Cada observación conserva además su propio origen: SIMULADO para synthetic y AUTOINFORME para user_report, sin etiquetar un registro manual como sintético. Procedencia, captura y calidad son etiquetas distintas. El entorno demo no admite expedientes reales.

Estados de operación: cargando, vacío, error de consulta, sin conexión, borrador NO GUARDADO, guardando, guardado confirmado y conflicto 409. Estados del dato: válido, nulo/excluido, historial insuficiente y última fecha disponible. Un éxito de guardado requiere respuesta real 200/201 del backend.

## Stack recomendado

| Capa | Elección | Propósito y límite |
| --- | --- | --- |
| Base | React + TypeScript + Vite | Mantener el frontend previsto y producir `frontend/dist` para FastAPI |
| Estilos | Tailwind CSS + tokens CSS | Componer interfaces con una paleta centralizada |
| Componentes | shadcn/ui | Componentes editables para diálogos, selects, pestañas y tablas; personalizar su aspecto |
| Navegación | React Router, modo declarativo | Rutas SPA; requiere fallback del servidor al desplegar |
| Datos remotos | TanStack Query + fetch | Caché por perfil/indicador/origen/cursor; invalidar tras guardar; no guardar datos demo como producción |
| Formularios | React Hook Form + Zod | Ayuda y validación de cliente; el backend sigue siendo autoridad |
| Gráficas | Recharts | Serie temporal con `connectNulls={false}`, escala temporal y tabla equivalente |
| Iconos | lucide-react | Un único vocabulario de iconos |
| Movimiento | CSS inicialmente; Motion opcional | Añadir Motion solo si las transiciones complejas lo justifican |

No añadir Next.js, servidor Node, Redux, Three.js o una segunda biblioteca de componentes en esta fase. Resolver versiones compatibles cuando se inicialice el frontend y generar el lockfile mediante el gestor; no escribirlo a mano. Esta entrega no instala dependencias.

## Referencias oficiales

- Vite: https://vite.dev/guide/
- Tailwind con Vite: https://tailwindcss.com/docs/installation/using-vite
- shadcn/ui con Vite: https://ui.shadcn.com/docs/installation/vite
- React Router: https://reactrouter.com/start/declarative/installation
- TanStack Query: https://tanstack.com/query/latest/docs/framework/react/overview
- React Hook Form: https://react-hook-form.com/get-started
- Zod: https://zod.dev/
- Recharts Line: https://recharts.github.io/en-US/api/Line/
- Lucide: https://lucide.dev/guide/react
- Movimiento accesible: https://motion.dev/docs/react-accessibility
- Kombai Design Systems: https://ww2.kombai.com/guides/make-agents-follow-a-design-system/
