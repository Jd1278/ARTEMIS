import type { ReactElement } from "react";
import {
  BatteryMedium,
  BookOpenText,
  CaretDown,
  CaretLeft,
  CaretRight,
  ChartLineUp,
  Heartbeat,
  MoonStars,
  Pause,
  Play,
  Planet,
  PlusCircle,
  Waves,
  X,
  type Icon as PhosphorIcon,
} from "@phosphor-icons/react";
import type { IndicatorKey } from "../services/types";
import logo from "../assets/logo.png";
import logo2x from "../assets/logo@2x.png";

// Phosphor icons (MIT), duotone weight by default. Decorative: callers provide the visible text label.
type P = { size?: number; className?: string };

const wrap =
  (Icon: PhosphorIcon, weight: "duotone" | "fill" | "bold" = "duotone") =>
  ({ size = 24, className }: P) => <Icon size={size} weight={weight} className={className} aria-hidden="true" focusable="false" />;

export const IconSleep = wrap(MoonStars);
export const IconFatigue = wrap(BatteryMedium);
export const IconStress = wrap(Waves);
export const IconPulse = wrap(Heartbeat);
export const IconHome = wrap(Planet);
export const IconAdd = wrap(PlusCircle);
export const IconHistory = wrap(ChartLineUp);
export const IconLearn = wrap(BookOpenText);
export const IconPlay = wrap(Play, "fill");
export const IconPause = wrap(Pause, "fill");
export const IconClose = wrap(X, "bold");
export const IconChevron = ({ dir = "right", ...p }: P & { dir?: "left" | "right" | "down" }) => {
  const C = dir === "left" ? CaretLeft : dir === "down" ? CaretDown : CaretRight;
  return wrap(C, "bold")(p);
};

export const INDICATOR_ICON: Record<IndicatorKey, (p: P) => ReactElement> = {
  sleep_duration_h: IconSleep,
  samn_perelli: IconFatigue,
  stress_vas: IconStress,
  resting_hr_bpm: IconPulse,
};

/** Project logo (team artwork, src/assets/logo.png). Decorative: the product name is always shown next to it. */
export function Logo({ size = 40 }: { size?: number }) {
  return <img src={logo} srcSet={`${logo} 1x, ${logo2x} 2x`} width={size} height={size} alt="" className="logo" decoding="async" />;
}
