import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';

export async function completeQuiz(quizId, correctAnswersCount) {
  const data = {
    correct: correctAnswersCount,
  };
  return apiClient.post(API_ENDPOINTS.QUIZZES.COMPLETE(quizId), data);
}

export async function fetchQuizResults(quizId) {
  return await apiClient.get(API_ENDPOINTS.QUIZZES.COMPLETE(quizId));
}