import apiClient from './api/client'
import { API_ENDPOINTS } from './api/endpoints'

export const getModul = async (modulId) => {
  return await apiClient.get(API_ENDPOINTS.MODULES.DETAIL(modulId))
}