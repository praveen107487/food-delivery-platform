class ApiError extends Error {
  constructor({
    code = "UNKNOWN_ERROR",
    message = "An unexpected error occurred.",
    details = null,
    status = null,
    traceId = null,
  }) {
    super(message);

    this.name = "ApiError";
    this.code = code;
    this.details = details;
    this.status = status;
    this.traceId = traceId;
  }
}

export default ApiError;
