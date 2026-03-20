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

  tabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      filterCards(tab.dataset.tab);
    });
  });

  filterCards('products');
}
