# Branch and promotion policy

- All development work belongs on `dev`. Before editing, committing, or pushing, check the branch in each affected repository, including nested repositories.
- Keep all four repositories checked out on `dev`. Never switch or check out `uat`, `main` (production), or any `prod`/production branch. Inspect those refs without checking them out when needed.
- `progressrooms/progressrooms-web` and `progressrooms/progressrooms-api` use `main` → `uat` → `dev`: initially create `uat` from `main`, then `dev` from `uat`.
- For Web and API, the user manually creates and handles promotion PRs from `dev` to `uat`, then from `uat` to `main`.
- Never push any branch in any of these four repositories, including `dev`, without asking the user and receiving explicit approval for that push. A request to push authorizes only the requested operation, not future pushes.
- `main` and `uat` remain user-controlled. Do not merge into them, update their remote refs, or create promotion PRs on the user's behalf unless the user explicitly authorizes that specific action.
- The parent `openroots` and `progressrooms` repositories use only `main` and `dev`, with `dev` initially created from `main`.
- Never force-push unless explicitly authorized.
- One-time exception authorized on 2026-10-05: publish all existing local branch refs to GitHub for initial setup. This does not authorize later pushes.
- Preserve existing uncommitted work when changing branches. Do not commit unrelated changes as part of branch setup.
- Branch names are lowercase: `main`, `uat`, `dev`.
