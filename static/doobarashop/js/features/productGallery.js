export function initProductGallery() {
  function imageData(dot) {
    const fallbackImage = dot.querySelector('.sp-thumb-image');
    return {
      src: dot.dataset.imageSrc || (fallbackImage ? fallbackImage.src : ''),
      alt: dot.dataset.imageAlt || (fallbackImage ? fallbackImage.alt : ''),
    };
  }

  function galleryParts(gallery) {
    return {
      dots: Array.from(gallery.querySelectorAll('.single-product-thumb')),
      mainImage: gallery.querySelector('.single-product-gallery__main img'),
    };
  }

  // Read the current dots at interaction time so system-variant galleries work after rebuilds.
  function showGalleryImage(gallery, index) {
    const { dots, mainImage } = galleryParts(gallery);

    if (!dots.length || !mainImage) {
      return;
    }

    const nextIndex = (index + dots.length) % dots.length;
    const selectedDot = dots[nextIndex];
    const selectedImage = imageData(selectedDot);

    if (!selectedImage.src) {
      return;
    }

    mainImage.src = selectedImage.src;
    if (selectedImage.alt) {
      mainImage.alt = selectedImage.alt;
    }

    dots.forEach((dot, dotIndex) => {
      const isActive = dotIndex === nextIndex;
      dot.classList.toggle('is-active', isActive);
      dot.setAttribute('aria-current', isActive ? 'true' : 'false');
    });
  }

  function activeDotIndex(gallery) {
    const { dots, mainImage } = galleryParts(gallery);
    let activeIndex = dots.findIndex((dot) => dot.classList.contains('is-active'));

    if (activeIndex < 0 && mainImage) {
      activeIndex = dots.findIndex((dot) => imageData(dot).src === mainImage.currentSrc || imageData(dot).src === mainImage.src);
    }

    return activeIndex >= 0 ? activeIndex : 0;
  }

  function setupGallery(gallery) {
    const { dots, mainImage } = galleryParts(gallery);

    if (!dots.length || !mainImage) {
      return;
    }

    let pointerStartX = null;
    let pointerStartY = null;

    dots.forEach((dot) => {
      const selectedImage = imageData(dot);
      if (selectedImage.src) {
        dot.dataset.imageSrc = selectedImage.src;
      }
      if (selectedImage.alt) {
        dot.dataset.imageAlt = selectedImage.alt;
      }
      dot.textContent = '';
    });

    if (gallery.dataset.galleryReady === 'true') {
      showGalleryImage(gallery, activeDotIndex(gallery));
      return;
    }

    gallery.dataset.galleryReady = 'true';

    mainImage.addEventListener('dragstart', (event) => {
      event.preventDefault();
    });

    mainImage.addEventListener('pointerdown', (event) => {
      pointerStartX = event.clientX;
      pointerStartY = event.clientY;
      if (typeof mainImage.setPointerCapture === 'function') {
        mainImage.setPointerCapture(event.pointerId);
      }
    });

    mainImage.addEventListener('pointerup', (event) => {
      if (pointerStartX === null || pointerStartY === null) {
        return;
      }

      const distanceX = event.clientX - pointerStartX;
      const distanceY = event.clientY - pointerStartY;
      pointerStartX = null;
      pointerStartY = null;

      if (Math.abs(distanceX) < 40 || Math.abs(distanceY) > Math.abs(distanceX)) {
        return;
      }

      showGalleryImage(gallery, activeDotIndex(gallery) + (distanceX < 0 ? 1 : -1));
    });

    mainImage.addEventListener('pointercancel', () => {
      pointerStartX = null;
      pointerStartY = null;
    });

    showGalleryImage(gallery, activeDotIndex(gallery));
  }

  document.querySelectorAll('.single-product-gallery').forEach(setupGallery);

  document.addEventListener('click', (event) => {
    const dot = event.target.closest('.single-product-thumb');
    const gallery = dot ? dot.closest('.single-product-gallery') : null;

    if (!dot || !gallery) {
      return;
    }

    event.preventDefault();
    const { dots } = galleryParts(gallery);
    showGalleryImage(gallery, dots.indexOf(dot));
  });

  document.addEventListener('productGallery:updated', (event) => {
    const gallery = event.detail && event.detail.gallery;
    if (gallery) {
      setupGallery(gallery);
    }
  });
}
