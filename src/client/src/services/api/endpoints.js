export const API_ENDPOINTS = {
  AUTH: {
    REGISTER: 'api/auth/register/',
    LOGIN: 'api/auth/login/',
    LOGOUT: 'api/auth/logout/',
    CSRF: 'api/auth/csrf/', 
  },

  USER: {
    ME: 'api/users/me/',
    MY_STATS: 'api/users/me/stats/',
    MY_STREAKS: 'api/users/me/streaks/',
    MY_FRIENDS: 'api/users/me/friends/',
    FRIEND_REQUESTS: 'api/users/me/friend-requests/',
  },

  SEARCH: (searchQuery, filter) => {
    let url = 'api/search/';
    const params = [];
    if (searchQuery) params.push(`q=${encodeURIComponent(searchQuery)}`);
    if (filter) params.push(`filter=${encodeURIComponent(filter)}`);
    if (params.length) url += `?${params.join('&')}`;
    return url;
  },

  STUDIENGAENGE: {
    BASE: 'api/studiengaenge/',
    DETAIL: (studiengangId) => `api/studiengaenge/${studiengangId}/`,
  },

  MODULES: {
    BASE: 'api/modules/',
    DETAIL: (moduleId) => `api/modules/${moduleId}/`,
  },

  LERNSETS: {
    BASE: 'api/lernsets/',
    DETAIL: (lernsetId) => `api/lernsets/${lernsetId}/`,
    QUIZZES: (lernsetId) => `api/lernsets/${lernsetId}/quizzes/`,
  },

  QUIZZES: {
    BASE: 'api/quizzes/',
    DETAIL: (quizId) => `api/quizzes/${quizId}/`,
    QUESTIONS: (quizId) => `api/quizzes/${quizId}/questions/`,
    QUESTION_DETAIL: (quizId, questionId) => `api/quizzes/${quizId}/questions/${questionId}/`,
    SUGGESTED_QUIZZES: 'api/suggested-quizzes/',
    START: (quizId) => `api/quizzes/${quizId}/start/`,
    SUBMIT_ANSWER: (quizId) => `api/quizzes/${quizId}/answer/`,
    SESSIONS: (quizId) => `api/quizzes/${quizId}/sessions/`,
    COMPLETE: (quizId) => `api/quizzes/${quizId}/complete/`,
  },

  QUESTIONS: {
    BASE: 'api/questions/',
    DETAIL: (questionId) => `api/questions/${questionId}/`,
    ANSWERS: (questionId) => `api/questions/${questionId}/answers/`,
    ANSWER_DETAIL: (questionId, answerId) => `api/questions/${questionId}/answers/${answerId}/`,
  },

  ANSWER_OPTIONS: {
    BASE: 'api/answer-options/',
    DETAIL: (optionId) => `api/answer-options/${optionId}/`
  },
  
  LEADERBOARD: {
    BASE: (limit = 3, around = 1, category = 'all') => `api/leaderboard?limit=${limit}&around=${around}&category=${encodeURIComponent(category)}`,
  }
};

export default API_ENDPOINTS;