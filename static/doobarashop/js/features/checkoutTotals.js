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
  const couponDiscount = Number.parseFloat(totalElement.dataset.couponDiscount || '0') || 0;

  const updateDisplay = (shippingPrice) => {
    if (shippingPrice > 0) {
      deliveryElement.innerHTML = `$ ${shippingPrice.toFixed(2)}`;
    } else {
      deliveryElement.innerHTML = 'Free';
    }

    const total = Math.max(subTotal - couponDiscount + shippingPrice, 0).toFixed(2);
    totalElement.innerHTML = `$ ${total}`;
  };

  const getPriceFromInput = (input) => {
    const fromDataAttribute = Number.parseFloat(input.dataset.shippingPrice);
    if (Number.isFinite(fromDataAttribute)) {
      return fromDataAttribute;
    }

    // Backward-compatible fallback for any older markup without data attributes.
    const optionRow = input.closest('.checkout-shipping-option, .cart-delivery-option');
    const priceText = optionRow?.querySelector('.checkout-shipping-option__price, strong')?.innerText || '0';
    return parseMoney(priceText);
  };

  const selectedInput = document.querySelector('.shipping-method-input:checked');
  if (selectedInput) {
    updateDisplay(getPriceFromInput(selectedInput));
  }

  shippingInputs.forEach((input) => {
    input.addEventListener('input', async () => {
      updateDisplay(getPriceFromInput(input));
      await sendJson('/updatecart', 'POST', { shipping_method_id: input.value });
    });
  });
}
