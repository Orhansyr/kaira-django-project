import { configureStore } from '@reduxjs/toolkit';
import menuReducer from './slices/menuSlice';
import pageComponentReducer from './slices/pageComponentSlice';

export const makeStore = () => {
  return configureStore({
    reducer: {
      menus: menuReducer,
      pageComponents: pageComponentReducer,
    },
  });
};
