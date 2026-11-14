import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { MISSION, missionDayCursor, PROFILES } from "../services/domain";

interface MissionState {
  profileId: string;
  setProfileId: (id: string) => void;
  missionDay: number;
  setMissionDay: (day: number | ((prev: number) => number)) => void;
  /** End-of-day UTC cursor for the selected mission day. All calculations use this, never "now". */
  at: string;
  /** Bumped after a successful save so views refetch. */
  revision: number;
  bumpRevision: () => void;
}

const MissionContext = createContext<MissionState | null>(null);

const read = (key: string) => {
  try {
    return sessionStorage.getItem(key);
  } catch {
    return null;
  }
};
const write = (key: string, value: string) => {
  try {
    sessionStorage.setItem(key, value);
  } catch {
    /* storage unavailable: state still works in memory */
  }
};

export function MissionProvider({ children }: { children: ReactNode }) {
  const [profileId, setProfileIdState] = useState(() => read("artemis.profile") ?? PROFILES[0].id);
  const [missionDay, setMissionDayState] = useState(() => {
    const d = Number(read("artemis.day"));
    return d >= 1 && d <= MISSION.days ? d : 60;
  });
  const [revision, setRevision] = useState(0);

  useEffect(() => write("artemis.profile", profileId), [profileId]);
  useEffect(() => write("artemis.day", String(missionDay)), [missionDay]);

  const setProfileId = useCallback((id: string) => setProfileIdState(id), []);
  const setMissionDay = useCallback(
    (d: number | ((prev: number) => number)) =>
      setMissionDayState((prev) => Math.min(MISSION.days, Math.max(1, Math.round(typeof d === "function" ? d(prev) : d)))),
    [],
  );
  const bumpRevision = useCallback(() => setRevision((r) => r + 1), []);

  const value = useMemo(
    () => ({ profileId, setProfileId, missionDay, setMissionDay, at: missionDayCursor(missionDay), revision, bumpRevision }),
    [profileId, setProfileId, missionDay, setMissionDay, revision, bumpRevision],
  );
  return <MissionContext.Provider value={value}>{children}</MissionContext.Provider>;
}

export function useMission() {
  const ctx = useContext(MissionContext);
  if (!ctx) throw new Error("useMission must be used inside MissionProvider");
  return ctx;
}
