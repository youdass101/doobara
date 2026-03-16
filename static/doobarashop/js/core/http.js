import { getCookie } from './csrf.js';

export async function sendJson(url, method, payload) {
  const response = await fetch(url, {
    method,
    body: JSON.stringify(payload),
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
  });

  return response;
}
