import "@fontsource-variable/inter";
import "../design-system/tokens.css";
import "../design-system/base.css";
import "../design-system/theme.css";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { AppShell } from "../layouts/AppShell";
import { DashboardPage } from "../features/dashboard/DashboardPage";
import { RecordPage } from "../features/observations/RecordPage";
import { HistoryPage } from "../features/history/HistoryPage";
import { EducationPage } from "../features/education/EducationPage";
import { GalleryPage } from "../features/gallery/GalleryPage";
import { EmptyState } from "../design-system/components";
import { MissionProvider } from "./state";

const router = createBrowserRouter([
  {
    element: <AppShell />,
    children: [
      { path: "/", element: <DashboardPage /> },
      { path: "/registrar", element: <RecordPage /> },
      { path: "/historial", element: <HistoryPage /> },
      { path: "/aprender", element: <EducationPage /> },
      { path: "/componentes", element: <GalleryPage /> },
      { path: "*", element: <EmptyState title="Página no encontrada">Usa la navegación para volver.</EmptyState> },
    ],
  },
]);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <MissionProvider>
      <RouterProvider router={router} />
    </MissionProvider>
  </StrictMode>,
);
