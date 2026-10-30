import { Toaster } from "react-hot-toast";

function ToastProvider({ children }) {
  return (
    <>
      {children}

      <Toaster
        position="top-right"
        reverseOrder={false}
        gutter={8}
        toastOptions={{
          duration: 4000,
          style: {
            background: "var(--color-surface)",
            color: "var(--color-on-surface)",
            border: "1px solid var(--color-outline)",
          },
          success: {
            duration: 3000,
          },
          error: {
            duration: 5000,
          },
        }}
      />
    </>
  );
}

export default ToastProvider;
