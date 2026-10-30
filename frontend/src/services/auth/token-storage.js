const TOKEN_STORAGE_KEY = "food_delivery_access_token";

export function getAccessToken() {
  return sessionStorage.getItem(TOKEN_STORAGE_KEY);
}

export function setAccessToken(token) {
  if (!token || typeof token !== "string") {
    throw new Error("A valid access token is required.");
  }

  sessionStorage.setItem(TOKEN_STORAGE_KEY, token);
}

export function removeAccessToken() {
  sessionStorage.removeItem(TOKEN_STORAGE_KEY);
}

export function hasAccessToken() {
  return Boolean(getAccessToken());
}
