import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider } from "react-router-dom";

import QueryProvider from "@/providers/query-provider";
import ThemeProvider from "@/providers/theme-provider";
import AuthProvider from "@/providers/auth-provider";
import ToastProvider from "@/providers/toast-provider";

import router from "@/routes/app-router";

import "@/index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <QueryProvider>
      <ThemeProvider>
        <AuthProvider>
          <ToastProvider>
            <RouterProvider router={router} />
          </ToastProvider>
        </AuthProvider>
      </ThemeProvider>
    </QueryProvider>
  </StrictMode>,
);
