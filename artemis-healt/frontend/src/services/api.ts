import type {
  ApiErrorBody,
  Comparison,
  Dashboard,
  EducationCard,
  Indicator,
  IndicatorKey,
  NewObservation,
  Observation,
  ObservationQuery,
  Profile,
  SaveResult,
} from "./types";

/** Contract from docs/architecture.md. Components depend only on this interface. */
export interface ArtemisApi {
  readonly mode: "mock" | "http";
  listProfiles(): Promise<Profile[]>;
  listIndicators(): Promise<Indicator[]>;
  getDashboard(profileId: string, at: string): Promise<Dashboard>;
  createObservation(input: NewObservation): Promise<SaveResult>;
  listObservations(profileId: string, query?: ObservationQuery): Promise<Observation[]>;
  getComparison(profileId: string, indicator: IndicatorKey, at: string): Promise<Comparison>;
  getEducation(indicator: IndicatorKey): Promise<EducationCard>;
}

export class ApiError extends Error {
  constructor(
    readonly status: number,
    readonly body: ApiErrorBody,
  ) {
    super(body.message);
  }
  /** Network failure or server unavailable (status 0 or 5xx). */
  get unavailable() {
    return this.status === 0 || this.status >= 500;
  }
}
