# Functional review — 2026-10-27

Scope: static route/client/form reconciliation, authorization predicates and selected positive/negative executable contracts. This is not browser journey coverage or a production sign-off.

## Inventory and reconciliation

`routes.json` records 152 API method registrations, dependencies, request parameters and handler filter expressions. `client-calls.json` records 161 request sites; `client-route-matches.json` directly reconciles 150 sites. The other 11 are delegation/dynamic sites reviewed manually:

- Communication Next proxy forwards the incoming method and path; communication-api delegates eight admin communication operations.
- staff-api supplies the generic bearer wrapper; WebsiteEditor supplies its request/FormData/download wrapper; SaaSBilling supplies its POST wrapper.
- StoreCheckout's generic request wrapper issues POST orders and payment verification (the static matcher defaults these indirect sites to GET).
- Student's GET helper forwards supplied options, including the invitation POST.
- StudentDetails constructs enrollment pause/resume/cancel paths accepted by the backend action route.

The form inventory records 202 controls and 22 form sites. Review covered account registration/login/OTP/reset/profile, studio setup and banking, teacher/student admission and editing, class/pricing/scheduling, memberships, checkout, SaaS billing, support, website editing, communication configuration and Zoom settings. Required/blank input, numeric bounds, enum values, partial-update semantics and readable validation responses were checked in the corresponding schemas and submit handlers. Server schemas remain authoritative. Dynamic component behavior and full browser flows belong to item 5.

## Role and tenant review

Route families reviewed: auth/context, admin, organizations/settings/analytics, teachers, students/enrollments, classes/session rules/occurrences/attendance, membership tiers, commerce, billing, websites, communication, support and Zoom. Foreign organization denial is exercised across the organization route family for studio/teacher/student roles; admin denial for non-admin roles; student-family denial for non-student roles. Selected object tests cover support, payment ownership, teacher class assignment, linked instructor/class type/tier resources and secondary-studio student admission. This is broad family coverage, not every possible positive permission combination.

## Fixes

- Implemented the missing typed owner analytics endpoint with organization/currency-scoped payment/order aggregates and explicit catalog-value semantics.
- Teacher activation submits its required studio-password confirmation. Student admission carries the selected studio; dashboard links preserve requested tenant and login destination.
- Student support creation requires a real organization relationship. Conversation access uses immutable user identity; email fallback removed. Student-only APIs reject other account roles.
- Bounded names, descriptions, currency, slug, timezone, pricing/precision, duration, age ranges, package counts and membership validity. Partial age updates validate the merged range; explicit null status/required membership fields return validation errors.
- One-on-one scheduling requires an active verified student. A paid order without enrollment returns a clear 409 instead of crashing or suggesting repayment.
- Frontend errors render FastAPI field messages safely without dumping submitted values. Public path segments are URL encoded.
- Notification links point to existing purchases/billing views with accurate CTA text and studio context; old receipt/invoice paths redirect. Downloadable/legal receipts were not implemented.

## Verification and remaining areas

657 backend tests pass, no skips/expected failures, including 13 isolated PostgreSQL cases (PG18.4, not PG16). The new boundary file has 40 passing cases. Frontend helper tests: 15 pass. Production build, TypeScript and lint pass; lint retains 11 existing warnings. All three legacy-link redirects return expected HTTP307 destinations.

Item 5: component/Playwright registration, login, purchases, billing and permissions. Item 6: database constraints/index drift, PG16, rollback/query plans and restore. Item 7: profiling/load/accessibility/privacy/observability/recovery. Privacy review must address the existing raw account-number storage behind `account_number_enc`, and studio-managed edits to globally shared student profiles/consent. Neither is certified resolved here. No live provider, payment, email or deployment actions were performed.

Inventory reproduction scripts assume this checkout path; run Python inventory from API with PYTHONPATH=. APP_ENV=test and its virtualenv; run Node scripts from Web with installed TypeScript. JSON filter inventories aid review and do not prove authorization by themselves.
