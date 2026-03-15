export function initCheckoutTotals() {
  const totalElement = document.getElementById('dtotal');
  const subTotalElement = document.getElementById('dsubtotal');
  const deliveryElement = document.getElementById('ddelivery');

  if (!totalElement || !subTotalElement || !deliveryElement) {
    return;
  }

  const subTotal = parseInt(subTotalElement.innerHTML.replace('$', '').trim(), 10);

  if (subTotal > 60) {
    deliveryElement.innerHTML = 'Free';
    return;
  }

  const total = (subTotal + 2).toFixed(2);
  totalElement.innerHTML = `$ ${total}`;
}
