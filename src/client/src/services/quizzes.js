import { ref } from 'vue'
import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';


// Login
export async function getQuizzes(lernsetID) {
  return apiClient.get(API_ENDPOINTS.LERNSETS.QUIZZES(lernsetID));
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

export async function getSearch({ searchTerm, modulID, lernsetID, studiengangID }) {
  const params = {};

  if (searchTerm) params.search = searchTerm;
  if (modulID) params.modul = modulID;
  if (lernsetID) params.lernset = lernsetID;
  if (studiengangID) params.studiengang = studiengangID;

  return apiClient.get(API_ENDPOINTS.QUIZZES.SEARCH, params);
}