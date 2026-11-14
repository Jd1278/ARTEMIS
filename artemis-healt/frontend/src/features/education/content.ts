import type { EducationCard } from "../../services/types";

// Local educational cards (RF-13). References must be confirmed by I1 before the demo:
// review_status stays "pendiente de revisión" until someone checks citation and URL.
export const EDUCATION_CARDS: EducationCard[] = [
  {
    indicator: "sleep_duration_h",
    title: "Duración del sueño",
    measures: "Las horas que crees haber dormido en tu último periodo de descanso.",
    how_to_record: "Anota las horas al despertar, con decimales si hace falta (7,5 = siete horas y media).",
    scale: "De 0 a 24 horas. Es un autoinforme: no sustituye a la actigrafía ni a la polisomnografía.",
    limits: [
      "No detecta trastornos del sueño ni mide su calidad.",
      "La percepción propia puede diferir de la duración real.",
      "La comparación solo usa tu propio historial, no rangos poblacionales.",
    ],
    reference: {
      citation: "NASA Human Research Program — Risk of Performance Decrements and Adverse Health Outcomes Resulting from Sleep Loss, Circadian Desynchronization, and Work Overload.",
      url: "https://humanresearchroadmap.nasa.gov/",
      review_status: "pendiente de revisión",
    },
  },
  {
    indicator: "samn_perelli",
    title: "Fatiga percibida (Samn–Perelli)",
    measures: "Cómo de cansado te sientes en este momento.",
    how_to_record: "Elige un único número entero de 1 a 7 según la descripción que mejor te encaje.",
    scale: "1 = totalmente alerta, completamente despierto; 4 = un poco cansado, por debajo de lo óptimo; 7 = completamente agotado, incapaz de funcionar con eficacia.",
    limits: [
      "Es una escala subjetiva de siete puntos; no mide rendimiento.",
      "Las diferencias se expresan en puntos, nunca en porcentajes.",
      "No indica si hay o no un problema de salud.",
    ],
    reference: {
      citation: "Samn, S. W. & Perelli, L. P. (1982). Estimating aircrew fatigue: a technique with application to airlift operations. USAF School of Aerospace Medicine, SAM-TR-82-21.",
      url: null,
      review_status: "pendiente de revisión",
    },
  },
  {
    indicator: "stress_vas",
    title: "Estrés percibido (escala visual analógica)",
    measures: "La intensidad del estrés que percibes ahora.",
    how_to_record: "Indica un valor entre 0 y 100 donde marcarías tu estrés en una línea continua.",
    scale: "0 = nada de estrés; 100 = el máximo estrés imaginable. Los valores intermedios no tienen etiquetas fijas.",
    limits: [
      "Es una valoración personal y cambia con el contexto del día.",
      "No es un test psicológico validado para diagnóstico.",
      "Las diferencias se expresan en puntos, no en porcentajes.",
    ],
    reference: {
      citation: "Lesage, F.-X., Berjot, S. & Deschamps, F. (2012). Clinical stress assessment using a visual analogue scale. Occupational Medicine, 62(8), 600–605.",
      url: "https://doi.org/10.1093/occmed/kqs140",
      review_status: "pendiente de revisión",
    },
  },
  {
    indicator: "resting_hr_bpm",
    title: "Pulso en reposo",
    measures: "Los latidos del corazón por minuto en reposo.",
    how_to_record: "Mídelo tras unos minutos sentado o tumbado y en calma, siempre en condiciones parecidas.",
    scale: "Latidos por minuto (lpm). El único límite técnico es que sea mayor que 0.",
    limits: [
      "Cambia con la postura, la actividad reciente, la cafeína o la hora del día.",
      "Un valor aislado no significa nada por sí solo.",
      "La app no clasifica el pulso como normal o anormal.",
    ],
    reference: {
      citation: "NASA Human Research Program — Risk of Cardiovascular Adaptations Contributing to Adverse Mission Performance and Health Outcomes.",
      url: "https://humanresearchroadmap.nasa.gov/",
      review_status: "pendiente de revisión",
    },
  },
];
