export const API_ENDPOINTS = {
  AUTH: {
    REGISTER: 'api/auth/register/',
    LOGIN: 'api/auth/login/',
    LOGOUT: 'api/auth/logout/',
    CSRF: 'api/auth/csrf/', 
  },

  USER: {
    ME: 'api/users/me/',
    MY_STATS: 'api/users/me/stats/'
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

  PROGRESS: {
    BASE: 'api/progress/',
    DETAIL: (progressId) => `api/progress/${progressId}/`,
  },

  SESSIONS: {
    BASE: 'api/sessions/',
    COMPLETE: (sessionId) => `api/sessions/${sessionId}/complete/`,
  },

  FEEDBACK: {
    BASE: 'api/feedback/',
    DETAIL: (feedbackId) => `api/feedback/${feedbackId}/`,
  },

  ACHIEVEMENTS: {
    BASE: 'api/achievements/',
    USER: 'api/achievements/user/',
  },
  LEADERBOARD: {
    BASE: () => `api/leaderboard`,
    LIMIT: (limit = 3) => `api/leaderboard?limit=${limit}`,
    AROUND: (limit = 3, around = 1) => `api/leaderboard?limit=${limit}&around=${around}`,
  }
};

export default API_ENDPOINTS;