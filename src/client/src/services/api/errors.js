export class ApiError extends Error {
  constructor(status, message, data = null) {
    super(message);
    this.status = status;
    this.data = data;
    this.name = 'ApiError';
  }
}

export async function handleApiError(response) {
  let errorData;
  try {
    errorData = await response.json();
  } catch (e) {
    errorData = { detail: 'Unknown error occurred' };
  }

  const message = errorData.detail || errorData.message || `Error ${response.status}`;
  throw new ApiError(response.status, message, errorData);
}