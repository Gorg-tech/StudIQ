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

// Questions Answers
// Backend funktioniert noch nicht, was die Answer Options angeht - es können keine Answer-Options angelegt werden
export async function getAnswers(questionId) {
  return apiClient.get(API_ENDPOINTS.QUESTIONS.ANSWERS(questionId));
}

export async function getAnswer(questionId, answerId) {
  return apiClient.get(API_ENDPOINTS.QUESTIONS.ANSWER_DETAIL(questionId, answerId));
}

export async function createAnswer(questionId, answerData) {
  return apiClient.post(API_ENDPOINTS.QUESTIONS.ANSWERS(questionId), answerData);
}

export async function updateAnswer(questionId, answerId, answerData) {
  return apiClient.put(API_ENDPOINTS.QUESTIONS.ANSWER_DETAIL(questionId, answerId), answerData);
}

export async function deleteAnswer(questionId, answerId) {
  return apiClient.delete(API_ENDPOINTS.QUESTIONS.ANSWER_DETAIL(questionId, answerId));
}