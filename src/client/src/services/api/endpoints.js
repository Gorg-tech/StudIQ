export const API_ENDPOINTS = {
  AUTH: {
    REGISTER: '/api/auth/register/',
    LOGIN: '/api/auth/login/',
    LOGOUT: '/api/auth/logout/',
  },

  USER: {
    ME: '/api/users/me/',
  },

  STUDIENGAENGE: {
    BASE: '/api/studiengaenge/',
    DETAIL: (studiengangId) => `/api/studiengaenge/${studiengangId}/`,
  },

  MODULES: {
    BASE: '/api/modules/',
    DETAIL: (moduleId) => `/api/modules/${moduleId}/`,
    LERNSETS: (moduleId) => `/api/modules/${moduleId}/lernsets/`,
  },

  LERNSETS: {
    BASE: '/api/lernsets/',
    DETAIL: (lernsetId) => `/api/lernsets/${lernsetId}/`,
    QUIZZES: (lernsetId) => `/api/lernsets/${lernsetId}/quizzes/`,
  },

  QUIZZES: {
    BASE: '/api/quizzes/',
    DETAIL: (quizId) => `/api/quizzes/${quizId}/`,
    QUESTIONS: (quizId) => `/api/quizzes/${quizId}/questions/`,
    QUESTION_DETAIL: (quizId, questionId) => `/api/quizzes/${quizId}/questions/${questionId}/`,
  },

  QUESTIONS: {
    BASE: '/api/questions/',
    DETAIL: (questionId) => `/api/questions/${questionId}/`,
    ANSWERS: (questionId) => `/api/questions/${questionId}/answers/`,
    ANSWER_DETAIL: (questionId, answerId) => `/api/questions/${questionId}/answers/${answerId}/`,
  },

  PROGRESS: {
    BASE: '/api/progress/',
    DETAIL: (progressId) => `/api/progress/${progressId}/`,
  },

  SESSIONS: {
    BASE: '/api/sessions/',
    COMPLETE: (sessionId) => `/api/sessions/${sessionId}/complete/`,
  },

  FEEDBACK: {
    BASE: '/api/feedback/',
    DETAIL: (feedbackId) => `/api/feedback/${feedbackId}/`,
  },

  ACHIEVEMENTS: {
    BASE: '/api/achievements/',
    USER: '/api/achievements/user/',
  }
};

export default API_ENDPOINTS;