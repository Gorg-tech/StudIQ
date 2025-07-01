import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';

export async function getLernset(lernsetId) {
  return apiClient.get(API_ENDPOINTS.LERNSETS.DETAIL(lernsetId));
}

export async function createLernset(lernsetData) {
  return apiClient.post(API_ENDPOINTS.LERNSETS.BASE, lernsetData);
}

export async function updateLernset(lernsetId, lernsetData) {
  return apiClient.put(API_ENDPOINTS.LERNSETS.DETAIL(lernsetId), lernsetData);
}

export async function deleteLernset(lernsetId) {
  return apiClient.delete(API_ENDPOINTS.LERNSETS.DETAIL(lernsetId));
}

export async function getLernsets() {
  return apiClient.get(API_ENDPOINTS.LERNSETS.BASE);
}

export async function getLernsetQuizzes(lernsetId) {
  return apiClient.get(API_ENDPOINTS.LERNSETS.QUIZZES(lernsetId));
}