import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';

export const fetchLeaderboard = async (limit = 10) => {
  const response = await apiClient.get(API_ENDPOINTS.LEADERBOARD.BASE(limit))
  return response.data
}

export const fetchUserStats = async () => {
  const response = await apiClient.get(API_ENDPOINTS.USER.MY_STATS)
  return response.data
}