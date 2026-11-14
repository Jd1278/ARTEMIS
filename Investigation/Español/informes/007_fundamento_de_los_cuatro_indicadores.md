# Fundamento y límites de los cuatro indicadores del MVP

**Informe:** 007 · **Fecha:** 14 de noviembre de 2026 · **Versión:** 1.0  
**Investigación secuencial:** 3 de 7. **Estado:** revisión documental concluida; protocolo y traducciones pendientes de revisión especializada.

## Conclusión

Sueño, fatiga, estrés y pulso permiten estudiar un seguimiento cotidiano acotado y contextual. No constituyen una evaluación completa de salud espacial ni permiten inferir inmunidad, densidad ósea o enfermedad. La selección es pertinente para una demo, pero no se ha demostrado que sea suficiente para uso operativo.

La investigación se inició al cerrar el informe 006. Se consultaron estudios originales, fuentes institucionales de instrumentos y orientación cardiovascular. No se inventaron umbrales clínicos ni se validó una escala propia. El alcance técnico corresponde a los [requisitos del commit 80be128](https://github.com/Jd1278/ARTEMIS/blob/80be128b17b5046ecd267d5a0604bbc5c74f5444/artemis-healt/docs/requirements.md).

## Evidencia transversal

Jones y colaboradores estudiaron longitudinalmente 24 astronautas en misiones de aproximadamente seis meses en la ISS. Recogieron autoinformes y pruebas de vigilancia; el sueño más corto se asoció con peor velocidad de respuesta y mayor estrés/carga percibida. El estudio es observacional: no proporciona un diagnóstico individual ni demuestra eficacia de ARTEMIS. [Jones et al., Sleep, 2022; DOI 10.1093/sleep/zsac006](https://pmc.ncbi.nlm.nih.gov/articles/PMC8919197/).

## Fichas de interpretación

| Indicador | Qué representa | Cómo documentarlo | Qué no puede concluirse |
| --- | --- | --- | --- |
| `sleep_duration_h` | Tiempo de sueño estimado por la persona para un episodio definido. | Horas; periodo recordado, hora de registro y método. Distinguir tiempo en cama, sueño estimado y siestas. | Etapas de sueño, diagnóstico de insomnio o exactitud equivalente a polisomnografía. |
| `samn_perelli` | Fatiga subjetiva en una escala ordinal de siete categorías. | Conservar escala 1–7 y descripción consistente de cada categoría. | Aptitud automática para pilotar o realizar tareas, diagnóstico o relaciones de proporción entre puntuaciones. |
| `stress_vas` | Intensidad de estrés percibido según pregunta y anclajes definidos. | Especificar periodo, extremos, modalidad de entrada y escala 0–100. | Trastorno psicológico, nivel hormonal o riesgo médico. |
| `resting_hr_bpm` | Frecuencia de latidos en un contexto de reposo definido. | Latidos/minuto, método o dispositivo, contexto, actividad reciente y calidad. | Presión arterial, ritmo ECG completo, oxigenación o exclusión de enfermedad. |

### Sueño

El Consensus Sleep Diary fue desarrollado para estandarizar el autorregistro prospectivo; ofrece un referente para formular preguntas y distinguir componentes del sueño. Un único campo de horas en ARTEMIS no equivale a implementar ni validar ese instrumento. [Carney et al., Sleep, 2012; DOI 10.5665/sleep.1642](https://pmc.ncbi.nlm.nih.gov/articles/PMC3250369/).

El custodio universitario indica condiciones para uso no lucrativo sin alteración y con cita. Antes de reproducir el formulario completo, adaptarlo o usarlo comercialmente hay que aclarar permisos; este informe no lo incorpora. [University of Pittsburgh, instrumentos](https://www.sleep.pitt.edu/research/measures-and-study-instruments).

### Fatiga

La documentación de gestión de fatiga alojada por ICAO describe Samn–Perelli como escala subjetiva de siete puntos. Su origen y uso aeronáutico no validan automáticamente una traducción española ni su uso como decisión clínica espacial. [ICAO, Biomathematical Fatigue Models, 2014](https://www.icao.int/safety/fatiguemanagement/ArticlesPublications/biomathematical_fatigue_models.pdf).

Mantener el sentido ordinal: 6 indica una categoría mayor que 3, pero no «el doble de fatiga». Mostrar variaciones en puntos y categorías sin porcentajes de mejoría. La traducción y las instrucciones deben revisarse antes de denominarlas versión validada.

### Estrés

Lesage y colaboradores examinaron sensibilidad discriminativa y validez entre conceptos de una escala visual analógica de estrés en un contexto terrestre. Esa evidencia es específica del instrumento y población estudiados. Un deslizador digital, pregunta o periodo diferente necesita comprobación adicional. [Lesage et al., Occupational Medicine, 2012; DOI 10.1093/occmed/kqs140](https://pubmed.ncbi.nlm.nih.gov/22965867/).

El campo debe llamarse «estrés percibido» y aclarar el periodo al que se responde. Un valor de cero significa la respuesta al instrumento, no ausencia de todo problema psicológico.

### Pulso

La AHA diferencia frecuencia cardíaca y presión arterial y describe cómo actividad, postura, emociones, temperatura y fármacos pueden influir en el pulso. Por tanto, una comparación exige contexto consistente. No se adoptan sus rangos educativos terrestres como semáforo universal de astronautas. [AHA, All About Heart Rate](https://www.heart.org/en/health-topics/high-blood-pressure/the-facts-about-high-blood-pressure/all-about-heart-rate-pulse).

Antes de integrar un wearable se deben documentar método, ubicación, periodo de reposo, precisión y condiciones del dispositivo. El informe no prescribe un protocolo médico ni asume que ya existe un sensor conectado.

## Reglas del producto y calidad

Los dominios sueño 0–24 h, fatiga entera 1–7, estrés 0–100 y pulso positivo son validaciones técnicas del formulario. No dividen sano/enfermo. La mediana de hasta 14 días previos dentro de 30 y mínimo siete días válidos es una elección de ingeniería de la especificación, sin validación clínica encontrada.

Comparar solo datos compatibles; excluir actual/futuro y valores imputados. El historial de una persona tampoco garantiza seguridad: una condición persistente podría formar parte de su referencia. Las desviaciones descriptivas deben mantener esa limitación.

## Resultado y siguiente paso

Quedan cuatro fichas fundamentadas, campos de contexto y criterios de interpretación. Pendientes: revisión profesional, permisos de instrumentos, traducciones, modalidad de estrés y evaluación de comprensión. Esta revisión cierra la investigación documental de indicadores; no se ha medido precisión de sensores ni beneficio clínico. Se puede continuar con la auditoría de datos.
