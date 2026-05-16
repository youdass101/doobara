import { initAddressPopup } from './features/addressPopup.js';
import { initCartActions } from './features/cartActions.js';
import { initCheckoutTotals } from './features/checkoutTotals.js';
import { initDefaultAddressSelection } from './features/defaultAddress.js';
import { initFooterAndWhatsapp } from './features/footerAndWhatsapp.js';
import { initMobileMenu } from './features/mobileMenu.js';
import { initMobileSearch } from './features/mobileSearch.js';
import { initProductGallery } from './features/productGallery.js?v=20260516-gallery-dots';
import { initShopTabs } from './features/shopTabs.js';
import { initProductVariants } from './features/productVariants.js';
import { initSystemVariants } from './features/systemVariants.js?v=20260516-gallery-dots';

document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initProductVariants();
  initSystemVariants();
  initProductGallery();
  initCartActions();
  initCheckoutTotals();
  initAddressPopup();
  initMobileSearch();
  initDefaultAddressSelection();
  initShopTabs();
  initFooterAndWhatsapp();
});
