import { handleApiError } from './errors';
import { API_ENDPOINTS } from './endpoints';

// zentrale Basis-URL (kann via Vite-Env überschrieben werden)
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/**
 * ApiClient – ein Singleton für alle Fetch‑Aufrufe.
 *  - Schickt bei jedem Request credentials: 'include' (sessionid, csrftoken)
 *  - Fügt bei Schreib-Methoden automatisch X‑CSRFToken hinzu
 *  - login(username, password) setzt zunächst den CSRF‑Cookie, dann Session
 */
class ApiClient {
  constructor(baseURL = API_URL) {
    this.baseURL = baseURL.replace(/\/$/, '');
  }

  /* ───── Hilfsfunktionen ─────────────────────────────────────────── */
  getCookie(name) {
    return document.cookie
      .split('; ')
      .find((row) => row.startsWith(name + '='))
      ?.split('=')[1];
  }

  async getCsrfToken() {
    await fetch(`${this.baseURL}/csrf/`, {
      credentials: 'include',
    });
  }

  async login(username, password) {
    // 1) CSRF Versuch
    await this.getCsrfToken();
    // 2) Prüfen, ob Cookie wirklich gesetzt wurde
    if (!this.getCookie('csrftoken')) {
      throw new Error('CSRF-Cookie konnte nicht gesetzt werden');
    }
    // 3) Login
    return this.post('login/', { username, password });
    }

  /* ───── zentrale Request‑Methode ────────────────────────────────── */
  async request(endpoint, method = 'GET', data = null, extraHeaders = {}) {
    const url = new URL(endpoint, this.baseURL + '/').toString();

    const headers = { 'Content-Type': 'application/json', ...extraHeaders };

    if (method !== 'GET') {
      const token = this.getCookie('csrftoken');
      if (token) headers['X-CSRFToken'] = token;
    }

    const options = { method, headers, credentials: 'include' };
    if (data && method !== 'GET') options.body = JSON.stringify(data);
    if (data && method === 'GET') {
      const qs = new URLSearchParams(data).toString();
      if (qs) url += `?${qs}`;
    }

    const res = await fetch(url, options);
    if (res.status === 401) {
      window.location.href = '/login';
      throw new Error('Bitte erneut einloggen');
    }
    if (!res.ok) return handleApiError(res);

    const type = res.headers.get('content-type');
    return type && type.includes('application/json') ? res.json() : res.text();
  }

  /* ───── Convenience‑Wrapper ─────────────────────────────────────── */
  get(ep, params)   { return this.request(ep, 'GET',    params); }
  post(ep, data)    { return this.request(ep, 'POST',   data);   }
  put(ep, data)     { return this.request(ep, 'PUT',    data);   }
  patch(ep, data)   { return this.request(ep, 'PATCH',  data);   }
  delete(ep)        { return this.request(ep, 'DELETE');        }
}

export default new ApiClient();
