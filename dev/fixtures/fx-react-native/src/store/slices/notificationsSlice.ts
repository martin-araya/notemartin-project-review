import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

export interface NotificationState {
  token: string | null;
  permission: 'granted' | 'denied' | 'undetermined';
  scheduleId: string | null;
}

const initialState: NotificationState = {
  token: null,
  permission: 'undetermined',
  scheduleId: null,
};

const notificationsSlice = createSlice({
  name: 'notifications',
  initialState,
  reducers: {
    setToken(state, action: PayloadAction<string | null>) {
      state.token = action.payload;
    },
    setPermission(state, action: PayloadAction<NotificationState['permission']>) {
      state.permission = action.payload;
    },
    setScheduleId(state, action: PayloadAction<string | null>) {
      state.scheduleId = action.payload;
    },
  },
});

export const { setToken, setPermission, setScheduleId } = notificationsSlice.actions;
export default notificationsSlice.reducer;