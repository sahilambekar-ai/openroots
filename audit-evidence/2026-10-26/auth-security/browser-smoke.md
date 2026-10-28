# Item 2 browser smoke (2026-10-26)

Next production build served on localhost:3108. Login rendered; Forgot password
opened the recovery form. Registration rendered. No credentials were entered,
no account was created, and no reset/delivery/payment was submitted in the browser.
Detailed password/reset/logout semantics were exercised through isolated API and
frontend helper tests. Full component/Playwright journeys remain item 5.
