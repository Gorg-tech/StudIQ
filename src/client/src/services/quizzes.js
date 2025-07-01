import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';


// Login
export async function getQuizzes(lernsetID) {
  return apiClient.get(API_ENDPOINTS.LERNSETS.QUIZZES(lernsetID));
}

export async function getSearch({ searchQuery, filter}) {
  return apiClient.get(API_ENDPOINTS.SEARCH( searchQuery, filter));
}

export async function getQuiz(quizId) {
  return apiClient.get(API_ENDPOINTS.QUIZZES.DETAIL(quizId));
}

export async function createQuiz(quizData) {
  return apiClient.post(API_ENDPOINTS.QUIZZES.BASE, quizData);
}

export async function updateQuiz(quizId, quizData) {
  return apiClient.put(API_ENDPOINTS.QUIZZES.DETAIL(quizId), quizData);
}

export async function getQuizQuestions(quizId) {
  return apiClient.get(API_ENDPOINTS.QUIZZES.QUESTIONS(quizId));
}

/* Usage Example:

import { getQuizzes } from '@/services/auth';

async function handleFetchQuizzes() {
  try {
    const quizzes = await getQuizzes();
    console.log('Fetched quizzes:', quizzes);
    // Use the quizzes data in your component or store
  } catch (err) {
    console.error('Error fetching quizzes:', err);
  }
}

*/