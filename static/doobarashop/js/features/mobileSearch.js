export function initMobileSearch() {
  const searchButton = document.getElementById('search_icon');
  const searchBar = document.getElementById('popsearch');

  if (!searchButton || !searchBar) {
    return;
  }

  searchButton.addEventListener('click', () => {
    searchBar.classList.toggle('show');
  });
}
