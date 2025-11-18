import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';

// Alle Studiengänge
export const getStudiengaenge = () => {
  return apiClient.get(API_ENDPOINTS.STUDIENGAENGE.BASE)
}

// Einen Studiengang nach ID
export const getStudiengangById = (studiengangId) => {
  return apiClient.get(API_ENDPOINTS.STUDIENGAENGE.DETAIL(studiengangId))
}

// Module zu einem Studiengang
export const getModulesByStudiengang = async (studiengangId) => {
  const response = await apiClient.get(`${API_ENDPOINTS.STUDIENGAENGE.DETAIL(studiengangId)}modules/`)
  return response  // direkt das Array zurückgeben
}
