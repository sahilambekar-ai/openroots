# OpenRoots

OpenRoots is the parent organization workspace housing digital platforms, brand assets, architecture blueprints, and product repositories designed to empower independent teachers, instructors, creators, and studio collectives.

---

## 🌿 Project Ecosystem

### 1. [ProgressRooms](https://github.com/sahilambekar-ai/progressrooms)
A multi-tenant operating platform for teachers, instructors, trainers, and studios conducting scheduled classes, workshops, and memberships.

The platform architecture is decomposed into dedicated repositories:

- **Web Frontend**: [`progressrooms-web`](https://github.com/sahilambekar-ai/progressrooms-web) — Built with Next.js 14 (App Router, Tailwind CSS, TypeScript).
- **Backend API**: [`progressrooms-api`](https://github.com/sahilambekar-ai/progressrooms-api) — Built with FastAPI, SQLAlchemy 2.0 (Async), PostgreSQL 16, Redis, and Razorpay.
- **Platform Specs & Docs**: [`progressrooms/docs/`](https://github.com/sahilambekar-ai/progressrooms/tree/main/docs) — Domain models, schema definitions, ER diagrams, RBAC policies, and payment flows.

---

## 📁 Repository Layout

```text
openroots/
├── AGENT_HELPER.md              # AI agent reference guide & environment specifications
├── README.md                    # Root workspace documentation
├── assets/                      # OpenRoots & ProgressRooms brand identity assets
│   └── logo-options/            # Visual identity explorations and variations
├── openroots_logo_01.png        # OpenRoots primary emblem
├── progressrooms/               # ProgressRooms orchestrator & specs (Git Submodule)
├── progressrooms-script.md      # Comprehensive product & technical specification
└── progressrooms_logo_01.png    # ProgressRooms primary emblem
```

---

## 🚀 Getting Started

### Clone with Submodules
To clone this workspace along with all linked submodules:

```bash
git clone --recurse-submodules https://github.com/sahilambekar-ai/openroots.git
cd openroots
```

If already cloned without `--recurse-submodules`:
```bash
git submodule update --init --recursive
```

### Local Development Reference
- Consult [`AGENT_HELPER.md`](./AGENT_HELPER.md) for local database credentials, service configuration, and AI agent execution rules.
- Review [`progressrooms-script.md`](./progressrooms-script.md) for detailed multi-tenant SaaS functional requirements.
- Refer to [`progressrooms/README.md`](./progressrooms/README.md) for local Docker Compose infrastructure and services startup.

---

## 🛡️ License

Private & Proprietary © OpenRoots.
