import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const analyzeCandidates = async (jobDescription, topN, files) => {
  const formData = new FormData();
  formData.append('job_description', jobDescription);
  formData.append('top_n', topN);

  files.forEach((file) => {
    formData.append('files', file);
  });

  try {
    const response = await axios.post(`${API_BASE_URL}/analysis`, formData);
    return response.data;
  } catch (error) {
    if (error.response) {
      // Server responded with error status
      const detail = error.response.data.detail;
      if (typeof detail === 'string') {
        throw new Error(detail);
      } else if (typeof detail === 'object') {
        throw new Error(detail.message || 'Analysis failed');
      } else {
        throw new Error('Analysis failed');
      }
    } else if (error.request) {
      // Request made but no response
      throw new Error('Unable to connect to backend server');
    } else {
      // Error in request setup
      throw new Error('An unexpected error occurred');
    }
  }
};
