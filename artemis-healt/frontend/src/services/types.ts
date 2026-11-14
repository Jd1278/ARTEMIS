// Contract types mirrored from docs/architecture.md, docs/requirements.md and migrations/001_initial.sql.

export type IndicatorKey = "sleep_duration_h" | "samn_perelli" | "stress_vas" | "resting_hr_bpm";
export type OriginType = "synthetic" | "user_report" | "public_dataset";
export type CaptureMethod = "import" | "manual" | "sensor";
export type Namespace = "demo" | "research";

export interface Profile {
  id: string;
  display_name: string;
  role: string;
  namespace: Namespace;
}

export interface Indicator {
  key: IndicatorKey;
  label: string;
  unit: string;
  unit_label: string;
  context: string;
  minimum: number | null;
  maximum: number | null;
  /** True when the lower bound itself is invalid (pulse must be > 0). */
  exclusive_minimum: boolean;
  integer_only: boolean;
  /** Differences are expressed in these units ("h", "puntos", "lpm"). */
  difference_unit: string;
}

export interface Observation {
  id: string;
  profile_id: string;
  indicator: IndicatorKey;
  value: number | null;
  source_value: number | null;
  unit: string;
  timestamp: string; // ISO 8601 UTC
  mission_day: number | null;
  context: string;
  namespace: Namespace;
  origin_type: OriginType;
  capture_method: CaptureMethod;
  quality_flags: string[];
  source_file: string | null;
  source_row: number | null;
}

export interface NewObservation {
  id: string;
  profile_id: string;
  indicator: IndicatorKey;
  value: number;
  unit: string;
  context: string;
  timestamp: string;
  mission_day: number | null;
}

export interface DashboardItem {
  indicator: IndicatorKey;
  /** Latest observation at or before the cursor, even if its value is null (excluded). */
  latest: Observation | null;
  /** Latest observation with a usable value at or before the cursor. */
  latest_valid: Observation | null;
}

export interface Dashboard {
  profile_id: string;
  at: string;
  mission_day: number;
  items: DashboardItem[];
}

export interface Comparison {
  profile_id: string;
  indicator: IndicatorKey;
  rule_version: string;
  at: string;
  origin_type: OriginType;
  current: Observation | null;
  baseline: number | null;
  difference: number | null;
  days_used: number;
  minimum_days: number;
  period_from: string | null;
  period_to: string | null;
  sufficient: boolean;
  reference_observation_ids: string[];
  explanation: string;
}

export interface EducationCard {
  indicator: IndicatorKey;
  title: string;
  measures: string;
  how_to_record: string;
  scale: string;
  limits: string[];
  reference: { citation: string; url: string | null; review_status: string };
}

export interface ApiErrorBody {
  code: string;
  message: string;
  fields: Record<string, string>;
  request_id: string;
}

export type SaveResult = { status: 201 | 200; observation: Observation };

export interface ObservationQuery {
  indicator?: IndicatorKey;
  from?: string;
  to?: string;
}
