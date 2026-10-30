import { getAccessToken } from "@/services/auth/token-storage";

function requestInterceptor(config) {
  const accessToken = getAccessToken();

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  } else {
    delete config.headers.Authorization;
  }

  if (import.meta.env.DEV) {
    console.info(`[API Request] ${config.method?.toUpperCase()} ${config.url}`);
  }

  return config;
}

export default requestInterceptor;
