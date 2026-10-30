import apiClient from "@/services/client/api-client";
import { API_ENDPOINTS } from "@/constants/api";
import {
  removeAccessToken,
  setAccessToken,
} from "@/services/auth/token-storage";

const authService = {
  /**
   * Register a new customer.
   *
   * @param {Object} customerData
   * @returns {Promise<Object>}
   */
  async register(customerData) {
    const response = await apiClient.post(
      API_ENDPOINTS.auth.register,
      customerData,
    );

    return response.data;
  },

  /**
   * Authenticate an existing customer.
   *
   * @param {Object} credentials
   * @returns {Promise<Object>}
   */
  async login(credentials) {
    const response = await apiClient.post(
      API_ENDPOINTS.auth.login,
      credentials,
    );

    const { access_token: accessToken } = response.data ?? {};

    if (!accessToken) {
      throw new Error("Login response does not contain an access token.");
    }

    setAccessToken(accessToken);

    return response.data;
  },

  /**
   * Retrieve the currently authenticated customer.
   *
   * @returns {Promise<Object>}
   */
  async getCurrentCustomer() {
    const response = await apiClient.get(API_ENDPOINTS.auth.me);

    return response.data;
  },

  /**
   * Log out the customer on the frontend.
   *
   * The backend does not currently document a logout endpoint.
   */
  logout() {
    removeAccessToken();
  },
};

export default authService;
