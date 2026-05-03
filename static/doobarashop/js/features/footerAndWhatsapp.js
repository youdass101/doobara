export function initFooterAndWhatsapp() {
  const yearElement = document.getElementById('year');
  if (yearElement) {
    yearElement.textContent = String(new Date().getFullYear());
  }

  const whatsappHeaderLink = document.getElementById('whatsapp-header-link');
  if (!whatsappHeaderLink) {
    return;
  }

  const pageTitle = document.title ? document.title.trim() : '';
  if (!pageTitle) {
    return;
  }

  // Build a page-aware prefilled message so support can instantly see where the user came from.
  const message = `Hi Doobara, I'm visiting: ${pageTitle}`;
  const encodedMessage = encodeURIComponent(message);
  whatsappHeaderLink.href = `${whatsappHeaderLink.href}?text=${encodedMessage}`;
}
