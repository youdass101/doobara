import { sendJson } from '../core/http.js';

// GA4 + Meta Pixel analytics: emit add_to_cart/AddToCart only after a successful backend add.
function trackAddToCart(button, quantity) {
  const itemId = button.dataset.gaItemId || button.value;
  const itemName = button.dataset.gaItemName || '';
  if (typeof window.gtag !== 'function') {
    if (typeof window.fbq !== 'function') {
      return;
    }
  }

  const itemPrice = Number.parseFloat(button.dataset.gaPrice || '0');
  const itemQuantity = Number.parseInt(quantity, 10) || 1;
  const item = {
    item_id: itemId,
    item_name: itemName,
    price: itemPrice,
    quantity: itemQuantity,
  };

  if (button.dataset.gaItemCategory) {
    item.item_category = button.dataset.gaItemCategory;
  }

  const currency = button.dataset.gaCurrency || 'USD';
  const value = Number((itemPrice * itemQuantity).toFixed(2));

  if (typeof window.gtag === 'function') {
    window.gtag('event', 'add_to_cart', {
      currency,
      value,
      items: [item],
    });
  }

  if (typeof window.fbq === 'function') {
    // Meta Pixel: AddToCart standard event.
    window.fbq('track', 'AddToCart', {
      content_ids: [itemId],
      content_name: itemName,
      content_type: 'product',
      value,
      currency,
      num_items: itemQuantity,
    });
  }
}

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

      const responsePayload = {
        pid: button.value,
        quantity,
      };
      // Keep normal single-product variant cart payload separate from system variants.
      if (button.dataset.normalVariantId) {
        responsePayload.normal_variant_id = Number(button.dataset.normalVariantId);
      }

      const response = await sendJson('/shopaddtocart', 'PUT', responsePayload);

      const result = await response.json();

      // GA4 analytics: fire add_to_cart only when API confirms success.
      if (result.result === 'done') {
        updateCartSummary(result.cart);
        trackAddToCart(button, quantity);
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
