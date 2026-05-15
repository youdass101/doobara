export function initFooterAndWhatsapp() {
  const yearElement = document.getElementById('year');
  if (yearElement) {
    yearElement.textContent = String(new Date().getFullYear());
  }

  const pageTitle = document.title ? document.title.trim() : '';
  const pageUrl = window.location.href;
  if (!pageTitle) {
    return;
  }

  // Reuse one shared WhatsApp prefilled message across header and product CTA links.
  const message = `Hi Doobara, I'm visiting: ${pageTitle} (${pageUrl})`;
  const encodedMessage = encodeURIComponent(message);

  document.querySelectorAll('#whatsapp-header-link, [data-whatsapp-help-link]').forEach((link) => {
    if (!(link instanceof HTMLAnchorElement)) {
      return;
    }
    const baseHref = link.href.split('?')[0];
    link.href = `${baseHref}?text=${encodedMessage}`;
  });
}
