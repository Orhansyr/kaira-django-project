import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/components/';

export const fetchComponentBySlug = createAsyncThunk(
  'pageComponents/fetchComponentBySlug',
  async (slug, { rejectWithValue }) => {
    try {
      const response = await axios.get(`${API_URL}${slug}/`);
      return response.data;
    } catch (error) {
      if (error.response) {
        return rejectWithValue(error.response.data);
      }
      return rejectWithValue(error.message);
    }
  }
);

const pageComponentSlice = createSlice({
  name: 'pageComponents',
  initialState: {
    // We store components by slug for easy access
    components: {},
    status: 'idle',
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchComponentBySlug.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchComponentBySlug.fulfilled, (state, action) => {
        state.status = 'succeeded';
        // Add or update the component in the state
        state.components[action.payload.slug] = action.payload;
      })
      .addCase(fetchComponentBySlug.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.payload || action.error.message;
      });
  },
});

export default pageComponentSlice.reducer;
