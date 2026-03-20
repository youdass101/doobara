import { sendJson } from '../core/http.js';

export function initDefaultAddressSelection() {
  const defaultAddressButtons = document.querySelectorAll('.make-default-address');

  if (!defaultAddressButtons.length) {
    return;
  }

  defaultAddressButtons.forEach((button) => {
    button.addEventListener('click', async () => {
      await sendJson('/address_list', 'POST', { id: button.value });
      window.location.reload();
    });
  });
}
