export function initProductLightbox() {
  const gallery = document.querySelector('.single-product-gallery');
  if (!gallery) {
    return;
  }

  const mainImageWrap = gallery.querySelector('.single-product-gallery__main');
  const mainImage = mainImageWrap ? mainImageWrap.querySelector('img') : null;
  const openButton = gallery.querySelector('[data-product-lightbox-open]');
  const lightbox = gallery.querySelector('[data-product-lightbox]');

  if (!mainImageWrap || !mainImage || !openButton || !lightbox) {
    return;
  }

  const closeButton = lightbox.querySelector('[data-product-lightbox-close]');
  const prevButton = lightbox.querySelector('[data-product-lightbox-prev]');
  const nextButton = lightbox.querySelector('[data-product-lightbox-next]');
  const lightboxImage = lightbox.querySelector('[data-product-lightbox-image]');

  if (!closeButton || !prevButton || !nextButton || !lightboxImage) {
    return;
  }

  const body = document.body;
  let lastFocused = null;
  let currentIndex = 0;
  let touchStartX = null;
  let touchStartY = null;

  function getImages() {
    // Read fresh image data every time so variant-driven galleries remain in sync.
    const dots = Array.from(gallery.querySelectorAll('.single-product-thumb'));
    const images = dots
      .map((dot) => ({
        src: dot.dataset.imageSrc || '',
        alt: dot.dataset.imageAlt || mainImage.alt || '',
      }))
      .filter((item) => Boolean(item.src));

    if (!images.length && mainImage.src) {
      images.push({ src: mainImage.src, alt: mainImage.alt || '' });
    }

    return images;
  }

  function findCurrentIndex(images) {
    const currentSrc = mainImage.currentSrc || mainImage.src;
    const found = images.findIndex((item) => item.src === currentSrc);
    return found >= 0 ? found : 0;
  }

  function render() {
    const images = getImages();
    if (!images.length) {
      return;
    }

    const active = images[currentIndex] || images[0];
    lightboxImage.src = active.src;
    lightboxImage.alt = active.alt || mainImage.alt || '';

    const hasManyImages = images.length > 1;
    prevButton.hidden = !hasManyImages;
    nextButton.hidden = !hasManyImages;
    prevButton.disabled = !hasManyImages;
    nextButton.disabled = !hasManyImages;
  }

  function move(step) {
    const images = getImages();
    if (images.length <= 1) {
      return;
    }

    currentIndex = (currentIndex + step + images.length) % images.length;
    render();
  }

  function open() {
    const images = getImages();
    if (!images.length) {
      return;
    }

    lastFocused = document.activeElement;
    currentIndex = findCurrentIndex(images);
    render();

    lightbox.hidden = false;
    body.classList.add('is-lightbox-open');
    closeButton.focus();
  }

  function close() {
    if (lightbox.hidden) {
      return;
    }

    lightbox.hidden = true;
    body.classList.remove('is-lightbox-open');

    if (lastFocused && typeof lastFocused.focus === 'function') {
      lastFocused.focus();
    } else {
      openButton.focus();
    }
  }

  openButton.addEventListener('click', open);
  closeButton.addEventListener('click', close);
  prevButton.addEventListener('click', () => move(-1));
  nextButton.addEventListener('click', () => move(1));

  lightbox.addEventListener('click', (event) => {
    if (event.target === lightbox) {
      close();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (lightbox.hidden) {
      return;
    }

    if (event.key === 'Escape') {
      event.preventDefault();
      close();
    } else if (event.key === 'ArrowLeft') {
      event.preventDefault();
      move(-1);
    } else if (event.key === 'ArrowRight') {
      event.preventDefault();
      move(1);
    }
  });

  lightbox.addEventListener('touchstart', (event) => {
    if (!event.touches.length) {
      return;
    }

    touchStartX = event.touches[0].clientX;
    touchStartY = event.touches[0].clientY;
  }, { passive: true });

  lightbox.addEventListener('touchend', (event) => {
    if (touchStartX === null || touchStartY === null || !event.changedTouches.length) {
      return;
    }

    const distanceX = event.changedTouches[0].clientX - touchStartX;
    const distanceY = event.changedTouches[0].clientY - touchStartY;
    touchStartX = null;
    touchStartY = null;

    if (Math.abs(distanceX) < 40 || Math.abs(distanceY) > Math.abs(distanceX)) {
      return;
    }

    move(distanceX < 0 ? 1 : -1);
  }, { passive: true });
}
