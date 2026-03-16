export function initAddressPopup() {
  const changeAddressButton = document.getElementById('id_change_address_checkout');
  const popup = document.getElementById('id_change_address_popup');
  const closeButton = document.getElementById('id_close_address_popup');

  if (!changeAddressButton || !popup) {
    return;
  }

  const closePopup = () => {
    popup.style.display = 'none';
  };

  changeAddressButton.addEventListener('click', () => {
    popup.style.display = 'flex';
  });

  closeButton?.addEventListener('click', closePopup);

  document.addEventListener('click', (event) => {
    if (event.target === popup || event.target.classList.contains('checkout-modal-backdrop')) {
      closePopup();
    }
  });
}
