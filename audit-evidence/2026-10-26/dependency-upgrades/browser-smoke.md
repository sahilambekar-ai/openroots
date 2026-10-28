# Dependency upgrade smoke checks (2026-10-26)

Local Next 15.5.28 production build served at localhost:3107.
- Homepage rendered; clicked Login and then Create an Account.
- Studio registration rendered; Student button switched the heading and fields.
- /privacy?role=STUDENT rendered the Students audience.
- No account was created and no credentials or payments were submitted.
- Sharp 0.35.5 transformed a 20x10 SVG into a 10x5 WebP.
- /_next/image?url=%2Fbrand%2Flogo-transparent.png&w=64&q=75 returned 200 image/png.
- Temporary browser tab/server were closed after verification.

These checks do not replace the planned authenticated component/Playwright journeys.
