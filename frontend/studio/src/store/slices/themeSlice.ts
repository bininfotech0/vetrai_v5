import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ThemeColors {
  primary: string;
  secondary: string;
  background: string;
  foreground: string;
}

interface ThemeState {
  currentTheme: string;
  colors: ThemeColors;
  customCss: string;
  logo?: string;
  loading: boolean;
}

const initialState: ThemeState = {
  currentTheme: 'default',
  colors: {
    primary: '221.2 83.2% 53.3%',
    secondary: '210 40% 96%',
    background: '0 0% 100%',
    foreground: '222.2 84% 4.9%',
  },
  customCss: '',
  loading: false,
};

const themeSlice = createSlice({
  name: 'theme',
  initialState,
  reducers: {
    setTheme: (state, action: PayloadAction<string>) => {
      state.currentTheme = action.payload;
    },
    setColors: (state, action: PayloadAction<ThemeColors>) => {
      state.colors = action.payload;
    },
    setCustomCss: (state, action: PayloadAction<string>) => {
      state.customCss = action.payload;
    },
    setLogo: (state, action: PayloadAction<string | undefined>) => {
      state.logo = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
  },
});

export const { setTheme, setColors, setCustomCss, setLogo, setLoading } = themeSlice.actions;
export default themeSlice.reducer;