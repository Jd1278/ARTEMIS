import { NavLink, Outlet, useLocation } from "react-router-dom";
import { api } from "../services";
import { MISSION } from "../services/domain";
import { IconAdd, IconHistory, IconHome, IconLearn, Logo } from "../design-system/icons";
import { SpaceBackground } from "../design-system/illustrations";
import { CrewPicker } from "./CrewPicker";
import { MissionTimeline } from "./MissionTimeline";
import "./AppShell.css";

const NAV = [
  { to: "/", label: "Resumen", Icon: IconHome },
  { to: "/registrar", label: "Registrar", Icon: IconAdd },
  { to: "/historial", label: "Historial", Icon: IconHistory },
  { to: "/aprender", label: "Aprender", Icon: IconLearn },
];

export function AppShell() {
  const location = useLocation();

  return (
    <div className="shell">
      <SpaceBackground />
      <a className="skip-link" href="#main">
        Saltar al contenido
      </a>

      <aside className="shell__side" aria-label="Navegación principal">
        <div className="brand">
          <Logo size={44} />
          <div>
            <p className="brand__name">ARTEMIS HEALTH</p>
            <p className="meta">{MISSION.name}</p>
          </div>
        </div>
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
        <p className="meta shell__mode">Datos: {api.mode === "mock" ? "demo local (sin backend)" : "API"}</p>
      </aside>

      <div className="shell__body">
        <header className="topbar">
          <div className="topbar__brand">
            <Logo size={32} />
            <strong>ARTEMIS HEALTH</strong>
          </div>
          <div className="sim-banner" role="note">
            <strong>DEMO · DATOS SIMULADOS</strong>
            <span className="meta">Tripulación ficticia. No usar con datos reales ni para decisiones médicas.</span>
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

      <nav className="bottom-nav" aria-label="Navegación principal (móvil)">
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
