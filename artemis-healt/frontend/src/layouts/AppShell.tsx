import { NavLink, Outlet, useLocation } from "react-router-dom";
import { MISSION } from "../services/domain";
import { IconAdd, IconHistory, IconHome, IconLearn, Logo } from "../design-system/icons";
import { SpaceBackground } from "../design-system/illustrations";
import { CrewPicker } from "./CrewPicker";
import { MissionTimeline } from "./MissionTimeline";
import "./AppShell.css";

const NAV = [
  { to: "/", label: "Overview", Icon: IconHome },
  { to: "/log", label: "Log entry", Icon: IconAdd },
  { to: "/history", label: "History", Icon: IconHistory },
  { to: "/learn", label: "Learn", Icon: IconLearn },
];

export function AppShell() {
  const location = useLocation();

  return (
    <div className="shell">
      <SpaceBackground />
      <a className="skip-link" href="#main">
        Skip to content
      </a>

      <aside className="shell__side" aria-label="Main navigation">
        <div className="brand">
          <Logo size={44} />
          <div>
            <p className="brand__name">ARTEMIS HEALTH</p>
            <p className="meta">{MISSION.name}</p>
          </div>
        </div>
        <p className="demo-tag" title="Demo with simulated data and a fictional crew. Not for real data or medical decisions.">
          Demo · simulated data · fictional crew
        </p>
        <nav>
          <ul className="nav">
            {NAV.map(({ to, label, Icon }) => (
              <li key={to}>
                <NavLink to={to} end={to === "/"} className="nav__link">
                  <span className="nav__icon">
                    <Icon size={20} />
                  </span>
                  {label}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </aside>

      <div className="shell__body">
        <header className="topbar">
          <div className="topbar__brand">
            <Logo size={32} />
            <strong>ARTEMIS HEALTH</strong>
            <span className="demo-tag demo-tag--inline">Demo · simulated data</span>
          </div>
          <div className="controls">
            <CrewPicker />
            <MissionTimeline />
          </div>
        </header>

        <main id="main" className="shell__main" tabIndex={-1}>
          <div className="page" key={location.pathname}>
            <Outlet />
          </div>
        </main>
      </div>

      <nav className="bottom-nav" aria-label="Main navigation (mobile)">
        {NAV.map(({ to, label, Icon }) => (
          <NavLink key={to} to={to} end={to === "/"} className="bottom-nav__link">
            <Icon size={22} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
