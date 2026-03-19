import { sendJson } from '../core/http.js';

export function initCheckoutTotals() {
  const totalElement = document.getElementById('dtotal');
  const subTotalElement = document.getElementById('dsubtotal');
  const deliveryElement = document.getElementById('ddelivery');
  const shippingInputs = document.querySelectorAll('.shipping-method-input');

  if (!totalElement || !subTotalElement || !deliveryElement || !shippingInputs.length) {
    return;
  }

  const parseMoney = (value) => Number.parseFloat(String(value).replace('$', '').trim()) || 0;
  const subTotal = parseMoney(subTotalElement.innerHTML);

  const updateDisplay = (shippingPrice) => {
    if (shippingPrice > 0) {
      deliveryElement.innerHTML = `$ ${shippingPrice.toFixed(2)}`;
    } else {
      deliveryElement.innerHTML = 'Free';
    }

    const total = (subTotal + shippingPrice).toFixed(2);
    totalElement.innerHTML = `$ ${total}`;
  };

  shippingInputs.forEach((input) => {
    input.addEventListener('change', async () => {
      const optionRow = input.closest('.checkout-shipping-option, .cart-delivery-option');
      const priceText = optionRow?.querySelector('.checkout-shipping-option__price, strong')?.innerText || '0';
      const shippingPrice = parseMoney(priceText);
      updateDisplay(shippingPrice);
      await sendJson('/updatecart', 'POST', { shipping_method_id: input.value });
    });
  });
}
