const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

import { handleApiError } from './errors';
import { API_ENDPOINTS } from './endpoints';

/**
 * Notiz zu CSRF in Django:
 * 
 * Django verwendet zwei Arten von Cookies:
 * 
 * 1. sessionid: 
 *    - HTTP-only (kann nicht von JS gelesen werden)
 *    - Für Auth zuständig
 *    - Wird automatisch bei jedem Request mitgeschickt
 * 
 * 2. csrftoken:
 *    - Nicht HTTP-only, damit JS es lesen kann
 *    - Muss im X-CSRFToken Header mitgeschickt werden
 *    - Verhindert CSRF-Angriffe 
 * 
 * Workflow:
 * - Server setzt csrftoken Cookie
 * - Wir lesen es mit getCookie aus
 * - Wir schicken es bei POST/PUT/etc. im Header mit
 * - Django prüft ob Header und Cookie übereinstimmen
 * 
 * Dabei wird 'credentials: include' für die Session-Cookies verwendet, 
 * und der CSRF-Token wird manuell ausgelesen und mitgeschickt.
 * 
 * Wichtig: 
 * - CSRF-Token wird NUR bei nicht-GET Requests benötigt (POST, PUT, DELETE, etc.)
 * - GET Requests verändern keine Daten und benötigen daher keinen CSRF-Schutz
 * - 'credentials: include' wird bei ALLEN Requests verwendet (für die Session-Cookies)
 * - Django ignoriert CSRF-Token bei GET Requests, fordert ihn aber bei allen anderen
 */

export class ApiClient {
  constructor(baseURL = API_URL) {
    this.baseURL = baseURL;
  }

  getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  async request(endpoint, method = 'GET', data = null, customHeaders = {}) {
    let url = `${this.baseURL}/${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...customHeaders
    };

    // For non-GET requests, get CSRF token from cookie
    if (method !== 'GET') {
      const csrfToken = this.getCookie('csrftoken');
      if (csrfToken) {
        headers['X-CSRFToken'] = csrfToken;
      }
    }

    const options = {
      method,
      headers,
      credentials: 'include', // This is critical - it ensures cookies are sent with requests
    };
    
    // Add body for non-GET requests
    if (data && method !== 'GET') {
      options.body = JSON.stringify(data);
    }

    // Handle query params for GET requests
    if (data && method === 'GET') {
      const params = new URLSearchParams();
      Object.entries(data).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value);
        }
      });
      
      const queryString = params.toString();
      if (queryString) {
        url += `?${queryString}`;
      }
    }

    try {
      const response = await fetch(url, options);
      
      // Handle 401 Unauthorized globally
      if (response.status === 401) {
        // Just redirect to login - no need to clear token since it's a cookie
        window.location.href = '/login';
        throw new Error('Session expired. Please log in again.');
      }
      
      // Check for other HTTP errors
      if (!response.ok) {
        return handleApiError(response);
      }
      
      // Handle empty responses
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      }
      
      return await response.text();
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    }
  }

  
  //Ruft den CSRF-Endpoint auf, um das CSRF-Cookie zu setzen.
  async ensureCsrf() {
    await this.get(API_ENDPOINTS.AUTH.CSRF);
  }

  // Convenience methods remain the same
  get(endpoint, params) {
    return this.request(endpoint, 'GET', params);
  }

  post(endpoint, data) {
    return this.request(endpoint, 'POST', data);
  }

  put(endpoint, data) {
    return this.request(endpoint, 'PUT', data);
  }

  patch(endpoint, data) {
    return this.request(endpoint, 'PATCH', data);
  }

  delete(endpoint) {
    return this.request(endpoint, 'DELETE');
  }
}

// Create and export default instance
export default new ApiClient();