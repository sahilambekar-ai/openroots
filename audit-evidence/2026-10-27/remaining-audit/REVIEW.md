# Remaining audit areas — local review (2026-10-27)

## Resource and performance evidence

The traced soak executed 3,000 requests at concurrency10 against real PostgreSQL16, with a synthetic 100-class catalog and a mix of health/plans/auth-me/public catalog reads. Warm-up:200 requests; six measured batches of500. No live provider calls or existing application tables. It owns/drops a random schema. Tracing is deliberately expensive and is not a throughput benchmark.

| Batch | Retained Python MiB | RSS MiB | Tasks | Threads | DB checked out |
|---|---:|---:|---:|---:|---:|
| 1 | 0.865 | 134.59 | 2 | 1 | 0 |
| 2 | 1.184 | 113.25 | 2 | 1 | 0 |
| 3 | 1.350 | 115.16 | 2 | 1 | 0 |
| 4 | 1.381 | 115.36 | 2 | 1 | 0 |
| 5 | 1.408 | 113.95 | 2 | 1 | 0 |
| 6 | 1.438 | 117.62 | 2 | 1 | 0 |

Retained growth slowed after warm-up; traces include benchmark duration/heartbeat arrays, asyncpg prepared statements and socket buffers. This is bounded short-run evidence, not proof of no long-term leak. API/worker shutdown disposal and telemetry exception cleanup have direct tests. Frontend review found unused inline-preview blobs and URLs retained until editor exit; the new bounded pool keeps five previews and releases downloads/unmounts. Calendar scroll timers now cancel/reuse.

The separate untraced run of the same workload recorded 3000 successes / 7.70s, 389.8 requests/s, p50 19.2 ms, p95 61.3 ms, p99 66.7 ms. Max loop lag 29.5 ms. These are in-process ASGI measurements on local macOS, with read-heavy synthetic data and no network/proxy/write/provider/worker load; do not use as production capacity.

Eight password verifications on the event loop measured 120.4 ms max lag; bounded offloaded work measured 3.3 ms. Registration/login/reset and teacher credential hashing/reconfirmation use a separate four-operation-per-worker limiter. Tests verify the limit and preserve security/race behavior. Multiply memory budgets by deployed workers.

Public teacher catalogs contained two per-class queries (enrollment count and next occurrence). Grouped enrollment and window-ranked next-occurrence queries now stay at two queries for both one and eight classes; output tests retain capacity and earliest-occurrence semantics. Existing public-studio batching remains covered.

## Browser resource and accessibility review

- chromium: 30 checkout/billing mount/unmount cycles (five warm-up,25 measured); DOM nodes 30 → 30, listeners 157 → 157, retained JS heap delta 0.380 MiB after forced GC.
- mobile-chromium: 30 checkout/billing mount/unmount cycles (five warm-up,25 measured); DOM nodes 30 → 30, listeners 157 → 157, retained JS heap delta 0.380 MiB after forced GC.

Axe A/AA tests cover login, both registration roles, privacy, pricing, and styled production checkout/billing. Fixes: invalid label on notification container, low-contrast muted auth/billing text and Tab wrap inside native dialogs. Keyboard tests check containment, Escape, focus restoration and no accidental privacy acceptance. All54 desktop/mobile browser checks pass against a production Next build (controlled API/payment responses); there are nine component and15 helper tests. No full-site WCAG/assistive-technology/physical-device certification is claimed.

Local production page samples cover login, student registration and privacy: raw LCP/CLS/TTFB/DCL samples are preserved for both viewports. Fonts were awaited and a single snapshot captured; this is local lab data, not field Core Web Vitals or real-user percentile measurement. Three pages do not establish dashboard performance.

## Verified dead code and quality

A conservative TypeScript import graph rooted at every Next app module found one unreachable source module: `src/components/EnrollmentModal.tsx`. Repository search confirmed no references/registry usage; its nine-line wrapper was removed. The post-cleanup graph reports no unreachable files under that analysis. Runtime models/routes/dynamic relationships were not deleted based on lint heuristics. This is not a general proof that every export/function is used. Ruff0.17.2 is pinned; CI gains an app/script/test correctness subset plus full scoped checks for new security/runtime modules. Existing broad Python lint/type debt and incomplete typed response contracts remain follow-up work (AUD012/013).

## Privacy, observability and recovery

- New bank values: versioned independent-key encryption, bounded storage format, no plaintext/ciphertext in owner or super-admin views; last-four masks only. Legacy rows stay masked but require the explicit dry-run/apply migration; no actual application data/key was changed. Tests cover migration/idempotency, key independence/wrong-key failure, shared missing-key refusal and storage-size/input constraints.
- Staff personal changes: required prior-consent attestation/reference, atomic field-name-only audit event; student/teacher UI exposes scope across studios. A staff assertion is not independent proof of individual consent. Local notes/status and self-edits remain distinct.
- Readiness checks a database query with a timeout; liveness remains separate. Generated request references, template-only request events and generic error responses omit bodies, query strings, supplied IDs, raw object paths and exception text. Uvicorn raw access logs are disabled in deployment startup. Worker failures use IDs/error types instead of sensitive tracebacks.
- API docs/OpenAPI disabled in both root and mounted shared app. Web adds basic embedding/referrer/MIME headers, a limited CSP and production HSTS; it intentionally does not claim a full script-src policy. Header/provider-widget flows are locally tested.
- Six deployment phase cases use fake Docker/curl: backup failure blocks migration; migration failure prevents new activation; API/worker/readiness failures after migration stop writers, preserve artifacts and release metadata, and require compatible recovery. No actual Docker deployment/recovery drill was performed.

## Open work; no production sign-off

The existing product lacks a complete automated personal-data export/erasure workflow and approved retention enforcement. Soft delete retains personal/historical rows; contact-based manual requests require identity verification, scoped fulfillment, evidence and ownership. No live erasure/export or universal retention job was introduced. Older backups/logs may still contain plaintext bank data or historical OTPs. Actual policy/child/guardian/subprocessor/transfer/request operations require owner review.

Host alert routing, off-site encrypted backup retention, WAL/PITR, compatible file/key restore, measured RPO/RTO, actual financial-key provisioning/legacy encryption and Docker/Linux/real-provider verification remain open. Broader authenticated-page accessibility, multi-hour/production-shaped write/worker load and live network/edge headers remain unverified. These limits are also described in the maintained [runtime/privacy operations runbook](/Users/sahil/Documents/work/openroots/progressrooms/progressrooms-api/deploy/RUNTIME_PRIVACY_OPERATIONS.md).

References: [W3C modal dialog behavior](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/), [AnyIO bounded worker threads](https://anyio.readthedocs.io/en/stable/threads.html). Tooling tests exercise project behavior; no regulatory compliance claim is made. All four repositories remain on dev; nothing was committed, pushed, deployed, or run against real application data.
