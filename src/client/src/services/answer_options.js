import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';

export async function getAnswer(answerId) {
  return apiClient.get(API_ENDPOINTS.ANSWER_OPTIONS.DETAIL(answerId))
}

export async function createAnswer(answerData) {
  return apiClient.post(API_ENDPOINTS.ANSWER_OPTIONS.BASE, answerData)
}

export async function updateAnswer(answerId, answerData) {
  return apiClient.put(API_ENDPOINTS.ANSWER_OPTIONS.DETAIL(answerId), answerData)
}

export async function deleteAnswer(answerId) {
  return apiClient.delete(API_ENDPOINTS.ANSWER_OPTIONS.DETAIL(answerId))
}