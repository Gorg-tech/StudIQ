import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';

// Questions
export async function getQuestion(questionId) {
  return apiClient.get(API_ENDPOINTS.QUESTIONS.DETAIL(questionId));
}

export async function createQuestion(questionData) {
  return apiClient.post(API_ENDPOINTS.QUESTIONS.BASE, questionData);
}

export async function updateQuestion(questionId, questionData) {
  return apiClient.put(API_ENDPOINTS.QUESTIONS.DETAIL(questionId), questionData);
}

export async function deleteQuestion(questionId) {
  return apiClient.delete(API_ENDPOINTS.QUESTIONS.DETAIL(questionId));
}

export async function getAnswers(questionId) {
  return apiClient.get(API_ENDPOINTS.QUESTIONS.ANSWERS(questionId));
}