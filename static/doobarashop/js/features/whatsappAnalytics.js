// Keep the guard on the document so repeated initialization/module loads share one listener.
const listenerKey = Symbol.for('doobara.whatsappAnalytics');

export function initWhatsappAnalytics() {
  if (document[listenerKey]) {
    return;
  }
  document[listenerKey] = true;
  const trackedClicks = new WeakSet();

  // Delegation includes future links and clicks on nested icons/text; capture survives bubbling stops.
  document.addEventListener('click', (event) => {
    const link = event.target?.closest?.('a[href]');
    if (!link || typeof window.gtag !== 'function' || trackedClicks.has(event)) {
      return;
    }

    let url;
    try {
      url = new URL(link.href, document.baseURI);
    } catch {
      return;
    }
    const isWhatsapp = url.protocol === 'whatsapp:' || (
      ['https:', 'http:'].includes(url.protocol) &&
      ['wa.me', 'api.whatsapp.com'].includes(url.hostname)
    );
    if (!isWhatsapp) {
      return;
    }

    // Deduplicate the same DOM event, while allowing each separate visitor click to count.
    trackedClicks.add(event);
    window.gtag('event', 'whatsapp_click', {
      link_url: link.href,
      link_text: (link.textContent || '').trim().slice(0, 100),
      page_location: window.location.href,
    });
    // Leave navigation untouched: no preventDefault, timeout, or event callback to wait for.
  }, { capture: true });
}
