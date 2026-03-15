# JavaScript Modernization Plan (from single `main.js` to dynamic modules)

## What I found in the current codebase

- A single browser script (`static/doobarashop/main.js`) handles all page features (mobile nav, product variants, thumbnails, cart add/update/remove, checkout totals, address popup, search popup, default address). This means one file is responsible for many unrelated page concerns.
- The base layout loads this same script for all pages, even though many handlers only apply to one screen.
- Event handlers are often attached with repeated DOM queries and several implicit globals (`obj`, `val`, `qtt`, `updates`, etc.), which raises coupling and bug risk.
- `window.onclick` is assigned in multiple places; later assignments override earlier ones.

## Why this is hard to scale

- **Tight coupling:** unrelated features change together.
- **Difficult debugging:** one page bug can come from code intended for another page.
- **Hard testing:** no clear unit boundaries.
- **Performance overhead:** handlers are scanned/attached on pages that do not use them.

## Recommended target architecture

Use **feature-based modules** plus a tiny bootstrap:

```text
static/doobarashop/js/
  bootstrap.js
  core/
    dom.js
    http.js
    csrf.js
  features/
    mobileMenu.js
    productVariants.js
    productGallery.js
    cartActions.js
    checkoutTotals.js
    addressPopup.js
    mobileSearch.js
```

### Bootstrap pattern

- Keep one entry file (`bootstrap.js`) loaded in layout.
- Each feature exposes `init()` and internally checks if required nodes exist.
- Bootstrap just calls all `init()` functions; each feature self-activates only when relevant.

## Practical migration plan (safe, incremental)

1. **Phase 1 — Extract helpers**
   - Move CSRF cookie helper + fetch wrapper into `core/`.
   - Replace direct repeated `fetch` blocks with one helper API.
2. **Phase 2 — Split by feature**
   - Extract mobile menu logic.
   - Extract cart logic (add/update/remove) into `cartActions.js`.
   - Extract single-product logic (variant + image thumb).
3. **Phase 3 — Data-driven hooks**
   - Replace hardcoded IDs with `data-*` attributes where possible (`data-action="add-to-cart"`, `data-role="mobile-menu"`).
   - Use delegated listeners for repeated elements.
4. **Phase 4 — Progressive enhancement**
   - Keep pages functional without JS; JS only enhances interactions.
5. **Phase 5 — Optional API cleanup**
   - Normalize cart endpoints and response shape to reduce UI branching.

## Immediate high-impact improvements

- Use `const`/`let` everywhere and remove implicit globals.
- Replace multiple `window.onclick = ...` assignments with `addEventListener('click', ...)`.
- Consolidate cart DOM updates in one function.
- Guard every feature with container-level selectors to avoid unnecessary work.

## Example pattern for each feature module

```js
// features/mobileMenu.js
export function initMobileMenu() {
  const btn = document.getElementById('mobile-menu-btn');
  const menu = document.getElementById('navigation-mobile');
  if (!btn || !menu) return;

  btn.addEventListener('click', () => menu.classList.toggle('show'));
  document.addEventListener('click', (event) => {
    const clickedInside = menu.contains(event.target) || btn.contains(event.target);
    if (!clickedInside) menu.classList.remove('show');
  });
}
```

## Suggested first sprint outcome

- Keep UI unchanged.
- Introduce module folders + bootstrap.
- Migrate only two features first:
  - `mobileMenu`
  - `cartActions`
- Verify all existing pages still work, then continue feature-by-feature.

This gives you a dynamic, maintainable foundation without a risky full rewrite.
