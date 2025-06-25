import { ref } from 'vue'
import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';


// Login
export async function getQuizzes(lernsetID) {
  return apiClient.post(API_ENDPOINTS.LERNSETS.QUIZZES, {
  lernsetID
  });
}

