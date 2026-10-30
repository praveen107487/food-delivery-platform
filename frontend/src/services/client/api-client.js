import axios from "axios";

import env from "@/config/env";
import requestInterceptor from "@/services/interceptors/request-interceptor";
import responseInterceptor from "@/services/interceptors/response-interceptor";
import errorInterceptor from "@/services/interceptors/error-interceptor";

const apiClient = axios.create({
  baseURL: env.apiBaseUrl,
  timeout: 15000,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use(requestInterceptor, (error) =>
  Promise.reject(error),
);

apiClient.interceptors.response.use(responseInterceptor, errorInterceptor);

export default apiClient;
