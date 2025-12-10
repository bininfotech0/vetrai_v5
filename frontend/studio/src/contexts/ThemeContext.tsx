import { createContext, useContext, useEffect, useState } from 'react';
import { themesApi } from '@/lib/api/themes';

interface Theme {
  id: string;
  name: string;
  colors: {
    primary: string;
    secondary: string;
    background: string;
    foreground: string;
  };
  logo?: string;
  customCss?: string;
}

interface ThemeContextType {
  theme: Theme | null;
  themes: Theme[];
  loading: boolean;
  setTheme: (theme: Theme) => void;
  refreshThemes: () => Promise<void>;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = useState<Theme | null>(null);
  const [themes, setThemes] = useState<Theme[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadThemes = async () => {
      try {
        const themesData = await themesApi.getThemes();
        setThemes(themesData);
        
        // Set organization theme or default
        const orgTheme = themesData.find(t => t.id === 'organization') || themesData[0];
        if (orgTheme) {
          setTheme(orgTheme);
        }
      } catch (error) {
        console.error('Failed to load themes:', error);
      } finally {
        setLoading(false);
      }
    };

    loadThemes();
  }, []);

  useEffect(() => {
    if (theme) {
      // Apply theme to document
      const root = document.documentElement;
      Object.entries(theme.colors).forEach(([key, value]) => {
        root.style.setProperty(`--${key}`, value);
      });

      // Apply custom CSS
      if (theme.customCss) {
        const style = document.getElementById('custom-theme-css') || document.createElement('style');
        style.id = 'custom-theme-css';
        style.textContent = theme.customCss;
        document.head.appendChild(style);
      }
    }
  }, [theme]);

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme);
    localStorage.setItem('selectedTheme', newTheme.id);
  };

  const refreshThemes = async () => {
    const themesData = await themesApi.getThemes();
    setThemes(themesData);
  };

  return (
    <ThemeContext.Provider
      value={{
        theme,
        themes,
        loading,
        setTheme,
        refreshThemes,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}