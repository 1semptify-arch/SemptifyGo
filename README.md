# Semptify Go

[![Deploy on Render](https://img.shields.io/badge/Render-Deploy-blue)](https://render.com)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)

**Your lease. Your documents. Your deposit.**

Semptify Go is a free, open-source mobile web app that helps tenants organize their housing journey — from signing the lease to getting their full deposit back. Upload documents, build timelines, and generate demand letters when landlords withhold unfair deductions.

Built mobile-first for Android and iOS browsers. Your data lives in your Google Drive, Dropbox, or OneDrive — we don't store it. Free forever. No ads. No accounts. Just tenant rights.

---

## What It Does

| Feature | Description |
|---------|-------------|
| 📄 **Document Upload** | Store leases, receipts, photos, emails in your cloud |
| 📊 **Timeline Builder** | Chronological case history, auto-extracted from documents |
| ✉️ **Demand Letters** | Auto-generated deposit dispute letters with your evidence |
| 📰 **Tenant Tidbits** | Daily tips on tenant rights from around the world |
| 🔒 **Privacy First** | Your data never touches our servers — stays in your cloud |

---

## Mobile-First

Designed for tenants on the move. Works in any mobile browser (Chrome, Safari). Add to home screen for an app-like experience. Touch-optimized, offline-capable, fast.

---

## Free Forever

- **No ads** — never
- **No tracking** — we don't want your data
- **No data mining** — we can't see your documents
- **No paid tiers** — free means free

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI + Python 3.12 |
| **Database** | PostgreSQL 16 |
| **Cache** | Redis 7 |
| **Frontend** | Vanilla JS + CSS (mobile-optimized) |
| **Auth** | OAuth2 (Google Drive, Dropbox, OneDrive) |
| **Encryption** | Fernet (AES-128) |
| **Deploy** | Render.com (free tier) |

---

## Quick Start

### Local Development

```bash
# Clone
git clone https://github.com/yourusername/semptify55.git
cd semptify55

# Setup environment
cp .env.example .env
# Edit .env with your OAuth credentials

# Run with Docker
docker-compose up

# Or native Python
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit `http://localhost:8000`

### Deploy to Render

1. Fork this repo
2. Go to [dashboard.render.com](https://dashboard.render.com)
3. Click **New → Blueprint**
4. Connect your GitHub repo
5. Render reads `render.yaml` and sets up:
   - Web service (Python)
   - PostgreSQL database
   - Redis cache
6. Add your OAuth credentials in **Environment** tab
7. Deploy — auto-updates on every push to `main`

---

## How It Works

```
1. Connect Your Storage
   ↓ OAuth to Google Drive, Dropbox, or OneDrive
   
2. Create a Case
   ↓ Lease dispute, deposit fight, eviction defense
   
3. Upload Documents
   ↓ Photos, receipts, emails — all to your cloud
   
4. Build Timeline
   ↓ Auto-extracted dates + manual events
   
5. Take Action
   ↓ Generate demand letters, know your rights
```

Your documents never touch our servers. They're stored in **your** cloud account, in a `Semptify Go/` folder you control.

---

## Tenant Rights Focus

Semptify Go is built for truth from **both** sides:

- We don't assume tenant claims are automatically true
- We don't assume landlord claims are automatically true
- We build for **facts, records, chronology, and evidence**
- We **do not** support deceptive, retaliatory, or manipulative flows

---

## Contributing

This is a housing justice tool. Contributions welcome — especially from:

- Tenant organizers
- Legal aid technologists  
- Mobile UX designers
- Housing attorneys

Read [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

---

## License

[AGPL-3.0](LICENSE) — Free forever, open forever. If you modify and distribute, share alike.

---

## About

Built by tenants, for tenants. Not a startup. No investors. No exit strategy. Just code that helps people keep their homes and their money.

**Questions?** Open an issue or start a discussion.

---

*Built for tenants, not landlords.*
