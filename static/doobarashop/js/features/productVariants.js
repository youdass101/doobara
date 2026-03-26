export function initProductVariants() {
  const variantSelector = document.getElementById('variants');
  const addToCartButton = document.getElementById('spatc');
  const productPrice = document.getElementById('spp');
  const availability = document.getElementById('normal-variant-availability');
  const comparePrice = document.getElementById('normal-variant-compare-price');
  const mainImage = document.getElementById('spi');
  const gallery = document.getElementById('normal-variant-gallery');
  const shortSpecs = document.getElementById('normal-variant-short-specs');
  const longDescription = document.getElementById('longdescription');
  const variantDataElement = document.getElementById('normal-variant-data');

  if (!variantSelector || !addToCartButton || !productPrice || !variantDataElement) {
    return;
  }

  let variants = [];
  try {
    variants = JSON.parse(variantDataElement.textContent || '[]');
  } catch (error) {
    return;
  }

  if (!Array.isArray(variants) || !variants.length) {
    return;
  }

  const baseGalleryMarkup = gallery ? gallery.innerHTML : '';
  const baseShortSpecsMarkup = shortSpecs ? shortSpecs.innerHTML : '';
  const baseLongDescriptionMarkup = longDescription ? longDescription.innerHTML : '';
  const baseMainImage = mainImage ? { src: mainImage.getAttribute('src') || '', alt: mainImage.getAttribute('alt') || '' } : null;

  function renderVariant(variant) {
    if (!variant) {
      return;
    }

    // Keep cart payload explicit so backend adds the selected variant, not the parent product.
    addToCartButton.dataset.variantId = String(variant.id);
    addToCartButton.dataset.gaItemId = String(variant.id);
    addToCartButton.dataset.gaItemName = variant.title || '';
    addToCartButton.dataset.gaPrice = String(variant.sale_price ?? variant.price ?? 0);
    addToCartButton.dataset.gaCurrency = variant.currency || addToCartButton.dataset.gaCurrency || 'USD';
    addToCartButton.disabled = !variant.can_purchase;
    addToCartButton.textContent = variant.cart_cta_label || 'Out of Stock';

    const activePrice = variant.sale_price ?? variant.price;
    productPrice.textContent = `$ ${Number(activePrice || 0).toFixed(2)}`;

    if (comparePrice) {
      if (variant.sale_price) {
        comparePrice.classList.remove('is-hidden');
        comparePrice.innerHTML = `<span>$ ${Number(variant.price || 0).toFixed(2)}</span>`;
      } else {
        comparePrice.classList.add('is-hidden');
        comparePrice.innerHTML = '';
      }
    }

    if (availability) {
      availability.textContent = variant.availability_label || 'Out of Stock';
      availability.classList.toggle('is-in-stock', Boolean(variant.can_purchase));
      availability.classList.toggle('is-out-of-stock', !variant.can_purchase);
    }

    if (gallery && mainImage) {
      const images = Array.isArray(variant.images) ? variant.images : [];
      if (!images.length) {
        // Variant fallback: keep parent product gallery/images when a variant has no dedicated media.
        gallery.innerHTML = baseGalleryMarkup;
        if (baseMainImage) {
          mainImage.src = baseMainImage.src;
          mainImage.alt = baseMainImage.alt;
        }
      } else {
        gallery.innerHTML = '';
        images.forEach((image, index) => {
          const button = document.createElement('button');
          button.type = 'button';
          button.className = 'single-product-thumb';
          const img = document.createElement('img');
          img.className = 'sp-thumb-image';
          img.src = image.url;
          img.alt = image.alt_text || variant.title || '';
          button.appendChild(img);
          button.addEventListener('click', () => {
            mainImage.src = image.url;
            mainImage.alt = image.alt_text || variant.title || '';
          });
          if (index === 0) {
            mainImage.src = image.url;
            mainImage.alt = image.alt_text || variant.title || '';
          }
          gallery.appendChild(button);
        });
      }
    }

    if (shortSpecs) {
      const lines = Array.isArray(variant.short_description_lines) ? variant.short_description_lines : [];
      // Only override specs content when variant actually carries its own content.
      if (lines.length) {
        shortSpecs.innerHTML = '';
        lines.forEach((line) => {
          const listItem = document.createElement('li');
          listItem.textContent = line;
          shortSpecs.appendChild(listItem);
        });
      } else {
        shortSpecs.innerHTML = baseShortSpecsMarkup;
      }
    }

    if (longDescription) {
      // Only override long description when variant has override content.
      longDescription.innerHTML = variant.description ? variant.description : baseLongDescriptionMarkup;
    }
  }

  const defaultVariantIdElement = document.getElementById('default-normal-variant-id');
  const defaultVariantId = defaultVariantIdElement ? Number(JSON.parse(defaultVariantIdElement.textContent || '0')) : 0;
  const defaultVariant = variants.find((variant) => variant.id === defaultVariantId) || variants[0];
  renderVariant(defaultVariant);

  variantSelector.addEventListener('change', () => {
    const variantId = Number(variantSelector.value);
    const variant = variants.find((item) => item.id === variantId);
    renderVariant(variant);
  });
}
