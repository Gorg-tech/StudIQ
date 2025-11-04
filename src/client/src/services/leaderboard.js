import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';

export const fetchLeaderboard = async (limit = 10, around = 0) => {
  // limit = number of top users to include; around = number of users before/after current user
  var url;
  if (Number.isInteger(around) && around > 0) {
    url = API_ENDPOINTS.LEADERBOARD.AROUND(limit, around)
  } else {
    url = API_ENDPOINTS.LEADERBOARD.LIMIT(limit)
  }
  return await apiClient.get(url)
}

export const fetchUserStats = async () => {
  return await apiClient.get(API_ENDPOINTS.USER.MY_STATS)
}