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
import { RouteErrorPage } from "./RouteErrorPage";

const router = createBrowserRouter([
  {
    element: <AppShell />,
    errorElement: <RouteErrorPage />,
    children: [
      { path: "/", element: <DashboardPage /> },
      { path: "/log", element: <RecordPage /> },
      { path: "/history", element: <HistoryPage /> },
      { path: "/learn", element: <EducationPage /> },
      { path: "/components", element: <GalleryPage /> },
      {
        path: "*",
        element: (
          <>
            <div className="page-head">
              <h1>Page not found</h1>
            </div>
            <EmptyState title="This page does not exist">Use the navigation to go back.</EmptyState>
          </>
        ),
      },
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
