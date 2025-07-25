import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { getType } from "../api/type";

export const getTypeList = createAsyncThunk(
  "type/get",
  async () => {
    const response = await getType();
    return response.data;
  }
);

const typeSlice = createSlice({
  name: "type",
  initialState: {
    typeList: [],
    issueTypeId: 'all',
    bookTypeId: 'all'
  },
  reducers: {
    updateIssueTypeId: (state, { payload }) => {
      state.issueTypeId = payload
    }
  },
  extraReducers: (builder) => {
    builder.addCase(getTypeList.fulfilled, (state, action) => {
      state.typeList = action.payload;
    });
  },
});

export const { updateIssueTypeId } = typeSlice.actions;
export default typeSlice.reducer;
