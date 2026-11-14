import { INDICATOR_BY_KEY } from "./domain";
import type { IndicatorKey } from "./types";

const numberFmt = new Intl.NumberFormat("es-MX", { maximumFractionDigits: 2 });
const dateFmt = new Intl.DateTimeFormat("es-MX", { day: "2-digit", month: "short", year: "numeric", timeZone: "UTC" });
const dateTimeFmt = new Intl.DateTimeFormat("es-MX", { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit", timeZone: "UTC" });

export const formatNumber = (n: number) => numberFmt.format(n);
export const formatDate = (iso: string) => dateFmt.format(new Date(iso));
export const formatDateTime = (iso: string) => `${dateTimeFmt.format(new Date(iso))} UTC`;

export function formatValue(indicator: IndicatorKey, value: number | null): string {
  if (value === null) return "—";
  return `${formatNumber(value)} ${INDICATOR_BY_KEY[indicator].unit_label.split(" ")[0]}`;
}

/** Signed difference in the indicator's own units ("puntos", never %). */
export function formatDifference(indicator: IndicatorKey, diff: number): string {
  const unit = INDICATOR_BY_KEY[indicator].difference_unit;
  if (Math.abs(diff) < 1e-9) return `0 ${unit}: igual que la mediana`;
  const sign = diff > 0 ? "+" : "−";
  return `${sign}${formatNumber(Math.abs(diff))} ${unit} ${diff > 0 ? "por encima de" : "por debajo de"} la mediana`;
}
