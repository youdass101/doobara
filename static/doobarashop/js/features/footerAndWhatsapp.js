export function initFooterAndWhatsapp() {
  const yearElement = document.getElementById('year');
  if (yearElement) {
    yearElement.textContent = String(new Date().getFullYear());
  }

  const pageTitle = document.title ? document.title.trim() : '';
  if (!pageTitle) {
    return;
  }

  // Build a page-aware prefilled message so support can instantly see where the user came from.
  const message = `Hi Doobara, I'm visiting: ${pageTitle}`;
  const encodedMessage = encodeURIComponent(message);
  const pageAwareWhatsappLinks = document.querySelectorAll('#whatsapp-header-link, [data-whatsapp-page-title]');
  pageAwareWhatsappLinks.forEach((link) => {
    const baseHref = link.href.split('?')[0];
    link.href = `${baseHref}?text=${encodedMessage}`;
  });
}
