import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';

// Registrierung
export async function register({ username, email, password, studiengang, semester }) {
  return apiClient.post(API_ENDPOINTS.AUTH.REGISTER, {
    username,
    email,
    password,
    studiengang,
    semester
});
}

// Login
export async function login({ username, password }) {
  return apiClient.post(API_ENDPOINTS.AUTH.LOGIN, {
    username,
    password,
  });
}

export async function refreshToken(refresh) {
  return apiClient.post(API_ENDPOINTS.AUTH.REFRESH, {
    refresh,
  })
}

export function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user')
  window.location.href = '/login'
}

/* Verwendung:

import { login, register } from '@/services/auth';

async function handleLogin() {
  try {
    const user = await login({ username: 'test', password: '1234' });
    // Weiterleitung oder User speichern
  } catch (err) {
    // Fehlerbehandlung
  }
}

async function handleRegister() {
  try {
    const user = await register({ username: 'test', email: 'test@mail.de', password: '1234', studiengang: 'Informatik', semester: 1 });
    // Weiterleitung oder User speichern
  } catch (err) {
    // Fehlerbehandlung
  }
}


*/
