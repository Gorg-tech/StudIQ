import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';

export async function getSelfUser() {
  return apiClient.get(API_ENDPOINTS.USER.ME);
}

export async function getSelfUserStats() {
  return apiClient.get(API_ENDPOINTS.USER.MY_STATS);
}

export async function getSelfUserStreaks() {
  return apiClient.get(API_ENDPOINTS.USER.MY_STREAKS);
}