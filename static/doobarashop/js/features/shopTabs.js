export function initShopTabs() {
  const tabsContainer = document.querySelector('[data-shop-tabs]');
  if (!tabsContainer) {
    return;
  }

  const tabs = tabsContainer.querySelectorAll('[data-tab]');
  const cards = document.querySelectorAll('.shop-card[data-system]');

  if (!tabs.length || !cards.length) {
    return;
  }

  // for URL query param, if we want to link to a specific tab
  // Keep the same tab-driven architecture, but allow the two new product-only filters.
  const validTabs = ['products', 'systems', 'desk-lamps', 'smart-devices'];

  const filterCards = (selectedTab) => {
    cards.forEach((card) => {
      const isSystem = card.dataset.system === 'true';
      // Category marker comes from template data-category and is normalized to lowercase there.
      const category = card.dataset.category || '';
      let shouldShow = false;

      if (selectedTab === 'systems') {
        // Existing behavior: systems tab shows only system products.
        shouldShow = isSystem;
      } else if (selectedTab === 'products') {
        // Existing behavior: all products tab shows non-system products.
        shouldShow = !isSystem;
      } else if (selectedTab === 'desk-lamps') {
        // New behavior: desk-lamps tab shows only non-system products in Desk Lamp category.
        shouldShow = !isSystem && category === 'desk lamp';
      } else if (selectedTab === 'smart-devices') {
        // New behavior: smart-devices is the safe fallback bucket for non-system, non-desk-lamp products.
        // Assumption: if there is no explicit smart-device category marker, all remaining non-system products are smart devices.
        shouldShow = !isSystem && category !== 'desk lamp';
      }

      card.style.display = shouldShow ? '' : 'none';
    });

    tabs.forEach((tab) => {
      const isActive = tab.dataset.tab === selectedTab;
      tab.setAttribute('aria-pressed', String(isActive));
    });
  };

  // Check URL for known tab values (including new tabs) to set initial state
  const getInitialTab = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const tab = urlParams.get('tab');
    return validTabs.includes(tab) ? tab : 'products';
  };
  // Update URL without reloading the page when a tab is clicked
  const updateUrl = (selectedTab) => {
    const url = new URL(window.location);
    url.searchParams.set('tab', selectedTab);
    window.history.replaceState({}, '', url);
  };

  tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      // dataset.tab is one of the values in validTabs.
      const selectedTab = tab.dataset.tab;
      filterCards(selectedTab);
      // URL UPDATE
      updateUrl(selectedTab);
    });
  });

  filterCards(getInitialTab());
}