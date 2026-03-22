import { sendJson } from '../core/http.js';

// GA4 + Meta Pixel analytics: emit add_to_cart/AddToCart for system variants only after successful add.
function trackAddToCart(button) {
  const itemId = button.dataset.gaItemId || button.dataset.variantId || '';
  const itemName = button.dataset.gaItemName || '';
  if (typeof window.gtag !== 'function') {
    if (typeof window.fbq !== 'function') {
      return;
    }
  }

  const itemPrice = Number.parseFloat(button.dataset.gaPrice || '0');
  const item = {
    item_id: itemId,
    item_name: itemName,
    price: itemPrice,
    quantity: 1,
  };

  if (button.dataset.gaItemCategory) {
    item.item_category = button.dataset.gaItemCategory;
  }

  const currency = button.dataset.gaCurrency || 'USD';
  const value = Number(itemPrice.toFixed(2));

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
      num_items: 1,
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

function renderVariant(variant) {
  if (!variant) {
    return;
  }

  const title = document.getElementById('system-variant-title');
  const shortDescription = document.getElementById('system-variant-short-description');
  const price = document.getElementById('system-variant-price');
  const availability = document.getElementById('system-variant-availability');
  const mainImage = document.getElementById('system-variant-main-image');
  const gallery = document.getElementById('system-variant-gallery');
  const packageItems = document.getElementById('system-variant-package-items');
  const addToCartButton = document.getElementById('spatc');
  const specifications = document.getElementById('longdescription');

  if (specifications) specifications.textContent = variant.description || '';
  if (title) title.textContent = variant.title || '';
  if (shortDescription) shortDescription.textContent = variant.short_description || '';
  if (price) {
    const activePrice = variant.sale_price ?? variant.price;
    price.textContent = `$ ${Number(activePrice).toFixed(2)}`;
  }

  if (availability) {
    const baseAvailability = variant.availability_label || 'Out of Stock';
    availability.textContent = variant.in_stock
      ? `${baseAvailability} (${Number(variant.quantity || 0)} available)`
      : baseAvailability;
    availability.classList.toggle('is-in-stock', Boolean(variant.in_stock));
    availability.classList.toggle('is-out-of-stock', !variant.in_stock);
  }

  if (addToCartButton) {
    addToCartButton.dataset.variantId = String(variant.id);
    addToCartButton.dataset.gaItemId = String(variant.id);
    addToCartButton.dataset.gaItemName = variant.title || '';
    addToCartButton.dataset.gaPrice = String(variant.sale_price ?? variant.price ?? 0);
    addToCartButton.dataset.gaCurrency = variant.currency || addToCartButton.dataset.gaCurrency || 'USD';
    addToCartButton.disabled = !variant.in_stock;
    addToCartButton.textContent = variant.in_stock ? 'Add to Cart' : 'Out of Stock';
  }

  if (gallery) {
    gallery.innerHTML = '';
    (variant.images || []).forEach((image, index) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'single-product-thumb';

      const img = document.createElement('img');
      img.className = 'sp-thumb-image';
      img.src = image.url;
      img.alt = image.alt_text || variant.title;

      button.appendChild(img);
      button.addEventListener('click', () => {
        if (mainImage) {
          mainImage.src = image.url;
          mainImage.alt = image.alt_text || variant.title;
        }
      });

      if (index === 0 && mainImage) {
        mainImage.src = image.url;
        mainImage.alt = image.alt_text || variant.title;
      }

      gallery.appendChild(button);
    });
  }

  if (packageItems) {
    packageItems.innerHTML = '';
    (variant.package_items || []).forEach((item) => {
      const listItem = document.createElement('li');
      if (item.thumbnail) {
        const thumb = document.createElement('img');
        thumb.src = item.thumbnail;
        thumb.alt = item.name;
        listItem.appendChild(thumb);
      }
      const link = document.createElement('a');
      link.href = item.url;
      link.textContent = `${item.qty} × ${item.name}`;
      listItem.appendChild(link);
      packageItems.appendChild(listItem);
    });
  }
}

export function initSystemVariants() {
  const variantDataElement = document.getElementById('variant-data');
  const selector = document.getElementById('system-variant-selector');
  const addToCartButton = document.getElementById('spatc');

  if (!variantDataElement || !selector || !addToCartButton) {
    return;
  }

  let variants = [];
  let selectedVariant = null;

  try {
    variants = JSON.parse(variantDataElement.textContent || '[]');
  } catch (error) {
    return;
  }

  const defaultVariantElement = document.getElementById('default-variant-id');
  const defaultVariantId = defaultVariantElement ? Number(JSON.parse(defaultVariantElement.textContent || '0')) : null;
  selectedVariant = variants.find((variant) => variant.id === defaultVariantId) || variants[0];

  function syncActiveState() {
    selector.querySelectorAll('.system-variant-option').forEach((button) => {
      const currentId = Number(button.dataset.variantId);
      button.classList.toggle('is-active', selectedVariant && currentId === selectedVariant.id);
    });
  }

  renderVariant(selectedVariant);
  syncActiveState();

  selector.addEventListener('click', (event) => {
    const targetButton = event.target.closest('.system-variant-option');
    if (!targetButton) {
      return;
    }

    const variantId = Number(targetButton.dataset.variantId);
    const found = variants.find((variant) => variant.id === variantId);

    if (!found) {
      return;
    }

    selectedVariant = found;
    renderVariant(selectedVariant);
    syncActiveState();
  });

  addToCartButton.addEventListener('click', async () => {
    if (addToCartButton.disabled) {
      return;
    }
    const variantId = Number(addToCartButton.dataset.variantId);
    if (!variantId) {
      return;
    }

    const response = await sendJson('/shopaddtocart', 'PUT', {
      variant_id: variantId,
      quantity: 1,
    });

    const result = await response.json();
    // GA4 analytics: fire add_to_cart only when API confirms success.
    if (result.result === 'done') {
      updateCartSummary(result.cart);
      trackAddToCart(addToCartButton);
    }
  });
}
