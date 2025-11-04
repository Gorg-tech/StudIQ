import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';

export async function getSelfUser() {
  return apiClient.get(API_ENDPOINTS.USER.ME);
}