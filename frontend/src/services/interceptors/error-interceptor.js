import ApiError from "@/services/errors/api-error";

function errorInterceptor(error) {
  // Ignore intentionally cancelled requests.
  if (error.code === "ERR_CANCELED") {
    return Promise.reject(error);
  }

  // Handle request timeout.
  if (error.code === "ECONNABORTED" || error.code === "ETIMEDOUT") {
    const apiError = new ApiError({
      code: "TIMEOUT_ERROR",
      message: "The request timed out. Please try again.",
    });

    if (import.meta.env.DEV) {
      console.error("[API Timeout Error]", error);
    }

    return Promise.reject(apiError);
  }

  // Handle network errors or unavailable backend.
  if (!error.response) {
    const apiError = new ApiError({
      code: "NETWORK_ERROR",
      message: "Unable to connect to the server. Please try again.",
    });

    if (import.meta.env.DEV) {
      console.error("[API Network Error]", error);
    }

    return Promise.reject(apiError);
  }

  const { status, data } = error.response;

  // Support both the documented FastAPI format and
  // a standardized API error response format.
  const detail = data?.detail;

  let message = data?.message;

  if (!message && typeof detail === "string") {
    message = detail;
  }

  if (!message && Array.isArray(detail)) {
    message = "Please check the submitted information.";
  }

  if (!message) {
    message = "Something went wrong. Please try again.";
  }

  const apiError = new ApiError({
    code: data?.code ?? `HTTP_${status}`,
    message,
    details: data?.details ?? (Array.isArray(detail) ? detail : null),
    status,
    traceId: data?.traceId ?? data?.trace_id ?? null,
  });

  if (import.meta.env.DEV) {
    console.error("[API Error]", {
      status,
      code: apiError.code,
      message: apiError.message,
      details: apiError.details,
      traceId: apiError.traceId,
    });
  }

  return Promise.reject(apiError);
}

export default errorInterceptor;
