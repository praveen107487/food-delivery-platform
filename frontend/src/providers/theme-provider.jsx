import { useCallback, useEffect, useMemo, useState } from "react";

import ThemeContext from "@/contexts/theme-context";

const THEME_STORAGE_KEY = "food_delivery_theme";

function getInitialTheme() {
  const savedTheme = localStorage.getItem(THEME_STORAGE_KEY);

  return savedTheme === "dark" ? "dark" : "light";
}

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(getInitialTheme);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);

    localStorage.setItem(THEME_STORAGE_KEY, theme);
  }, [theme]);

  const toggleTheme = useCallback(() => {
    setTheme((currentTheme) => (currentTheme === "light" ? "dark" : "light"));
  }, []);

  const changeTheme = useCallback((newTheme) => {
    if (newTheme !== "light" && newTheme !== "dark") {
      throw new Error("Theme must be either light or dark.");
    }

    setTheme(newTheme);
  }, []);

  const value = useMemo(
    () => ({
      theme,
      isDarkMode: theme === "dark",
      toggleTheme,
      changeTheme,
    }),
    [theme, toggleTheme, changeTheme],
  );

  return (
    <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
  );
}

export default ThemeProvider;
