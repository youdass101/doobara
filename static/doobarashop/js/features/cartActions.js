import { sendJson } from '../core/http.js';

function updateCartSummary(cart) {
  const cartItemsElement = document.getElementById('cartitemsqtt');
  const footerItemsElement = document.getElementById('footeritemqtt');
  const cartTotalElement = document.getElementById('carttotal');

  if (cartItemsElement) {
    cartItemsElement.innerHTML = cart.item;
  }

  if (footerItemsElement) {
    footerItemsElement.innerHTML = cart.item;
  }

  if (cartTotalElement) {
    cartTotalElement.innerHTML = `$ ${Number(cart.total).toFixed(2)}`;
  }
}

async function cartUpdate(data) {
  await sendJson('/updatecart', 'POST', { cart: data });
  window.location.reload();
}

function bindAddToCartButtons() {
  const addToCartButtons = document.querySelectorAll('.shop-add-to-cart');

  if (!addToCartButtons.length) {
    return;
  }

  addToCartButtons.forEach((button) => {
    if (button.dataset.variantId) {
      return;
    }

    button.addEventListener('click', async () => {
      const quantityField = document.getElementById('spq');
      const quantity = quantityField ? quantityField.value : 1;

      const response = await sendJson('/shopaddtocart', 'PUT', {
        pid: button.value,
        quantity,
      });

      const result = await response.json();

      if (result.result !== 'login') {
        updateCartSummary(result.cart);
      }
    });
  });
}

function bindUpdateCartButton() {
  const updateButton = document.getElementById('update-cart-button');

  if (!updateButton) {
    return;
  }

  updateButton.addEventListener('click', () => {
    const updates = [];

    document.querySelectorAll('.in-cart-qtty').forEach((element) => {
      const parent = element.parentElement;
      const productId = parent.querySelector('#quantity-item-name')?.value;

      if (productId) {
        updates.push({ quantity: element.value, pid: productId });
      }
    });

    cartUpdate(updates);
  });
}

function bindRemoveButtons() {
  const removeButtons = document.querySelectorAll('.cart-item__remove.close-button');

  if (!removeButtons.length) {
    return;
  }

  removeButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const productRow = button.closest('.cart-item');
      const currentQuantity = productRow?.querySelector('.in-cart-qtty')?.value;
      const quantityNumber = Number.parseInt(currentQuantity, 10);

      if (!Number.isFinite(quantityNumber) || quantityNumber <= 0) {
        return;
      }

      cartUpdate({ pid: button.value, quantity: -quantityNumber });
    });
  });
}

export function initCartActions() {
  bindAddToCartButtons();
  bindUpdateCartButton();
  bindRemoveButtons();
}
