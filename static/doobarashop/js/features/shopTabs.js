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
  const validTabs = ['products', 'systems'];

  const filterCards = (selectedTab) => {
    const shouldShowSystem = selectedTab === 'systems';

    cards.forEach((card) => {
      const isSystem = card.dataset.system === 'true';
      card.style.display = isSystem === shouldShowSystem ? '' : 'none';
    });

    tabs.forEach((tab) => {
      const isActive = tab.dataset.tab === selectedTab;
      tab.setAttribute('aria-pressed', String(isActive));
    });
  };

  // Check URL for ?tab=systems or ?tab=products to set initial state
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
      // dataset.tab is either 'products' or 'systems'
      const selectedTab = tab.dataset.tab;
      filterCards(selectedTab);
      // URL UPDATE
      updateUrl(selectedTab);
    });
  });

  filterCards(getInitialTab());
}