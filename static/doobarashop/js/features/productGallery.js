export function initProductGallery() {
  const thumbnails = document.querySelectorAll('.sp-thumb-image');
  const mainImage = document.getElementById('spi');

  if (!thumbnails.length || !mainImage) {
    return;
  }

  thumbnails.forEach((thumbnail) => {
    thumbnail.addEventListener('click', () => {
      mainImage.src = thumbnail.src;
    });
  });
}
