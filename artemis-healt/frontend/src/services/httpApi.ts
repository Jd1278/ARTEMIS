import { ApiError, type ArtemisApi } from "./api";
import type { NewObservation, ObservationQuery, SaveResult } from "./types";

async function request<T>(path: string, init?: RequestInit): Promise<{ status: number; data: T }> {
  let response: Response;
  try {
    response = await fetch(path, { headers: { "Content-Type": "application/json", Accept: "application/json" }, ...init });
  } catch {
    throw new ApiError(0, { code: "network_unavailable", message: "No se pudo contactar con el servidor.", fields: {}, request_id: "" });
  }
  const text = await response.text();
  const body = text ? JSON.parse(text) : null;
  if (!response.ok) {
    throw new ApiError(response.status, {
      code: body?.code ?? `http_${response.status}`,
      message: body?.message ?? response.statusText,
      fields: body?.fields ?? {},
      request_id: body?.request_id ?? response.headers.get("x-request-id") ?? "",
    });
  }
  return { status: response.status, data: body as T };
}

const qs = (params: Record<string, string | undefined>) => {
  const p = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) if (v) p.set(k, v);
  const s = p.toString();
  return s ? `?${s}` : "";
};

export const httpApi: ArtemisApi = {
  mode: "http",
  listProfiles: async () => (await request<never>("/api/profiles")).data,
  listIndicators: async () => (await request<never>("/api/indicators")).data,
  getDashboard: async (id, at) => (await request<never>(`/api/profiles/${encodeURIComponent(id)}/dashboard${qs({ at })}`)).data,
  async createObservation(input: NewObservation): Promise<SaveResult> {
    const { status, data } = await request<SaveResult["observation"]>("/api/observations", { method: "POST", body: JSON.stringify(input) });
    return { status: status === 201 ? 201 : 200, observation: data };
  },
  listObservations: async (id, query: ObservationQuery = {}) =>
    (await request<never>(`/api/profiles/${encodeURIComponent(id)}/observations${qs({ ...query })}`)).data,
  getComparison: async (id, indicator, at) =>
    (await request<never>(`/api/profiles/${encodeURIComponent(id)}/comparison${qs({ indicator, at })}`)).data,
  getEducation: async (indicator) => (await request<never>(`/api/education/${indicator}`)).data,
};
