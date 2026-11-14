-- Apply once through scripts/database.py migrate or Supabase migration tooling.
-- Private schema: never add artemis to the Supabase Data API exposed schemas.
CREATE SCHEMA artemis;
REVOKE ALL ON SCHEMA artemis FROM PUBLIC;
CREATE TABLE artemis.schema_migrations (
 version text PRIMARY KEY, checksum text NOT NULL,
 applied_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE artemis.profiles (
 id text PRIMARY KEY, display_name text NOT NULL,
 namespace text NOT NULL DEFAULT 'demo' CHECK (namespace IN ('demo','research')),
 created_at timestamptz NOT NULL DEFAULT now(), UNIQUE(id,namespace)
);
CREATE TABLE artemis.indicators (
 key text PRIMARY KEY, label text NOT NULL, unit text NOT NULL,
 context text NOT NULL, minimum numeric, maximum numeric,
 integer_only boolean NOT NULL DEFAULT false,
 UNIQUE(key,unit,context)
);
INSERT INTO artemis.indicators VALUES
 ('sleep_duration_h','Duración del sueño','h','sleep_report',0,24,false),
 ('samn_perelli','Fatiga percibida','points_1_7','fatigue_report',1,7,true),
 ('stress_vas','Estrés percibido','points_0_100','stress_report',0,100,false),
 ('resting_hr_bpm','Pulso en reposo','bpm','rest',0,NULL,false);
CREATE TABLE artemis.import_batches (
 id text PRIMARY KEY, source_file text NOT NULL, source_sha256 text NOT NULL,
 output_sha256 text NOT NULL, transform_version text NOT NULL,
 row_count integer NOT NULL CHECK(row_count>=0),
 manifest jsonb NOT NULL, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE artemis.observations (
 id uuid PRIMARY KEY, profile_id text NOT NULL, namespace text NOT NULL,
 indicator text NOT NULL, value numeric, source_value numeric,
 unit text NOT NULL, context text NOT NULL, measured_at timestamptz NOT NULL,
 mission_day integer, origin_type text NOT NULL
 CHECK(origin_type IN ('synthetic','user_report','public_dataset')),
 capture_method text NOT NULL CHECK(capture_method IN ('import','manual','sensor')),
 quality_flags jsonb NOT NULL DEFAULT '["ok"]'::jsonb,
 source_file text, source_row integer CHECK(source_row>=2),
 import_batch_id text REFERENCES artemis.import_batches(id),
 created_at timestamptz NOT NULL DEFAULT now(),
 FOREIGN KEY(profile_id,namespace) REFERENCES artemis.profiles(id,namespace),
 FOREIGN KEY(indicator,unit,context) REFERENCES artemis.indicators(key,unit,context),
 CHECK(jsonb_typeof(quality_flags)='array'),
 CHECK(value IS NULL OR value::text NOT IN ('NaN','Infinity','-Infinity')),
 CHECK(source_value IS NULL OR source_value::text NOT IN ('NaN','Infinity','-Infinity')),
 CHECK((origin_type='public_dataset' AND namespace='research') OR
       (origin_type IN ('synthetic','user_report') AND namespace='demo')),
 CHECK(capture_method!='import' OR import_batch_id IS NOT NULL),
 CHECK(origin_type!='user_report' OR value IS NOT NULL)
);
CREATE INDEX observations_history ON artemis.observations
 (profile_id,indicator,origin_type,context,measured_at DESC);
CREATE FUNCTION artemis.validate_observation() RETURNS trigger
 LANGUAGE plpgsql SET search_path=pg_catalog,artemis AS $$
DECLARE definition artemis.indicators%ROWTYPE;
BEGIN
 SELECT * INTO definition FROM artemis.indicators WHERE key=NEW.indicator;
 IF NEW.value IS NOT NULL THEN
  IF NEW.value < definition.minimum OR NEW.value > definition.maximum
     OR (definition.integer_only AND NEW.value <> trunc(NEW.value))
     OR (NEW.indicator='resting_hr_bpm' AND NEW.value<=0) THEN
   RAISE EXCEPTION 'Value outside technical domain' USING ERRCODE='23514';
  END IF;
  IF EXISTS(SELECT 1 FROM jsonb_array_elements_text(NEW.quality_flags) f
     WHERE f LIKE '%\_imputed' ESCAPE '\' OR f LIKE '%\_out_of_range' ESCAPE '\') THEN
   RAISE EXCEPTION 'Excluded quality flag requires null value' USING ERRCODE='23514';
  END IF;
 END IF;
 RETURN NEW;
END $$;
CREATE TRIGGER observation_domain BEFORE INSERT OR UPDATE ON artemis.observations
 FOR EACH ROW EXECUTE FUNCTION artemis.validate_observation();
CREATE TABLE artemis.rule_versions (
 version text PRIMARY KEY, configuration jsonb NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now()
);
INSERT INTO artemis.rule_versions VALUES ('baseline_v1',
 '{"window_days":30,"max_days":14,"minimum_days":7,"exclude_current_day":true,"exclude_imputed":true}',now());
CREATE TABLE artemis.notices (
 id uuid PRIMARY KEY, observation_id uuid NOT NULL REFERENCES artemis.observations(id),
 rule_version text NOT NULL REFERENCES artemis.rule_versions(version),
 baseline numeric, difference numeric, baseline_count integer NOT NULL CHECK(baseline_count>=0),
 explanation text NOT NULL, reference_observation_ids jsonb NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now(), UNIQUE(observation_id,rule_version)
);
-- API clients have no access. Backend role privileges are explicit.
DO $$ BEGIN
 IF NOT EXISTS(SELECT 1 FROM pg_roles WHERE rolname='artemis_backend') THEN
  CREATE ROLE artemis_backend NOLOGIN;
 END IF;
END $$;
GRANT USAGE ON SCHEMA artemis TO artemis_backend;
GRANT SELECT ON artemis.profiles,artemis.indicators,artemis.rule_versions TO artemis_backend;
GRANT SELECT,INSERT ON artemis.observations,artemis.notices TO artemis_backend;
ALTER TABLE artemis.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE artemis.indicators ENABLE ROW LEVEL SECURITY;
ALTER TABLE artemis.observations ENABLE ROW LEVEL SECURITY;
ALTER TABLE artemis.import_batches ENABLE ROW LEVEL SECURITY;
ALTER TABLE artemis.notices ENABLE ROW LEVEL SECURITY;
ALTER TABLE artemis.rule_versions ENABLE ROW LEVEL SECURITY;
ALTER TABLE artemis.schema_migrations ENABLE ROW LEVEL SECURITY;
CREATE POLICY backend_read ON artemis.profiles FOR SELECT TO artemis_backend USING(true);
CREATE POLICY backend_read ON artemis.indicators FOR SELECT TO artemis_backend USING(true);
CREATE POLICY backend_read ON artemis.rule_versions FOR SELECT TO artemis_backend USING(true);
CREATE POLICY backend_read ON artemis.observations FOR SELECT TO artemis_backend USING(namespace='demo');
CREATE POLICY backend_insert ON artemis.observations FOR INSERT TO artemis_backend
 WITH CHECK(namespace='demo' AND origin_type='user_report' AND capture_method='manual' AND import_batch_id IS NULL);
CREATE POLICY backend_read ON artemis.notices FOR SELECT TO artemis_backend
 USING(EXISTS(SELECT 1 FROM artemis.observations o WHERE o.id=observation_id AND o.namespace='demo'));
CREATE POLICY backend_insert ON artemis.notices FOR INSERT TO artemis_backend
 WITH CHECK(EXISTS(SELECT 1 FROM artemis.observations o WHERE o.id=observation_id AND o.namespace='demo'));
REVOKE ALL ON ALL TABLES IN SCHEMA artemis FROM PUBLIC,anon,authenticated;
REVOKE ALL ON ALL FUNCTIONS IN SCHEMA artemis FROM PUBLIC,anon,authenticated;
