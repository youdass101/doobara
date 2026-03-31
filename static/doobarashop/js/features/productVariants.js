export function initProductVariants() {
  // Normal product variants are separate from system variants.
  // This initializer only handles non-system single-product variant switching.
  const variantDataElement = document.getElementById('normal-variant-data');
  const selector = document.getElementById('normal-variant-selector');
  const addToCartButton = document.getElementById('spatc');
  const productPrice = document.getElementById('spp');
  const shortDescription = document.getElementById('normal-variant-short-description');
  const productImage = document.getElementById('spi');

  if (!variantDataElement || !selector || !addToCartButton || !productPrice) {
    return;
  }

  let variants = [];
  try {
    variants = JSON.parse(variantDataElement.textContent || '[]');
  } catch (error) {
    return;
  }

  const defaultVariantElement = document.getElementById('default-normal-variant-id');
  const defaultVariantId = defaultVariantElement ? Number(JSON.parse(defaultVariantElement.textContent || '0')) : null;
  let selectedVariant = variants.find((variant) => variant.id === defaultVariantId) || variants[0];

  function syncButtons() {
    selector.querySelectorAll('.system-variant-option').forEach((button) => {
      const currentId = Number(button.dataset.normalVariantId);
      button.classList.toggle('is-active', selectedVariant && currentId === selectedVariant.id);
    });
  }

  function renderVariant() {
    if (!selectedVariant) {
      return;
    }

    const activePrice = selectedVariant.sale_price ?? selectedVariant.price;
    productPrice.innerHTML = `$ ${Number(activePrice).toFixed(2)}`;

    addToCartButton.dataset.normalVariantId = String(selectedVariant.id);
    addToCartButton.dataset.gaItemId = String(selectedVariant.id);
    addToCartButton.dataset.gaItemName = selectedVariant.title || '';
    addToCartButton.dataset.gaPrice = String(activePrice);

    if (shortDescription) {
      shortDescription.textContent = selectedVariant.short_description || '';
    }

    // Update the main product image only when this variant has its own image.
    if (productImage && selectedVariant.image) {
      productImage.src = selectedVariant.image;
      productImage.alt = selectedVariant.title || productImage.alt;
    }
  }

  renderVariant();
  syncButtons();

  selector.addEventListener('click', (event) => {
    const targetButton = event.target.closest('.system-variant-option');
    if (!targetButton) {
      return;
    }

    const variantId = Number(targetButton.dataset.normalVariantId);
    const found = variants.find((variant) => variant.id === variantId);
    if (!found) {
      return;
    }

    selectedVariant = found;
    renderVariant();
    syncButtons();
  });
}
