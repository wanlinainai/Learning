import { createSlice } from '@reduxjs/toolkit'

const userSlice = createSlice({
  name: 'user',
  initialState: {
    isLogin: false,
    userInfo: {},
  },
  reducers: {
    initUserInfo: (state, { payload }) => {
      state.userInfo = payload
    },
    changeLoginStatus: (state, { payload }) => {
      state.isLogin = true
    }
  }
})


export const { initUserInfo, changeLoginStatus } = userSlice.actions;
export default userSlice.reducer;