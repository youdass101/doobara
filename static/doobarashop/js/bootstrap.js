import { initAddressPopup } from './features/addressPopup.js';
import { initCartActions } from './features/cartActions.js';
import { initCheckoutTotals } from './features/checkoutTotals.js';
import { initDefaultAddressSelection } from './features/defaultAddress.js';
import { initMobileMenu } from './features/mobileMenu.js';
import { initMobileSearch } from './features/mobileSearch.js';
import { initProductGallery } from './features/productGallery.js';
import { initProductVariants } from './features/productVariants.js';

document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initProductVariants();
  initProductGallery();
  initCartActions();
  initCheckoutTotals();
  initAddressPopup();
  initMobileSearch();
  initDefaultAddressSelection();
});
