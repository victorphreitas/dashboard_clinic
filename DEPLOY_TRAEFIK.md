# Deploy Dashboard behind Traefik (DigitalOcean + Docker)

Production setup for **dashboard_clinic** at **https://painel.agenciakimera.com** via Traefik, with no public container ports.

---

## 1. docker-compose service (copy-paste ready)

Use the file **`docker-compose.traefik.yml`** in this repo. Summary:

- **No `ports:`** — container is only reachable through Traefik.
- **Network:** `traefik-public` (must exist; create with `docker network create traefik-public` if needed).
- **HTTPS:** Let's Encrypt via Traefik resolver `letsencrypt`.
- **HTTP:** Redirect to HTTPS.
- **Healthcheck:** Streamlit `/_stcore/health` every 30s.

If your Traefik uses another **cert resolver** or **entrypoint** name, change in the compose:

- `traefik.http.routers.dashboard-clinic.tls.certresolver=letsencrypt` → your resolver (e.g. `le`).
- `websecure` / `web` → your entrypoints (e.g. `https` / `http`).

---

## 2. GitHub Actions workflow

File: **`.github/workflows/deploy.yml`**

- **Trigger:** push to `main`.
- **Build:** Builds image and pushes to **GitHub Container Registry (GHCR)**.
- **Deploy:** SSH to Droplet → login to GHCR → pull → `docker compose up -d --force-recreate`.

### GitHub Secrets (required)

| Secret           | Description |
|------------------|-------------|
| `SSH_PRIVATE_KEY` | Private key for SSH to the Droplet (full key, including `-----BEGIN ... -----`) |
| `DROPLET_HOST`    | Droplet IP or hostname (e.g. `192.241.157.215`) |
| `DROPLET_USER`    | SSH user (e.g. `root` or `ubuntu`). Optional; default `root` |
| `GHCR_PAT`        | GitHub PAT with `read:packages` so the Droplet can pull the image |

### GitHub variable (optional)

| Variable      | Description |
|---------------|-------------|
| `DEPLOY_PATH` | Path on Droplet where `docker-compose.traefik.yml` lives (default: `/opt/dashboard_clinic`) |

### GHCR visibility

- First push creates the package under `ghcr.io/<your-org-or-user>/dashboard_clinic`.
- If the package is **private**, the Droplet must use `GHCR_PAT` (above).
- To avoid PAT: set package to **Public** (Repo → Packages → dashboard_clinic → Package settings → Change visibility).

---

## 3. Commands for the Droplet

For a full step-by-step in Portuguese (first-time setup and updates), see **[DEPLOY_DROPLET.md](DEPLOY_DROPLET.md)**.

### One-time setup on the Droplet

```bash
# Create app directory
sudo mkdir -p /opt/dashboard_clinic
sudo chown $USER:$USER /opt/dashboard_clinic
cd /opt/dashboard_clinic

# Ensure Traefik network exists (if not already)
docker network create traefik-public 2>/dev/null || true

# Copy compose file (from your machine or clone repo)
# Option A: clone repo and use compose from there
git clone https://github.com/YOUR_ORG/prestige_clinic_dash.git .
# Option B: copy only the compose file and create .env for IMAGE
# scp docker-compose.traefik.yml user@192.241.157.215:/opt/dashboard_clinic/
```

Create `.env` on the Droplet if you use GHCR image (CI sets `IMAGE`; for manual runs set it here):

```bash
# /opt/dashboard_clinic/.env
IMAGE=ghcr.io/YOUR_GITHUB_OWNER/dashboard_clinic:latest
```

### Build image (local or CI)

```bash
# Local build (from repo root)
docker build -t dashboard_clinic:latest .

# Tag for GHCR (replace OWNER with your GitHub user/org)
docker tag dashboard_clinic:latest ghcr.io/OWNER/dashboard_clinic:latest
```

### Push to GHCR

```bash
# Login (use a PAT with write:packages or use GitHub CLI)
echo YOUR_GITHUB_PAT | docker login ghcr.io -u OWNER --password-stdin

# Push
docker push ghcr.io/OWNER/dashboard_clinic:latest
```

### Deploy / redeploy on the Droplet

```bash
cd /opt/dashboard_clinic

# Set image if not in .env (for GHCR)
export IMAGE=ghcr.io/YOUR_OWNER/dashboard_clinic:latest

# Pull and recreate (zero-downtime style: new container then old removed)
docker compose -f docker-compose.traefik.yml pull
docker compose -f docker-compose.traefik.yml up -d --force-recreate

# Optional: prune old images
docker image prune -f
```

### Stop exposing port 8501

If the dashboard was previously run with `-p 8501:10000` or similar:

1. Stop that container: `docker stop <container_name>` (or remove the `ports:` from the old compose).
2. Deploy only with `docker-compose.traefik.yml` (no port mapping).
3. Access only via **https://painel.agenciakimera.com**.

---

## 4. Zero-downtime deploy strategy

- **`docker compose up -d --force-recreate`** starts a new container and then stops the old one. Traefik switches to the new container when it’s healthy; brief in-flight requests may complete on the old container.
- For smoother rollout:
  - Use **Traefik health checks** (already in the compose: `loadbalancer.healthcheck.path=/_stcore/health`). Traefik will send traffic only to healthy backends.
  - Optionally add a short **scripted delay**: pull → up -d (new container) → sleep 5 → stop old by name. For a single replica, `--force-recreate` is usually enough.

---

## 5. Troubleshooting checklist

### Traefik

- **Logs:**  
  `docker logs traefik 2>&1 | tail -100`  
  or container name you use for Traefik.
- **Routers:** In Traefik dashboard (if enabled) or logs, confirm a router for `painel.agenciakimera.com` and no errors.
- **Backend:** Check that the service points to port **10000** and that the backend is “UP”.

### Dashboard container

- **Logs:**  
  `docker logs dashboard_clinic 2>&1 | tail -200`
- **Health:**  
  `docker exec dashboard_clinic curl -s -o /dev/null -w "%{http_code}" http://localhost:10000/_stcore/health`  
  Expected: `200`.
- **Inspect:**  
  `docker inspect dashboard_clinic` — confirm it’s on network `traefik-public`.

### DNS

- **Resolution:**  
  `dig +short painel.agenciakimera.com`  
  or `nslookup painel.agenciakimera.com`  
  Must return the Droplet’s public IP (e.g. 192.241.157.215).
- **Propagation:** If you just changed DNS, wait 5–60 minutes and recheck.

### SSL (Let’s Encrypt)

- **Certificate:** In Traefik logs, look for ACME / certificate success or errors for `painel.agenciakimera.com`.
- **Resolver:** Compose uses `certresolver=letsencrypt`. If your Traefik uses another name, update the label.
- **Browser:** Check certificate in browser (valid issuer, no mixed content).

### Network

- **Traefik and dashboard on same network:**  
  `docker network inspect traefik-public`  
  Both Traefik and `dashboard_clinic` should be listed.
- **No public port:**  
  `docker port dashboard_clinic`  
  Should show nothing (no host port mapping).

### Quick end-to-end

```bash
# From the Droplet
curl -sI http://localhost:10000/_stcore/health   # from host to container (if port not published, use exec)
docker exec dashboard_clinic curl -sI http://localhost:10000/_stcore/health
curl -sI -H "Host: painel.agenciakimera.com" http://127.0.0.1:80/   # Traefik HTTP (redirect)
curl -sI -k -H "Host: painel.agenciakimera.com" https://127.0.0.1:443/  # Traefik HTTPS (optional -k if self-signed during issuance)
```

---

## 6. Architecture flow

```
Internet
    │
    ▼
[DNS: painel.agenciakimera.com → 192.241.157.215]
    │
    ▼
Droplet (ports 80 / 443)
    │
    ▼
Traefik container
    │  • Terminates TLS (Let’s Encrypt)
    │  • Router: Host(`painel.agenciakimera.com`) → service dashboard-clinic
    │  • Resolves backend on network traefik-public
    │
    ▼
dashboard_clinic container (port 10000, no host port)
    │  • Streamlit on 0.0.0.0:10000
    │  • Health: /_stcore/health
    │
    ▼
Response to client (HTTPS)
```

- **No direct exposure** of the dashboard container; only Traefik listens on 80/443.
- **Single entry point:** All traffic for `painel.agenciakimera.com` goes to Traefik, then to the dashboard service on the same Docker network.
