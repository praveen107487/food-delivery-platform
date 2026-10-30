const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
  throw new Error(
    "VITE_API_BASE_URL is not configured. Check your frontend .env file.",
  );
}

const env = {
  apiBaseUrl: API_BASE_URL,
  appName: import.meta.env.VITE_APP_NAME || "Food Delivery Platform",
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
};

export default env;
