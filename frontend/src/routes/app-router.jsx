import { createBrowserRouter } from "react-router-dom";

import App from "@/App";
import RootLayout from "@/layouts/root-layout";
import PublicLayout from "@/layouts/public-layout";
import MainLayout from "@/layouts/main-layout";
import ErrorLayout from "@/layouts/error-layout";

const router = createBrowserRouter([
  {
    element: <RootLayout />,
    errorElement: <ErrorLayout />,
    children: [
      {
        element: <PublicLayout />,
        children: [
          {
            index: true,
            element: <App />,
          },
        ],
      },
      {
        element: <MainLayout />,
        children: [],
      },
    ],
  },
]);

export default router;
