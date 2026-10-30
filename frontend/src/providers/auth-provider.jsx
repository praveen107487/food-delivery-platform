import { useCallback, useEffect, useMemo, useState } from "react";
import AuthContext from "@/contexts/auth-context";
import authService from "@/services/auth/auth-service";
import {
  hasAccessToken,
  removeAccessToken,
} from "@/services/auth/token-storage";

function AuthProvider({ children }) {
  const [customer, setCustomer] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Restore the authenticated customer when the app starts.
  useEffect(() => {
    let isMounted = true;

    async function initializeAuth() {
      if (!hasAccessToken()) {
        if (isMounted) {
          setIsLoading(false);
        }
        return;
      }

      try {
        const currentCustomer = await authService.getCurrentCustomer();

        if (isMounted) {
          setCustomer(currentCustomer);
        }
      } catch {
        removeAccessToken();

        if (isMounted) {
          setCustomer(null);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    initializeAuth();

    return () => {
      isMounted = false;
    };
  }, []);

  // Authenticate the customer.
  const login = useCallback(async (credentials) => {
    const response = await authService.login(credentials);

    setCustomer(response.customer ?? null);

    return response;
  }, []);

  // Register a new customer.
  const register = useCallback(async (customerData) => {
    return authService.register(customerData);
  }, []);

  // Clear the current authentication session.
  const logout = useCallback(() => {
    authService.logout();
    setCustomer(null);
  }, []);

  // Update customer information in the shared state.
  const updateCustomer = useCallback((updatedCustomer) => {
    setCustomer(updatedCustomer);
  }, []);

  const value = useMemo(
    () => ({
      customer,
      isAuthenticated: Boolean(customer && hasAccessToken()),
      isLoading,
      login,
      register,
      logout,
      updateCustomer,
    }),
    [customer, isLoading, login, register, logout, updateCustomer],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export default AuthProvider;
