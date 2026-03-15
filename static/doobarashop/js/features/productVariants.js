export function initProductVariants() {
  const variantSelector = document.getElementById('variants');
  const addToCartButton = document.getElementById('spatc');
  const productPrice = document.getElementById('spp');

  if (!variantSelector || !addToCartButton || !productPrice) {
    return;
  }

  variantSelector.addEventListener('change', () => {
    const selectedValue = variantSelector.options[variantSelector.selectedIndex]?.value;

    if (!selectedValue) {
      return;
    }

    const normalized = selectedValue.replaceAll("'", '"');
    const variant = JSON.parse(normalized);

    addToCartButton.value = variant.id;
    productPrice.innerHTML = Number(variant.price).toFixed(2);
  });
}
