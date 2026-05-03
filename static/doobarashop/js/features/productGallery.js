export function initProductGallery() {
  const thumbnails = document.querySelectorAll('.sp-thumb-image');
  const mainImage = document.getElementById('spi');

  if (thumbnails.length && mainImage) {
    thumbnails.forEach((thumbnail) => {
      thumbnail.addEventListener('click', () => {
        mainImage.src = thumbnail.src;
      });
    });
  }

  // Add left/right controls for thumbnail strips so mobile users can discover more images.
  document.querySelectorAll('.single-product-gallery__thumbs-wrap').forEach((wrap) => {
    const list = wrap.querySelector('.single-product-gallery__thumbs');
    const leftButton = wrap.querySelector('[data-thumbs-nav="left"]');
    const rightButton = wrap.querySelector('[data-thumbs-nav="right"]');

    if (!list || !leftButton || !rightButton) {
      return;
    }

    const scrollDistance = () => Math.max(120, Math.floor(list.clientWidth * 0.65));

    leftButton.addEventListener('click', () => {
      list.scrollBy({ left: -scrollDistance(), behavior: 'smooth' });
    });

    rightButton.addEventListener('click', () => {
      list.scrollBy({ left: scrollDistance(), behavior: 'smooth' });
    });
  });
}
