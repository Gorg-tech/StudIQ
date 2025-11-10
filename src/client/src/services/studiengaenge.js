import apiClient from './api/client'
import { API_ENDPOINTS } from './api/endpoints'

export const getStudiengaenge = async () => {
  return apiClient.get(API_ENDPOINTS.STUDIENGAENGE.BASE)
}