import { useEffect, useState, type DependencyList } from "react";
import { ApiError } from "../services";

export type AsyncState<T> =
  | { status: "loading"; data?: T }
  | { status: "success"; data: T }
  | { status: "error"; error: ApiError; data?: T };

/** Runs an async loader on dependency change, ignoring stale responses. */
export function useAsync<T>(loader: () => Promise<T>, deps: DependencyList): AsyncState<T> {
  const [state, setState] = useState<AsyncState<T>>({ status: "loading" });
  useEffect(() => {
    let alive = true;
    setState((s) => ({ status: "loading", data: s.data }));
    loader().then(
      (data) => alive && setState({ status: "success", data }),
      (e) =>
        alive &&
        setState((s) => ({
          status: "error",
          data: s.data,
          error: e instanceof ApiError ? e : new ApiError(0, { code: "unknown", message: String(e), fields: {}, request_id: "" }),
        })),
    );
    return () => {
      alive = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
  return state;
}
