import type { ArtemisApi } from "./api";
import { httpApi } from "./httpApi";
import { mockApi } from "./mockApi";

export const api: ArtemisApi = import.meta.env.VITE_API_MODE === "http" ? httpApi : mockApi;
export { ApiError } from "./api";
export type { ArtemisApi } from "./api";
