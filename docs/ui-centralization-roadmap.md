# UI Centralization Roadmap (Sass + HTML + JS)

## Why this roadmap
This project already has good building blocks (Sass variables, shared layout template, and one main JS file), but the front-end is currently spread across app-level Sass entrypoints, mixed template patterns, and a monolithic JavaScript file. Centralizing those concerns will make future UI updates faster, safer, and easier to review.

## Current-state observations

1. **Sass is split by Django app with several separate `all.scss` aggregators**, while a root `style.scss` imports each one.
2. **Global design tokens exist** (`static/doobarashop/sass/abstracts/_variables.scss`), but values are still hardcoded in component styles (e.g. header/footer colors).
3. **Global layout is centralized** in `templates/doobarashop/layout.html`, but there is also a duplicate `layout copy.html` file, which increases maintenance cost.
4. **Behavior is centralized in one large JS file** (`static/doobarashop/main.js`) handling menu, account tabs, cart updates, checkout address logic, and more.
5. **Some UI behavior is still embedded in templates** via inline handlers (`onclick`) and inline scripts.

---

## Target architecture

### 1) Sass: one source of truth for tokens + component primitives
- Keep one top-level entrypoint (`style.scss`) that compiles to one CSS artifact.
- Move to a strict layered Sass structure:
  - `abstracts/` → tokens (colors, spacing, radius, typography, z-index)
  - `base/` → reset, typography, base element defaults
  - `components/` → reusable UI pieces (buttons, cards, nav items, badges, forms)
  - `layouts/` → site-wide layout regions (header/footer/grid/shell)
  - `pages/` → page-specific overrides only
  - `utilities/` → helper classes if needed (`.u-hidden`, spacing helpers)
- Replace hardcoded values in page/component files with token variables.
- Keep app-level Sass files only if they forward into the global component/page directories (avoid isolated style islands).

### 2) HTML: shared components and predictable template contracts
- Keep `layout.html` as the single global shell.
- Remove duplicate layout templates once parity is verified.
- Extract repeated HTML fragments into include partials:
  - `templates/doobarashop/partials/header.html`
  - `templates/doobarashop/partials/footer.html`
  - shared snippets for cards, buttons, pagination, forms.
- Define naming conventions for classes and data hooks:
  - visual classes for style (e.g. `.checkout-btn`)
  - `data-*` hooks for behavior (e.g. `data-js="mobile-menu-toggle"`)
- Stop adding inline JS in templates; attach behavior from JS modules.

### 3) JavaScript: split by feature + initialize by data hooks
- Split `main.js` into feature modules:
  - `ui/mobile-menu.js`
  - `ui/account-tabs.js`
  - `cart/cart-actions.js`
  - `checkout/address-switcher.js`
  - `shared/http.js` (fetch wrapper + CSRF helper)
- Add a small bootstrap file that initializes only the features found on the current page.
- Replace element-id coupling with resilient selectors and `data-js` attributes.
- Replace inline handlers with delegated listeners in modules.
- Optional but high-value: add JSDoc typing or migrate modules to TypeScript incrementally.

---

## Practical migration plan (low-risk)

### Phase 1: Inventory and guardrails (1–2 days)
1. Create a UI inventory document listing:
   - all Sass entrypoints/import graphs
   - duplicate template structures
   - all inline scripts/onclick usage
   - JS feature boundaries from `main.js`.
2. Add stylelint + eslint (or biome) config for consistency.
3. Define naming conventions and contribution rules in a `docs/ui-conventions.md`.

### Phase 2: Sass consolidation (2–4 days)
1. Keep `style.scss` as the only compiled entrypoint.
2. Move app-specific repeated patterns (buttons, form controls, cards) into `static/doobarashop/sass/components/`.
3. Replace hardcoded colors/radius with token variables.
4. Ensure each app-level `all.scss` only forwards page files (or remove them if unnecessary).

### Phase 3: Template cleanup (2–3 days)
1. Remove `layout copy.html` after migrating any required markup.
2. Extract header/footer and repeated chunks into include partials.
3. Replace inline event handlers with `data-js` attributes.
4. Keep template logic focused on content/state, not behavior wiring.

### Phase 4: JS modularization (3–5 days)
1. Introduce a small module folder under `static/doobarashop/js/`.
2. Move one feature at a time out of `main.js` (menu first, then account, cart, checkout).
3. Create shared helpers for CSRF + fetch response handling.
4. Keep `main.js` temporarily as a compatibility entry that imports/initializes modules.

### Phase 5: Validate and enforce (ongoing)
1. Add visual smoke checks for key pages (home, shop, cart, checkout, account).
2. Add lightweight DOM tests for JS behaviors (menu toggle, cart update trigger).
3. Add a PR checklist requiring:
   - tokens used instead of hardcoded visual values
   - no inline scripts/onclick
   - page CSS limited to page-specific concerns.

---

## High-impact quick wins you can do immediately
1. Remove `templates/doobarashop/layout copy.html` after confirming no usage.
2. Move inline year script in `layout.html` into a tiny `ui/footer-year.js` initializer.
3. Replace template `onclick` handlers in checkout/auth templates with `data-js` hooks and module listeners.
4. Extract CSRF + fetch boilerplate from `main.js` into one helper used by cart and checkout flows.
5. Add a single design-token map (spacing scale + font sizes) and start consuming it in header/footer/components.

## Success criteria
- A UI change (e.g. button radius/color) is made in one token/component file and reflected everywhere.
- New features can be built without editing giant global files.
- Template behavior wiring is standardized and testable.
- Front-end reviews become smaller and easier to reason about.
