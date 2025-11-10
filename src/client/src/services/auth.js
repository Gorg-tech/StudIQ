import { ref } from 'vue'
import apiClient from './api/client';
import { API_ENDPOINTS } from './api/endpoints';

export const isAuthenticated = ref(false)

export async function checkAuth() {
  try {
    // Call the backend "me" endpoint
    await apiClient.get(API_ENDPOINTS.USER.ME)
    isAuthenticated.value = true
  } catch {
    isAuthenticated.value = false
  }
}

// Registrierung
export async function register({ username, email, password, studiengang }) {
  return apiClient.post(API_ENDPOINTS.AUTH.REGISTER, {
    username,
    email,
    password,
    studiengang,
});
}

// Login
export async function login({ username, password }) {
  return apiClient.post(API_ENDPOINTS.AUTH.LOGIN, {
    username,
    password,
  });
}

// Logout
export async function logout() {
  return apiClient.post(API_ENDPOINTS.AUTH.LOGOUT);
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
    const user = await register({ username: 'test', email: 'test@mail.de', password: '1234', studiengang: 'Informatik' });
    // Weiterleitung oder User speichern
  } catch (err) {
    // Fehlerbehandlung
  }
}


*/
