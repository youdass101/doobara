# AGENTS.md

## Project overview
This repository is a Django ecommerce project for Doobara.
Main stack:
- Django
- PostgreSQL
- SCSS
- Django templates
- JavaScript modules

Primary business areas:
- normal products
- normal product variants
- system products with system variants
- cart / checkout / orders
- account / auth / email flows
- admin product and order management

## Working style
- Prefer minimal, safe, maintainable changes
- Preserve current architecture unless a change is clearly required
- Do not make unrelated refactors
- Keep code simple and explicit
- Comment all newly added non-trivial code with clear explanations of what it does and why

## Styling rules
- Never modify `style.css`
- Put styling changes only in the related SCSS file(s)
- Reuse shared variables and mixins from shared SCSS files where possible
- Add shared variables/mixins only if it improves the centralized styling system
- Keep styling visually consistent with the existing Doobara design language
- Preserve mobile-friendliness

## Django and backend rules
- Reuse current models, views, templates, and helper patterns where possible
- Keep system variant logic separate from normal product variant logic
- Do not merge product variants and system variants into one confusing abstraction
- For historical order data, save purchase snapshots correctly so later UI/admin/email does not rely on current product state
- Do not hardcode data that should live in models when the project already supports admin-managed content

## Product content rules
- Product optimization/content structure must stay consistent:
  - Product title
  - SEO title
  - Short description
  - Long description
  - Package includes
  - Main image alt text
  - Additional image alt texts
  - Image title
- Do not invent unsupported specs or fake brand data
- Short description should remain concise and structured
- Long description should remain practical and sales-useful
- Where plain text content is mapped into HTML, preserve the current formatting rules instead of reintroducing raw HTML storage unless explicitly requested

## Shop / product page rules
- Simple products, normal variant products, and system products must be handled as distinct cases
- If a product requires selection before purchase, prefer "Choose Option" over direct add-to-cart from listing pages
- Use real selectable variant/tier prices when showing price ranges
- Keep single product UI clean and predictable

## Cart / checkout / order rules
- Preserve current cart and checkout flows unless changes are required for the task
- When adding new checkout logic, ensure order history, admin, and emails reflect the saved order data correctly
- Delivery/payment/order-related changes must remain consistent across:
  - cart
  - checkout
  - order creation
  - order history
  - admin
  - email notifications

## Admin rules
- Admin changes should improve practical usability
- Make product, variant, and order management easier without overbuilding
- Prefer inline editing, sorting, filtering, and clear defaults where useful

## Email rules
- Email templates should be email-client friendly
- Keep email styling inside the email template
- Use simple, robust HTML suitable for email rendering
- Preserve consistency between customer emails, admin notifications, and saved order data

## Settings and environment rules
- This project uses `.env` locally and explicit loading may be required
- Production settings should remain environment-driven
- Do not weaken security-related settings casually
- Be careful around SECRET_KEY, DEBUG, ALLOWED_HOSTS, CSRF, cookies, email, and Sentry config

## Logging and production safety
- Preserve Sentry integration
- Do not remove or weaken error monitoring without reason
- For production-facing changes, prefer fail-safe behavior and clear logging

## Migrations and database changes
- When models change, create proper Django migrations
- Keep migrations focused and easy to review
- Do not rewrite old migrations unless explicitly asked

## Testing and validation
Before finishing a task:
- Check for obvious template/rendering regressions
- Check whether cart/order/admin/email flows still match the changed data model
- Prefer small reviewable diffs
- Mention any assumptions or areas that still need manual verification