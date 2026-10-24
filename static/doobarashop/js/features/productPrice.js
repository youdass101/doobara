// Keep price and image badge synchronized with the currently selected option.
export function renderProductPrice(element, variant) {
  const hasSale = Boolean(variant.sale_price);
  element.replaceChildren();
  if (hasSale) {
    const original = document.createElement('del');
    original.className = 'product-price-original';
    original.textContent = `$ ${Number(variant.price).toFixed(2)}`;
    element.append(original, document.createTextNode(' '));
  }
  const current = document.createElement('span');
  current.textContent = `$ ${Number(hasSale ? variant.sale_price : variant.price).toFixed(2)}`;
  element.append(current);
  const badge = document.getElementById('product-sale-badge');
  if (badge) badge.hidden = !hasSale;
}
