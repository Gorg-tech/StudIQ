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
    DETAIL: (id) => `/api/studiengaenge/${id}/`,
  },
  
  MODULE: {
    BASE: '/api/module/',
    DETAIL: (id) => `/api/module/${id}/`,
  },
  
  LERNSETS: {
    BASE: '/api/lernsets/',
    DETAIL: (id) => `/api/lernsets/${id}/`,
  },
  
  QUIZZES: {
    BASE: '/api/quizzes/',
    DETAIL: (id) => `/api/quizzes/${id}/`,
    QUESTIONS: (quizId) => `/api/quizzes/${quizId}/questions/`,
    QUESTION_DETAIL: (quizId, questionId) => `/api/quizzes/${quizId}/questions/${questionId}/`, // idk brauchen wir wahrscheinlich nicht
  },
  
  QUESTIONS: {
    BASE: '/api/questions/',
    DETAIL: (id) => `/api/questions/${id}/`,
    ANSWERS: (questionId) => `/api/questions/${questionId}/answers/`,
    ANSWER_DETAIL: (questionId, answerId) => `/api/questions/${questionId}/answers/${answerId}/`,
  },
  
  PROGRESS: {
    BASE: '/api/progress/',
    DETAIL: (quizId) => `/api/progress/${quizId}/`,
  },
  
  SESSIONS: {
    BASE: '/api/sessions/',
    COMPLETE: (id) => `/api/sessions/${id}/complete/`,
  },
  
  FEEDBACK: {
    BASE: '/api/feedback/',
    DETAIL: (id) => `/api/feedback/${id}/`,
  },
  
  ACHIEVEMENTS: {
    BASE: '/api/achievements/',
    USER: '/api/achievements/user/',
  }
};

export default API_ENDPOINTS;