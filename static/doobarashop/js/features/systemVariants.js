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
  const featureSection = document.getElementById('single-product-feature-card');
  const featureGrid = document.getElementById('single-product-benefit-grid');
  const defaultFeatureCardsElement = document.getElementById('default-feature-cards-data');
  let defaultFeatureCards = [];
  try {
    defaultFeatureCards = defaultFeatureCardsElement ? JSON.parse(defaultFeatureCardsElement.textContent || '[]') : [];
  } catch (error) {
    defaultFeatureCards = [];
  }

  // NEW: System variant long description is pre-rendered HTML from server-side markdown conversion.
  if (specifications) specifications.innerHTML = variant.long_description_html || '';
  if (title) title.textContent = variant.title || '';
  // NEW: Rebuild bullet list from pre-split short description lines.
  if (shortDescription) {
    shortDescription.innerHTML = '';
    (variant.short_description_lines || []).forEach((line) => {
      const listItem = document.createElement('li');
      listItem.textContent = line;
      shortDescription.appendChild(listItem);
    });
  }
  if (price) {
    const activePrice = variant.sale_price ?? variant.price;
    price.textContent = `$ ${Number(activePrice).toFixed(2)}`;
  }

  if (availability) {
    const baseAvailability = variant.availability_label || 'Out of Stock';
    availability.textContent = variant.can_purchase
      ? `${baseAvailability} `
      : baseAvailability;
    availability.classList.toggle('is-in-stock', Boolean(variant.can_purchase));
    availability.classList.toggle('is-out-of-stock', !variant.can_purchase);
  }

  if (addToCartButton) {
    const addToCartLabel = addToCartButton.querySelector('.single-product-addtocart__label');
    addToCartButton.dataset.variantId = String(variant.id);
    addToCartButton.dataset.gaItemId = String(variant.id);
    addToCartButton.dataset.gaItemName = variant.title || '';
    addToCartButton.dataset.gaPrice = String(variant.sale_price ?? variant.price ?? 0);
    addToCartButton.dataset.gaCurrency = variant.currency || addToCartButton.dataset.gaCurrency || 'USD';
    addToCartButton.disabled = !variant.can_purchase;
    if (addToCartLabel) {
      addToCartLabel.textContent = variant.cart_cta_label || 'Out of Stock';
    } else {
      addToCartButton.textContent = variant.cart_cta_label || 'Out of Stock';
    }
  }

  if (gallery) {
    gallery.innerHTML = '';
    (variant.images || []).forEach((image, index) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'single-product-thumb';
      button.dataset.imageSrc = image.url;
      button.dataset.imageAlt = image.alt_text || variant.title;
      button.setAttribute('aria-label', `View image ${index + 1} of ${variant.images.length}`);
      button.classList.toggle('is-active', index === 0);
      button.setAttribute('aria-current', index === 0 ? 'true' : 'false');
      button.addEventListener('click', () => {
        if (!mainImage) {
          return;
        }

        mainImage.src = image.url;
        mainImage.alt = image.alt_text || variant.title;
        gallery.querySelectorAll('.single-product-thumb').forEach((dot, dotIndex) => {
          const isActive = dotIndex === index;
          dot.classList.toggle('is-active', isActive);
          dot.setAttribute('aria-current', isActive ? 'true' : 'false');
        });
      });

      if (index === 0 && mainImage) {
        mainImage.src = image.url;
        mainImage.alt = image.alt_text || variant.title;
      }

      gallery.appendChild(button);
    });

    // Let the shared gallery module bind swipe navigation after variant dots are rebuilt.
    gallery.closest('.single-product-gallery')?.removeAttribute('data-gallery-ready');
    document.dispatchEvent(new CustomEvent('productGallery:updated', { detail: { gallery: gallery.closest('.single-product-gallery') } }));

    if (!(variant.images || []).length && mainImage) {
      mainImage.removeAttribute('src');
      mainImage.alt = variant.title || '';
    }
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

  if (featureSection && featureGrid) {
    const cards = (variant.feature_cards || []).length ? (variant.feature_cards || []) : defaultFeatureCards;
    // Preserve card styling by rendering the same card/item DOM structure used by Django template.
    featureGrid.innerHTML = '';
    cards.forEach((feature) => {
      const article = document.createElement('article');
      article.className = 'single-product-benefit-item';
      if (feature.icon_url) {
        const icon = document.createElement('img');
        icon.className = 'single-product-benefit-item__icon';
        icon.src = feature.icon_url;
        icon.alt = `${feature.title || ''} icon`;
        icon.loading = 'lazy';
        article.appendChild(icon);
      }
      const titleElement = document.createElement('h3');
      titleElement.textContent = feature.title || '';
      article.appendChild(titleElement);
      if (feature.description) {
        const descriptionElement = document.createElement('p');
        descriptionElement.textContent = feature.description;
        article.appendChild(descriptionElement);
      }
      featureGrid.appendChild(article);
    });
    featureSection.hidden = !cards.length;
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
