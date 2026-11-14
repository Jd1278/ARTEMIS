-- Migration 002: Complete ARTEMIS HEALTH schema, check-ins, educational content,
-- research dataset catalog, quality flags, and Row-Level Security (RLS) policies.
-- Keeps full compatibility with 001_initial.sql and packaged demo seed.

ALTER TABLE artemis.profiles
  ADD COLUMN IF NOT EXISTS profile_uuid uuid NOT NULL DEFAULT gen_random_uuid(),
  ADD COLUMN IF NOT EXISTS alias text NOT NULL DEFAULT 'Perfil Ficticio DEMO',
  ADD COLUMN IF NOT EXISTS profile_type text NOT NULL DEFAULT 'fictional_astronaut'
    CHECK (profile_type IN ('fictional_astronaut', 'demo_astronaut', 'research_subject', 'analog_subject')),
  ADD COLUMN IF NOT EXISTS role text NOT NULL DEFAULT 'Crew Member',
  ADD COLUMN IF NOT EXISTS mission text NOT NULL DEFAULT 'SIM-ISS-180',
  ADD COLUMN IF NOT EXISTS updated_at timestamptz NOT NULL DEFAULT now();

CREATE UNIQUE INDEX IF NOT EXISTS profiles_uuid_idx ON artemis.profiles(profile_uuid);

-- Enrich indicators with canonical aliases and descriptions while preserving 001_initial keys
ALTER TABLE artemis.indicators
  ADD COLUMN IF NOT EXISTS description text NOT NULL DEFAULT '';

INSERT INTO artemis.indicators (key, label, unit, context, minimum, maximum, integer_only, description)
VALUES
  ('fatigue', 'Fatiga percibida (escala 1-5)', 'scale_1_5', 'fatigue_report', 1, 5, true,
   'Autoinforme subjetivo de fatiga en escala discreta de 1 (alerta) a 5 (fatiga elevada).'),
  ('perceived_stress', 'Estrés percibido (escala 1-5)', 'scale_1_5', 'stress_report', 1, 5, true,
   'Autoinforme subjetivo de carga o tensión percibida en escala discreta de 1 (bajo) a 5 (alto).')
ON CONFLICT (key) DO NOTHING;

UPDATE artemis.indicators SET
  maximum = 250,
  description = 'Frecuencia cardíaca matutina medida en reposo (latidos por minuto). Indicador descriptivo no diagnóstico.'
WHERE key = 'resting_hr_bpm';

UPDATE artemis.indicators SET
  description = 'Horas totales de sueño autoinformadas en el ciclo diario de misión (0 a 24 h).'
WHERE key = 'sleep_duration_h';

UPDATE artemis.indicators SET
  description = 'Escala subjetiva de fatiga de Samn-Perelli (1 = totalmente alerta, 7 = completamente agotado).'
WHERE key = 'samn_perelli';

UPDATE artemis.indicators SET
  description = 'Escala visual analógica (VAS 0-100 puntos) de estrés percibido autoinformado.'
WHERE key = 'stress_vas';

-- Add source_reference and primary quality_flag column to observations
ALTER TABLE artemis.observations
  ADD COLUMN IF NOT EXISTS source_reference text,
  ADD COLUMN IF NOT EXISTS quality_flag text NOT NULL DEFAULT 'ok'
    CHECK (quality_flag IN ('ok', 'missing', 'imputed', 'stale', 'incompatible', 'pending_review', 'out_of_range'));

-- Populate default profiles with fictional astronaut metadata
INSERT INTO artemis.profiles (id, profile_uuid, display_name, alias, profile_type, role, mission, namespace)
VALUES
  ('demo', '00000000-0000-5000-8000-000000000000', 'Cmdr. Vega (DEMO)', 'Cmdr. Alex Vega (SIMULADO)', 'fictional_astronaut', 'Commander', 'SIM-ISS-180', 'demo'),
  ('CM-01', '00000000-0000-5000-8000-000000000001', 'CM-01 Commander', 'Cmdr. Alex Vega (CM-01)', 'fictional_astronaut', 'Commander', 'SIM-ISS-180', 'demo'),
  ('CM-02', '00000000-0000-5000-8000-000000000002', 'CM-02 Flight Engineer 1', 'Ing. Elena Rostova (CM-02)', 'fictional_astronaut', 'Flight Engineer 1', 'SIM-ISS-180', 'demo'),
  ('CM-03', '00000000-0000-5000-8000-000000000003', 'CM-03 Flight Engineer 2', 'Ing. Mateo Silva (CM-03)', 'fictional_astronaut', 'Flight Engineer 2', 'SIM-ISS-180', 'demo'),
  ('CM-04', '00000000-0000-5000-8000-000000000004', 'CM-04 Flight Engineer 3', 'Ing. Sora Takahashi (CM-04)', 'fictional_astronaut', 'Flight Engineer 3', 'SIM-ISS-180', 'demo'),
  ('CM-05', '00000000-0000-5000-8000-000000000005', 'CM-05 Science Officer', 'Of. Científico Liam O''Connor (CM-05)', 'fictional_astronaut', 'Science Officer', 'SIM-ISS-180', 'demo'),
  ('CM-06', '00000000-0000-5000-8000-000000000006', 'CM-06 Medical Officer', 'Of. Médico Amara Okafor (CM-06)', 'fictional_astronaut', 'Medical Officer', 'SIM-ISS-180', 'demo')
ON CONFLICT (id) DO UPDATE SET
  alias = EXCLUDED.alias,
  profile_type = EXCLUDED.profile_type,
  role = EXCLUDED.role,
  mission = EXCLUDED.mission,
  updated_at = now();

-- Check-ins table (daily wellness self-report: fatigue 1-5, perceived_stress 1-5, non-identifiable notes)
CREATE TABLE IF NOT EXISTS artemis.checkins (
  id uuid PRIMARY KEY,
  profile_id text NOT NULL,
  namespace text NOT NULL DEFAULT 'demo' CHECK (namespace = 'demo'),
  checkin_date date NOT NULL,
  fatigue integer NOT NULL CHECK (fatigue BETWEEN 1 AND 5),
  perceived_stress integer NOT NULL CHECK (perceived_stress BETWEEN 1 AND 5),
  notes text CHECK (notes IS NULL OR char_length(notes) <= 500),
  origin_type text NOT NULL DEFAULT 'user_report' CHECK (origin_type IN ('synthetic', 'user_report')),
  capture_method text NOT NULL DEFAULT 'manual' CHECK (capture_method IN ('manual', 'sensor', 'import')),
  quality_flag text NOT NULL DEFAULT 'ok' CHECK (quality_flag IN ('ok', 'missing', 'imputed', 'stale', 'incompatible', 'pending_review')),
  created_at timestamptz NOT NULL DEFAULT now(),
  FOREIGN KEY (profile_id, namespace) REFERENCES artemis.profiles(id, namespace)
);

CREATE INDEX IF NOT EXISTS checkins_profile_date_idx
  ON artemis.checkins (profile_id, checkin_date DESC, created_at DESC);

-- Educational content table
CREATE TABLE IF NOT EXISTS artemis.educational_content (
  id uuid PRIMARY KEY,
  indicator text NOT NULL UNIQUE,
  title text NOT NULL,
  description text NOT NULL,
  unit text NOT NULL,
  limitations text NOT NULL,
  bibliographic_reference text NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO artemis.educational_content (id, indicator, title, description, unit, limitations, bibliographic_reference)
VALUES
  ('10000000-0000-4000-8000-000000000001', 'resting_hr_bpm',
   'Frecuencia cardíaca en reposo',
   'Mide los latidos por minuto en condición de reposo matutino. Permite observar la variación individual frente a la línea base personal durante las fases de adaptación y misión.',
   'bpm',
   'No constituye un diagnóstico cardiológico ni sustituye un electrocardiograma clínico. Factores como hidratación, ciclo circadiano, actividad previa y microgravedad modifican el valor sin implicar patología.',
   'American Heart Association (AHA) Target Heart Rates & NASA Human Research Program (HRP) Standard Measures.'),
  ('10000000-0000-4000-8000-000000000002', 'sleep_duration_h',
   'Duración del sueño',
   'Registra el tiempo total de descanso autoinformado o medido por actigrafía en cada ciclo de 24 horas. El seguimiento longitudinal ayuda a identificar variaciones en los horarios de descanso de la tripulación.',
   'h',
   'El autoinforme de sueño puede diferir de la polisomnografía y no evalúa arquitectura de fases del sueño ni trastornos clínicos del sueño.',
   'Barger LK et al. (2014). Prevalence of sleep deficiency and use of hypnotic drugs in astronauts before, during, and after spaceflight. The Lancet Neurology, 13(9), 904-912. doi:10.1016/S1474-4422(14)70122-X.'),
  ('10000000-0000-4000-8000-000000000003', 'fatigue',
   'Fatiga percibida',
   'Registra la percepción subjetiva de cansancio o alerta al inicio de la jornada (escala de seguimiento 1-5 en check-in rápido y escala Samn-Perelli 1-7 en bitácora operativa).',
   'escala 1-5 / puntos 1-7',
   'Es una medida autoinformada sujeta a sesgo de percepción individual. No mide desempeño psicomotor objetivo ni sustituye pruebas como PVT-B ni evaluaciones médicas.',
   'Samn SW, Perelli LP (1982). Estimating Aircrew Fatigue: A Technique with Application to Airlift Operations. USAF School of Aerospace Medicine, Technical Report SAM-TR-82-21.'),
  ('10000000-0000-4000-8000-000000000004', 'perceived_stress',
   'Estrés percibido',
   'Evalúa la tensión subjetiva percibida frente a la carga operativa, el aislamiento y los cambios de cronograma (escala 1-5 en check-in diario y escala visual analógica VAS 0-100 en registro extendido).',
   'escala 1-5 / puntos 0-100',
   'Representa una apreciación subjetiva momentánea expresada en puntos, no un porcentaje clínico ni un diagnóstico psicológico o psiquiátrico.',
   'Jones CW et al. (2022). Sleep deficiency in spaceflight is associated with degraded neurobehavioral functions and elevated stress in astronauts on six-month missions aboard the ISS. SLEEP, 45(3). https://pmc.ncbi.nlm.nih.gov/articles/PMC8919197')
ON CONFLICT (indicator) DO NOTHING;

-- Research datasets catalog table (isolated in namespace = 'research')
CREATE TABLE IF NOT EXISTS artemis.research_datasets (
  id uuid PRIMARY KEY,
  dataset_key text NOT NULL UNIQUE,
  file_name text NOT NULL UNIQUE,
  title text NOT NULL,
  namespace text NOT NULL DEFAULT 'research' CHECK (namespace IN ('research', 'demo_audit')),
  origin_type text NOT NULL CHECK (origin_type IN ('public_dataset', 'synthetic')),
  capture_method text NOT NULL CHECK (capture_method IN ('import', 'sensor', 'manual')),
  study_context text NOT NULL,
  is_inflight_measurement boolean NOT NULL DEFAULT false,
  is_personal_radiation_dose boolean NOT NULL DEFAULT false,
  included_in_personal_calculations boolean NOT NULL DEFAULT false CHECK (included_in_personal_calculations = false),
  row_count integer NOT NULL CHECK (row_count >= 0),
  sha256 text NOT NULL,
  limitations text NOT NULL,
  source_reference text NOT NULL,
  quality_flag text NOT NULL DEFAULT 'ok',
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Enable RLS and grant explicit permissions to artemis_backend
GRANT SELECT, INSERT, UPDATE ON artemis.profiles TO artemis_backend;
GRANT SELECT, INSERT ON artemis.checkins TO artemis_backend;
GRANT SELECT ON artemis.educational_content, artemis.research_datasets TO artemis_backend;

ALTER TABLE artemis.checkins ENABLE ROW LEVEL SECURITY;
ALTER TABLE artemis.educational_content ENABLE ROW LEVEL SECURITY;
ALTER TABLE artemis.research_datasets ENABLE ROW LEVEL SECURITY;

CREATE POLICY backend_read_checkins ON artemis.checkins
  FOR SELECT TO artemis_backend USING (namespace = 'demo');

CREATE POLICY backend_insert_checkins ON artemis.checkins
  FOR INSERT TO artemis_backend
  WITH CHECK (namespace = 'demo' AND origin_type IN ('user_report', 'synthetic'));

CREATE POLICY backend_read_education ON artemis.educational_content
  FOR SELECT TO artemis_backend USING (true);

CREATE POLICY backend_read_research ON artemis.research_datasets
  FOR SELECT TO artemis_backend USING (true);

REVOKE ALL ON artemis.checkins, artemis.educational_content, artemis.research_datasets FROM PUBLIC, anon, authenticated;
