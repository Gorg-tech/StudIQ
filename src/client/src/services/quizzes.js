import { ref } from 'vue'
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

// Quiz Questions
export async function getQuizQuestions(quizId) {
  return apiClient.get(API_ENDPOINTS.QUIZZES.QUESTIONS(quizId));
}

export async function getQuizQuestion(quizId, questionId) {
  return apiClient.get(API_ENDPOINTS.QUIZZES.QUESTION_DETAIL(quizId, questionId));
}

export async function createQuizQuestion(quizId, questionData) {
  return apiClient.post(API_ENDPOINTS.QUIZZES.QUESTIONS(quizId), questionData);
}

export async function updateQuizQuestion(quizId, questionId, questionData) {
  return apiClient.put(API_ENDPOINTS.QUIZZES.QUESTION_DETAIL(quizId, questionId), questionData);
}

export async function deleteQuizQuestion(quizId, questionId) {
  return apiClient.delete(API_ENDPOINTS.QUIZZES.QUESTION_DETAIL(quizId, questionId));
}

// Questions Answers
export async function getQuestionAnswers(questionId) {
  return apiClient.get(API_ENDPOINTS.QUESTIONS.ANSWERS(questionId));
}

export async function getQuestionAnswer(questionId, answerId) {
  return apiClient.get(API_ENDPOINTS.QUESTIONS.ANSWER_DETAIL(questionId, answerId));
}

export async function createQuestionAnswer(questionId, answerData) {
  return apiClient.post(API_ENDPOINTS.QUESTIONS.ANSWERS(questionId), answerData);
}

export async function updateQuestionAnswer(questionId, answerId, answerData) {
  return apiClient.put(API_ENDPOINTS.QUESTIONS.ANSWER_DETAIL(questionId, answerId), answerData);
}

export async function deleteQuestionAnswer(questionId, answerId) {
  return apiClient.delete(API_ENDPOINTS.QUESTIONS.ANSWER_DETAIL(questionId, answerId));
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