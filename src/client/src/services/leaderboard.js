import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';

export const fetchLeaderboard = async (limit, around, category) => {
  return await apiClient.get(API_ENDPOINTS.LEADERBOARD.BASE(limit, around, category));
}