function responseInterceptor(response) {
  if (import.meta.env.DEV) {
    console.info(`[API Response] ${response.status} ${response.config.url}`);
  }

  return response;
}

export default responseInterceptor;
