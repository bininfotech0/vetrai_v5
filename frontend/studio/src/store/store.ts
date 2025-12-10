import { configureStore } from '@reduxjs/toolkit';
import authSlice from './slices/authSlice';
import workflowSlice from './slices/workflowSlice';
import themeSlice from './slices/themeSlice';

export const store = configureStore({
  reducer: {
    auth: authSlice,
    workflow: workflowSlice,
    theme: themeSlice,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;