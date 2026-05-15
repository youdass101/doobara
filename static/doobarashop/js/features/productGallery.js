export function initProductGallery() {
  const thumbnails = Array.from(document.querySelectorAll('.sp-thumb-image'));
  const mainImage = document.getElementById('spi');
  const mainMedia = document.querySelector('.single-product-gallery__main');
  const dotsContainer = document.getElementById('normal-gallery-dots');

  if (!thumbnails.length || !mainImage || !mainMedia) {
    return;
  }

  let currentIndex = 0;

  function setActiveImage(index) {
    const boundedIndex = (index + thumbnails.length) % thumbnails.length;
    currentIndex = boundedIndex;
    const activeThumb = thumbnails[boundedIndex];
    mainImage.src = activeThumb.src;
    mainImage.alt = activeThumb.alt || mainImage.alt;

    if (dotsContainer) {
      dotsContainer.querySelectorAll('button').forEach((dot, dotIndex) => {
        dot.classList.toggle('is-active', dotIndex === boundedIndex);
      });
    }
  }

  thumbnails.forEach((thumbnail, index) => {
    thumbnail.addEventListener('click', () => setActiveImage(index));
  });

  if (dotsContainer && thumbnails.length > 1) {
    thumbnails.forEach((_, index) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'single-product-gallery__dot';
      dot.setAttribute('aria-label', `Go to image ${index + 1}`);
      dot.addEventListener('click', () => setActiveImage(index));
      dotsContainer.appendChild(dot);
    });
  } else if (dotsContainer) {
    dotsContainer.style.display = 'none';
  }

  let startX = 0;
  mainMedia.addEventListener('touchstart', (event) => {
    startX = event.changedTouches[0].clientX;
  }, { passive: true });

  mainMedia.addEventListener('touchend', (event) => {
    const deltaX = event.changedTouches[0].clientX - startX;
    if (Math.abs(deltaX) < 30) return;
    setActiveImage(currentIndex + (deltaX < 0 ? 1 : -1));
  }, { passive: true });

  setActiveImage(0);
}
