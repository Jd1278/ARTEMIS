# Riesgos para la salud en microgravedad y gravedad parcial

**Informe:** 002  
**Fecha:** 14 de noviembre de 2026  
**Versión:** 1.0  
**Tipo:** revisión documental exploratoria  
**Propósito:** fundamentar el problema de ASTROGUARD y orientar su presentación y desarrollo

## Pregunta y conclusión principal

**¿Qué riesgos biológicos, psicológicos y operativos pueden presentarse cuando una persona vive en microgravedad o en una gravedad inferior a la terrestre, y qué parte de su seguimiento puede apoyar ASTROGUARD?**

La reducción de la carga mecánica y los cambios de distribución de líquidos y de referencias sensoriales afectan a distintos sistemas del cuerpo. Entre los riesgos documentados del vuelo espacial están la pérdida ósea y muscular, el desacondicionamiento cardiovascular, las alteraciones visuales y las dificultades de orientación y equilibrio. La intensidad, la recuperación y el impacto operativo varían entre personas, fases de misión y duración de la exposición.

ASTROGUARD puede proponerse como apoyo al registro y la comprensión del seguimiento, pero los signos vitales habituales no permiten detectar todas estas alteraciones. La gravedad parcial de la Luna y Marte requiere especial cautela: no debe asumirse que protege suficientemente al cuerpo ni que produce exactamente los mismos efectos que la microgravedad orbital. [F03](https://www.nasa.gov/directorates/esdmd/hhp/cv-risk/), [F04](https://www.nasa.gov/reference/risk-of-reduced-cardiorespiratory-and-musculoskeletal-fitness/), [F15](https://www.nasa.gov/reference/risk-of-spaceflight-associated-neuro-ocular-syndrome-sans/), [F16](https://www.nasa.gov/directorates/esdmd/hhp/sensorimotor-risk/), [F18](https://ntrs.nasa.gov/citations/20210019591)

## Método y límites

Se revisaron explicaciones y síntesis de NASA, una publicación técnica sobre gravedad parcial y un estudio original longitudinal de recuperación ósea. Se utilizaron fuentes del informe 001 cuando correspondía. Las referencias completas y su alcance se conservan en el [registro de fuentes](../fuentes/registro_de_fuentes.md).

La búsqueda es exploratoria, no una revisión sistemática. No se descargaron mediciones de datasets ni se analizaron expedientes; las cifras citadas proceden de publicaciones identificadas. No se hicieron pruebas del software ni se verificaron funciones implementadas. Las implicaciones para ASTROGUARD son propuestas de diseño.

Debe diferenciarse evidencia humana de vuelo, resultados de análogos terrestres y extrapolaciones a otros destinos. Un reposo en cama, un vuelo parabólico o un sistema de descarga del peso reproducen aspectos de la exposición, pero no todo el entorno espacial ni sus efectos crónicos.

## Qué significa poca o nula gravedad

En una estación orbital sigue existiendo atracción gravitatoria. La nave y sus ocupantes se encuentran en caída libre conjunta, por lo que experimentan ingravidez aparente. Para describir ese entorno se utiliza **microgravedad**; decir que allí desapareció la gravedad es incorrecto. La masa y la inercia de los objetos tampoco desaparecen. [F12](https://www.nasa.gov/centers-and-facilities/glenn/what-is-microgravity/)

| Entorno | Condición relevante | Interpretación para la investigación |
| --- | --- | --- |
| Tierra | Referencia de aproximadamente 1 g. | La postura y la actividad cotidiana generan cargas mecánicas habituales. |
| Nave orbital o trayecto en caída libre | Microgravedad o ingravidez aparente. | Hay amplia experiencia humana orbital, con contramedidas y seguimiento médico. |
| Superficie lunar | Aproximadamente 0,17 g, alrededor de una sexta parte de la terrestre. | Hay carga parcial, pero no evidencia humana suficiente sobre residencia prolongada para cuantificar todos sus efectos. |
| Superficie marciana | Aproximadamente 0,38 g. | La extrapolación fisiológica de larga duración tiene incertidumbre. |

Las proporciones de gravedad superficial están documentadas por NASA. No constituyen porcentajes equivalentes de riesgo: 0,38 g no significa 38 % del riesgo terrestre ni una reducción predecible de los daños. [F19](https://www.nasa.gov/wp-content/uploads/2018/05/explorediscover_-_teacher.pdf)

## Riesgos biológicos y funcionales

### Huesos y recuperación posterior

Al disminuir la carga que soporta el esqueleto, cambia su remodelación y puede reducirse la densidad y la resistencia ósea, especialmente en zonas que normalmente soportan peso. La pérdida puede elevar la vulnerabilidad frente a cargas posteriores. Su vigilancia requiere mediciones óseas apropiadas; el pulso y la saturación no la cuantifican. [F13](https://www.nasa.gov/reference/risk-of-spaceflight-induced-bone-changes/)

Un estudio de Gabel y colaboradores siguió a **17 astronautas** tras misiones de aproximadamente cuatro a siete meses, mediante tomografía periférica de alta resolución. **Nueve de los 17 no habían recuperado completamente la densidad mineral ósea total de la tibia al año del regreso.** Es un resultado de esa cohorte y ese sitio anatómico, no una tasa universal de daño irreversible. El seguimiento de doce meses no permite concluir que la recuperación nunca ocurra. [F14](https://pmc.ncbi.nlm.nih.gov/articles/PMC9247070/)

**Implicación para ASTROGUARD:** registrar ejercicio prescrito, evaluaciones y resultados clínicos disponibles. No mostrar una puntuación de densidad ósea calculada a partir de actividad o signos vitales.

### Músculos y capacidad para realizar tareas

La descarga del cuerpo puede reducir la aptitud muscular y cardiorrespiratoria. Las consecuencias son funcionales: dificultades para moverse y ejecutar tareas exigentes, especialmente al volver a un entorno con carga gravitatoria. El ejercicio de resistencia y aeróbico forma parte de las contramedidas, aunque su cumplimiento no demuestra por sí solo conservación completa de la función. [F04](https://www.nasa.gov/reference/risk-of-reduced-cardiorespiratory-and-musculoskeletal-fitness/)

**Implicación:** registrar rutinas aprobadas, esfuerzo percibido y resultados de evaluaciones cuando existan. La app no debe aumentar automáticamente la carga de entrenamiento ni premiar ignorar síntomas.

### Circulación y tolerancia a las transiciones

En microgravedad los líquidos se redistribuyen hacia la parte superior del cuerpo y se producen adaptaciones cardiovasculares. El riesgo depende de la fase: la tolerancia a cambios de postura y aceleración y el rendimiento al regresar a gravedad merecen atención. NASA también estudia cambios del flujo venoso y trombosis dentro del riesgo cardiovascular; no todos los astronautas desarrollan esos eventos. [F03](https://www.nasa.gov/directorates/esdmd/hhp/cv-risk/), [F02](https://www.nasa.gov/reference/medical-operations-and-clinical-care/)

**Implicación:** conservar frecuencia cardíaca y presión arterial solo si se miden apropiadamente, junto con síntomas, actividad y fase de misión. Ni un pulso normal ni una lectura de SpO₂ descartan alteraciones cardiovasculares, trombos o problemas de tolerancia ortostática.

### Ojos y visión

El síndrome neuroocular asociado al vuelo espacial, **SANS**, incluye hallazgos como edema del disco óptico, pliegues retinianos y aplanamiento de la parte posterior del globo ocular. La redistribución de líquidos es una línea importante de investigación, pero no debe presentarse como una explicación causal completa y cerrada. Las manifestaciones y sus consecuencias a largo plazo continúan estudiándose. [F15](https://www.nasa.gov/reference/risk-of-spaceflight-associated-neuro-ocular-syndrome-sans/)

**Implicación:** registrar síntomas visuales y resultados profesionales, con derivación al protocolo de misión. Un autoinforme de visión normal no descarta SANS; su evaluación requiere exploración y equipos especializados.

### Equilibrio, orientación y control del movimiento

Los cambios de gravedad modifican la función vestibular y sensoriomotora. Pueden aparecer mareo, náuseas, desorientación y dificultades de control postural, locomoción y motricidad fina. NASA destaca el impacto durante y después de las transiciones, cuando pueden coincidir con aterrizaje, salida de la nave y primeras actividades extravehiculares. [F16](https://www.nasa.gov/directorates/esdmd/hhp/sensorimotor-risk/)

**Implicación:** un registro breve de síntomas con fase y tiempo de aparición puede aportar contexto. Una interfaz simple puede ser útil, pero habrá que probarla; el MVP no debe certificar que alguien está apto para caminar, pilotar o realizar una salida.

### Salud urinaria y cálculos renales

Los cambios óseos pueden aumentar el calcio urinario. Junto con variaciones de hidratación y química de la orina, esto contribuye al riesgo de cálculos. La evaluación depende de datos clínicos y urinarios; no se obtiene únicamente de un wearable. [F17](https://www.nasa.gov/ochmo-mtb-003-urinary-health-2/)

**Implicación:** registrar síntomas y resultados aportados; incorporar recordatorios solo conforme a protocolos aprobados. No afirmar que la app detecta un cálculo o determina hidratación por frecuencia cardíaca.

### Inmunidad y otros efectos del vuelo

Hay alteraciones inmunitarias documentadas durante vuelos espaciales, pero coexisten gravedad alterada, estrés, radiación, descanso y otros factores. No corresponde adjudicar todos esos cambios exclusivamente a la microgravedad ni convertir una variación inmunitaria en una predicción de infección. [F05](https://www.nasa.gov/directorates/esdmd/hhp/immune-risk/)

**Implicación:** conservar síntomas y pruebas si se proporcionan. Una puntuación de inmunidad derivada de pulso, sueño o fatiga carece de respaldo en esta investigación.

## Componente psicológico y factores que deben separarse

Las dificultades de adaptación física y las molestias pueden coexistir con cansancio y problemas de bienestar. Sin embargo, el aislamiento, el confinamiento, la separación de la Tierra y las exigencias operativas son factores distintos de la gravedad. La evidencia revisada no permite afirmar que la microgravedad por sí sola provoque depresión o ansiedad en una persona. [F06](https://www.nasa.gov/directorates/esdmd/hhp/behavioral-health-risk/)

El sueño también depende de horarios, iluminación, carga de trabajo y ambiente. El registro de sueño, fatiga y estrés percibido es pertinente como contexto, sin atribuir automáticamente sus cambios a la gravedad. [F07](https://www.nasa.gov/reference/risk-from-inadequate-sleep-and-irregular-schedules/)

Para el pitch, separar las cadenas causales:

- **Gravedad alterada:** descarga mecánica, redistribución de líquidos y adaptación sensoriomotora.
- **Otros peligros espaciales:** radiación, aislamiento, distancia y entorno cerrado; pueden interactuar con los anteriores, pero requieren evidencia propia.

Esta separación evita afirmar, por ejemplo, que la ingravidez genera radiación o que todas las dificultades psicológicas se resuelven con sensores.

## Gravedad parcial y preguntas abiertas

Un trabajo técnico de Harry W. Jones publicado en ICES 2021, disponible en NASA NTRS, argumenta a partir de evidencia indirecta que la gravedad lunar y marciana podría ser insuficiente para mantener el acondicionamiento a largo plazo. Es un análisis técnico, no un ensayo de personas viviendo durante años en esos destinos. Su referencia a valores inferiores a 0,4 g **no debe transformarse en un umbral clínico validado** ni en una regla de alerta de ASTROGUARD. [F18](https://ntrs.nasa.gov/citations/20210019591)

Siguen siendo preguntas pertinentes: qué carga gravitatoria y ejercicio se necesitan para cada sistema corporal; cómo se acumulan los efectos de tránsito y estancia en superficie; cómo cambia la respuesta individual; y qué seguimiento será factible con menos recursos. No es válido trasladar directamente una tasa observada en órbita a la Luna o Marte.

## Cuándo pueden importar los riesgos

| Momento | Aspectos a vigilar según protocolos | Contexto que conviene conservar |
| --- | --- | --- |
| Ingreso a microgravedad | Adaptación sensoriomotora, síntomas y redistribución de líquidos. | Inicio de exposición y cambio reciente de entorno. |
| Estancia prolongada | Aptitud física, seguimiento óseo, visual y cardiovascular; bienestar y descanso. | Duración, actividad, evaluaciones y calidad de las mediciones. |
| Aterrizaje o transición de gravedad | Equilibrio, locomoción y tolerancia cardiovascular para tareas críticas. | Transición concreta y proximidad a tareas exigentes. |
| Seguimiento posterior | Recuperación funcional y posibles cambios persistentes. | Tiempo desde el retorno y resultados longitudinales. |

Esta organización es una síntesis de diseño basada en F03, F04, F14, F15 y F16; no es un calendario clínico ni una predicción individual de aparición de síntomas.

## Priorización para ASTROGUARD

| Nivel propuesto | Función | Qué aporta y qué exige |
| --- | --- | --- |
| MVP | Identificar fase de misión y procedencia del registro. | Contexto para interpretar; no implica medir automáticamente la gravedad. |
| MVP | Medición e historial de indicadores disponibles. | Permite ver cambios, ausencias y antigüedad; requiere unidades y persistencia verificadas. |
| MVP | Autoinforme de fatiga, descanso y síntomas. | Complementa mediciones; no equivale a diagnóstico ni prueba funcional validada. |
| MVP | Explicaciones por indicador y límites. | Ayuda a comprender qué puede y qué no puede mostrar el panel. |
| Ampliación | Seguimiento de rutinas prescritas y resultados clínicos importados. | Exige protocolo, permisos y trazabilidad. |
| Investigación futura | Integración con equipos especializados y evaluación de desempeño. | Exige validación del dispositivo y del análisis en condiciones relevantes. |

El documento de 48 horas sigue siendo la referencia de alcance. Los riesgos descritos justifican investigar; no obligan a construir un detector distinto para cada enfermedad. El siguiente paso es revisar esta matriz con un especialista y elegir datos que el equipo realmente pueda obtener.

## Mensajes utilizables en la presentación

**Mensaje del problema:** «En microgravedad, el cuerpo cambia su forma de sostenerse, mover líquidos y orientarse. Algunos efectos requieren seguimiento durante la misión y después del regreso».

**Dato con contexto:** «En una cohorte de 17 astronautas, nueve no habían recuperado completamente la densidad mineral ósea total de la tibia al año del retorno». Citar F14 y conservar población, sitio anatómico y plazo; evitar convertirlo en un porcentaje universal o en daño permanente.

**Vínculo con el proyecto:** «ASTROGUARD propone organizar indicadores, síntomas y contexto de misión para facilitar un seguimiento comprensible. Los riesgos que requieren pruebas especializadas se identifican como tales».

No afirmar que la aplicación mide pérdida ósea, diagnostica SANS, evita trombos o determina seguridad de una transición gravitatoria a partir de signos vitales. Tampoco afirmar que la gravedad parcial sea suficiente o insuficiente para toda persona con certeza cuantificada.

## Verificación y próximos pasos

Se verificaron el denominador y plazo del dato óseo en el artículo original. Las referencias se enlazan junto a los hallazgos y se registraron las limitaciones de extrapolación. No se estimaron incidencias conjuntas ni puntajes de riesgo individuales.

Para avanzar: obtener revisión de medicina aeroespacial; seleccionar indicadores y síntomas con definiciones claras; documentar qué sensores o entradas existen; y evaluar si el usuario distingue un cambio descriptivo de una conclusión médica. La revisión no valida el prototipo ni sustituye protocolos de misión.
