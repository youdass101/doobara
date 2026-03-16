export function initMobileMenu() {
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('navigation-mobile');

  if (!mobileMenuBtn || !mobileMenu) {
    return;
  }

  mobileMenuBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('show');
  });

  document.addEventListener('click', (event) => {
    const clickedInside =
      mobileMenu.contains(event.target) || mobileMenuBtn.contains(event.target);

    if (!clickedInside) {
      mobileMenu.classList.remove('show');
    }
  });
}
